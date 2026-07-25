import apiClient from './client';
import type { ReportSummary, ReportDetail } from '@/types';

/**
 * Get aggregated report summary for the dashboard.
 * @param days - Number of days to include (default 7).
 */
export async function getReportSummary(days?: number): Promise<ReportSummary> {
  const response = await apiClient.get<ReportSummary>('/reports/summary', { params: { days } });
  return response.data;
}

/**
 * Get detailed report for a specific batch.
 */
export async function getReportDetail(id: string): Promise<ReportDetail> {
  const response = await apiClient.get<ReportDetail>(`/reports/batches/${id}`);
  return response.data;
}
