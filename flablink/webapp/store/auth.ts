// src/store/authStore.ts
import { create } from 'zustand';

type AuthState = {
  isAuthenticated: boolean;
  login: (username: string, password: string) => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  login: (username, password) => {
    if (username === 'admin' && password === 'admin') {
      set({ isAuthenticated: true });
      localStorage.setItem('auth', JSON.stringify({ isAuthenticated: true }));
    } else {
      console.error('Invalid credentials');
    }
  },
  logout: () => {
    localStorage.removeItem('auth');
    set({ isAuthenticated: false });
  },
}));

// To initialize the store with persisted state from localStorage
const persistedState = localStorage.getItem('auth');
if (persistedState) {
  const parsedState = JSON.parse(persistedState);
  if (parsedState.isAuthenticated) {
    useAuthStore.setState(parsedState);
  }
}


// usage