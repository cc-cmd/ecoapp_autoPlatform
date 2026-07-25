import apiClient from './client';
import type { LoginRequest, RegisterRequest, AuthResponse, RegisterResponse } from '@/types';

/**
 * Login with username and password.
 * Returns JWT token and user info.
 */
export async function login(data: LoginRequest): Promise<AuthResponse> {
  const response = await apiClient.post<AuthResponse>('/auth/login', data);
  return response.data;
}

/**
 * Register a new user.
 * Does NOT return a token — user must log in separately.
 */
export async function register(data: RegisterRequest): Promise<RegisterResponse> {
  const response = await apiClient.post<RegisterResponse>('/auth/register', data);
  return response.data;
}
