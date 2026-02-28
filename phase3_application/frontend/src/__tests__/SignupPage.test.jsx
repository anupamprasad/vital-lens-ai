import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SignupPage from '../pages/SignupPage';
import * as api from '../services/api';
import { MemoryRouter } from 'react-router-dom';

// mock navigate hook using Vitest's `vi` while preserving other exports
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('SignupPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('submits form and calls authService.signup', async () => {
    const signupSpy = vi.spyOn(api.authService, 'signup').mockResolvedValue({
      data: { access_token: 'token', user: { id: 1, email: 'a@b.com', name: 'A' } },
    });
    const onSignup = vi.fn();

    render(
      <MemoryRouter>
        <SignupPage onSignup={onSignup} />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('John Doe'), {
      target: { value: 'Alice' },
    });
    fireEvent.change(screen.getByPlaceholderText('you@example.com'), {
      target: { value: 'alice@example.com' },
    });
    const passFields = screen.getAllByPlaceholderText('••••••••');
    // first field is password, second is confirm
    fireEvent.change(passFields[0], { target: { value: 'password123' } });
    fireEvent.change(passFields[1], { target: { value: 'password123' } });

    fireEvent.click(screen.getByLabelText(/privacy policy/i));
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => {
      expect(signupSpy).toHaveBeenCalledWith('Alice', 'alice@example.com', 'password123');
      expect(onSignup).toHaveBeenCalled();
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });
});
