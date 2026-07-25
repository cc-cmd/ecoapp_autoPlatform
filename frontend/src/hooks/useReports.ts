import { useQuery } from '@tanstack/react-query';
import { getReportSummary, getReportDetail } from '@/api/reports';

// ---------------------------------------------------------------------------
// Query keys
// ---------------------------------------------------------------------------

export const reportKeys = {
  all: ['reports'] as const,
  summary: (days?: number) => [...reportKeys.all, 'summary', days ?? 7] as const,
  detail: (id: string) => [...reportKeys.all, 'detail', id] as const,
};

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

/**
 * Fetch aggregated report summary. staleTime: 60s (aggregate data).
 */
export function useReportSummary(days?: number) {
  return useQuery({
    queryKey: reportKeys.summary(days),
    queryFn: () => getReportSummary(days),
    staleTime: 60_000,
  });
}

/**
 * Fetch detailed report for a specific batch.
 */
export function useReportDetail(id: string) {
  return useQuery({
    queryKey: reportKeys.detail(id),
    queryFn: () => getReportDetail(id),
    staleTime: 0,
    enabled: !!id,
  });
}
