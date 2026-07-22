# LowDiskOnPostgres

**Severity:** Warning  
**Condition:** PostgreSQL persistent volume usage exceeds 80% for five minutes.

## Confirm

```bash
kubectl -n banking get pvc
kubectl -n banking exec postgres-0 -- df -h /var/lib/postgresql/data
kubectl -n banking exec postgres-0 -- psql -U banking_user -d bankingdb -c "SELECT pg_size_pretty(pg_database_size('bankingdb'));"
```

## Remediate

1. Identify unexpected database, WAL, temporary-file, or log growth.
2. Expand the PVC using the StorageClass-supported process before capacity becomes critical.
3. Apply approved retention or maintenance and verify backups before deleting data.
