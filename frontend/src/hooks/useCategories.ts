import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getCategoryTree, createCategory, renameCategory, deleteCategory } from '@/api/categories';

// ---------------------------------------------------------------------------
// Query keys
// ---------------------------------------------------------------------------

export const categoryKeys = {
  all: ['categories'] as const,
  tree: () => [...categoryKeys.all, 'tree'] as const,
};

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

/**
 * Fetch the full category tree. staleTime: 60s (rarely changes).
 */
export function useCategoryTree() {
  return useQuery({
    queryKey: categoryKeys.tree(),
    queryFn: getCategoryTree,
    staleTime: 60_000,
  });
}

/**
 * Create a new category. Invalidates tree on success.
 */
export function useCreateCategory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { name: string; parent_id?: string }) => createCategory(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoryKeys.tree() });
    },
  });
}

/**
 * Rename a category. Invalidates tree on success.
 */
export function useRenameCategory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, name }: { id: string; name: string }) => renameCategory(id, name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoryKeys.tree() });
    },
  });
}

/**
 * Delete a category. Invalidates tree on success.
 */
export function useDeleteCategory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteCategory(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoryKeys.tree() });
    },
  });
}
