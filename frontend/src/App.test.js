import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

// Mock the context provider to prevent errors
jest.mock('./context/AuthContext', () => ({
  AuthProvider: ({ children }) => children,
  useAuth: () => ({
    isAuthenticated: false,
    currentUser: null,
    login: jest.fn(),
    logout: jest.fn()
  })
}));

test('renders without crashing', () => {
  // This is a very basic test that just makes sure the component renders
  render(<App />);
});