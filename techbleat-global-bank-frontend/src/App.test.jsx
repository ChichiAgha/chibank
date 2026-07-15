import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';

describe('Techbleat Global Bank frontend', () => {
  beforeEach(() => {
    vi.resetModules();
    window.__APP_CONFIG__ = {
      USER_API: '/api/users',
      TX_API: '/api/transactions',
      ACTIVITY_API: '/api/activities',
    };

    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: () => Promise.resolve([]),
        }),
      ),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    delete window.__APP_CONFIG__;
  });

  test('renders the login screen and loads users through configured API path', async () => {
    const { default: App } = await import('./App');

    render(<App />);

    expect(screen.getByRole('heading', { name: /welcome back/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        '/api/users/users',
        expect.objectContaining({
          headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
        }),
      );
    });
  });
});
