import apiClient from './client';
import type { PaginatedResponse, TestCase, TestCaseListParams, CreateCaseRequest, UpdateCaseRequest } from '@/types';

/**
 * Get paginated list of test cases.
 */
export async function getCases(params?: TestCaseListParams): Promise<PaginatedResponse<TestCase>> {
  const response = await apiClient.get<PaginatedResponse<TestCase>>('/cases', { params });
  return response.data;
}

/**
 * Get a single test case by ID.
 */
export async function getCase(id: string): Promise<TestCase> {
  const response = await apiClient.get<TestCase>(`/cases/${id}`);
  return response.data;
}

/**
 * Create a new test case.
 */
export async function createCase(data: CreateCaseRequest): Promise<TestCase> {
  const response = await apiClient.post<TestCase>('/cases', data);
  return response.data;
}

/**
 * Update an existing test case.
 */
export async function updateCase(id: string, data: UpdateCaseRequest): Promise<TestCase> {
  const response = await apiClient.put<TestCase>(`/cases/${id}`, data);
  return response.data;
}

/**
 * Delete a test case.
 */
export async function deleteCase(id: string): Promise<void> {
  await apiClient.delete(`/cases/${id}`);
}

/**
 * Upload a Python script for a test case.
 * Uses multipart/form-data.
 */
export async function uploadScript(id: string, file: File): Promise<{ script_path: string }> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post<{ script_path: string }>(`/cases/${id}/script`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

/**
 * Download the Python script for a test case.
 */
export async function downloadScript(id: string): Promise<Blob> {
  const response = await apiClient.get<Blob>(`/cases/${id}/script`, { responseType: 'blob' });
  return response.data;
}

/**
 * Get execution history for a test case.
 */
export async function getExecutionHistory(id: string, params?: { page?: number; size?: number }): Promise<PaginatedResponse<import('@/types').TestRun>> {
  const response = await apiClient.get(`/cases/${id}/runs`, { params });
  return response.data;
}
