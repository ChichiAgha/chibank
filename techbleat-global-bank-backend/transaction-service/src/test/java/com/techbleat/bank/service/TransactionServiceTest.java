package com.techbleat.bank.service;

import com.techbleat.bank.model.Account;
import com.techbleat.bank.repo.AccountRepository;
import com.techbleat.bank.repo.BankTransactionRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

import java.util.Map;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TransactionServiceTest {

    @Mock
    private AccountRepository accountRepository;

    @Mock
    private BankTransactionRepository transactionRepository;

    @Mock
    private KafkaTemplate<String, Object> kafkaTemplate;

    @InjectMocks
    private TransactionService transactionService;

    @Test
    void depositIncreasesBalanceAndPublishesEvent() {
        Account account = new Account();
        account.setUserId("user1");
        account.setBalance(100.0);

        when(accountRepository.findById("user1")).thenReturn(Optional.of(account));

        Map<String, Object> response = transactionService.deposit("user1", 50.0);

        assertEquals("Deposit successful", response.get("message"));
        assertEquals(150.0, response.get("balance"));
        verify(accountRepository).save(account);
        verify(transactionRepository).save(any());
        verify(kafkaTemplate).send(eq("banking-transactions"), eq("user1"), any());
    }

    @Test
    void withdrawRejectsInsufficientFunds() {
        Account account = new Account();
        account.setUserId("user1");
        account.setBalance(25.0);

        when(accountRepository.findById("user1")).thenReturn(Optional.of(account));

        RuntimeException error = assertThrows(
                RuntimeException.class,
                () -> transactionService.withdraw("user1", 50.0)
        );

        assertEquals("Insufficient funds", error.getMessage());
    }

    @Test
    void depositRejectsInvalidAmount() {
        RuntimeException error = assertThrows(
                RuntimeException.class,
                () -> transactionService.deposit("user1", 0.0)
        );

        assertEquals("Amount must be greater than zero", error.getMessage());
    }
}
