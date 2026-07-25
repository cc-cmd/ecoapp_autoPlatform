import apiClient from './client';
import type { CategoryTreeNode, Category } from '@/types';

/**
 * Get the full category tree.
 */
export async function getCategoryTree(): Promise<CategoryTreeNode[]> {
  const response = await apiClient.get<CategoryTreeNode[]>('/categories/tree');
  return response.data;
}

/**
 * Create a new category.
 */
export async function createCategory(data: { name: string; parent_id?: string }): Promise<Category> {
  const response = await apiClient.post<Category>('/categories', data);
  return response.data;
}

/**
 * Rename a category.
 */
export async function renameCategory(id: string, name: string): Promise<Category> {
  const response = await apiClient.put<Category>(`/categories/${id}`, { name });
  return response.data;
}

/**
 * Delete a category.
 */
export async function deleteCategory(id: string): Promise<void> {
  await apiClient.delete(`/categories/${id}`);
}
