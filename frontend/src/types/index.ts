/** Priority levels for test cases */
export type Priority = 'P0' | 'P1' | 'P2' | 'P3';

/** Supported mobile platforms */
export type Platform = 'android' | 'ios';

/** Device connection status */
export type DeviceStatus = 'online' | 'busy' | 'offline';

/** Test run status state machine */
export type RunStatus = 'queued' | 'running' | 'passed' | 'failed' | 'error';

/** Batch execution status */
export type BatchStatus = 'queued' | 'running' | 'completed';

/** Standard API error response */
export interface ApiError {
  code: number;
  message: string;
  details?: Record<string, string[]>;
}

/** Paginated response wrapper */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

/** User account model (as returned by API) */
export interface User {
  id: string;
  username: string;
  created_at: string;
}

/** Login request payload */
export interface LoginRequest {
  username: string;
  password: string;
}

/** Registration request payload */
export interface RegisterRequest {
  username: string;
  password: string;
}

/** Login response */
export interface AuthResponse {
  token: string;
  user: User;
}

/** Registration response (no token — user must log in separately) */
export interface RegisterResponse {
  user: User;
}

/** Test case model */
export interface TestCase {
  id: string;
  name: string;
  priority: Priority;
  platform: Platform;
  is_automated: boolean;
  category_id: string;
  category_name?: string;
  steps?: string;
  script_path?: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

/** Parameters for listing test cases */
export interface TestCaseListParams {
  page?: number;
  size?: number;
  search?: string;
  category_id?: string;
  priority?: Priority;
  platform?: Platform;
  is_automated?: boolean;
}

/** Create test case request */
export interface CreateCaseRequest {
  name: string;
  priority: Priority;
  platform: Platform;
  is_automated: boolean;
  category_id: string;
  steps?: string;
}

/** Update test case request */
export interface UpdateCaseRequest {
  name?: string;
  priority?: Priority;
  platform?: Platform;
  is_automated?: boolean;
  category_id?: string;
  steps?: string;
}

/** Test case category */
export interface Category {
  id: string;
  name: string;
  parent_id: string | null;
  sort_order: number;
  created_at: string;
}

/** Category tree node (with children) */
export interface CategoryTreeNode extends Category {
  children: CategoryTreeNode[];
}

/** Test device model */
export interface Device {
  id: string;
  name: string;
  udid: string;
  platform: Platform;
  os_version: string;
  status: DeviceStatus;
  last_heartbeat: string;
  created_at: string;
}

/** Single test run record */
export interface TestRun {
  id: string;
  run_group_id: string;
  test_case_id: string;
  test_case_name?: string;
  status: RunStatus;
  device_id?: string;
  device_name?: string;
  log_path?: string;
  started_at?: string;
  finished_at?: string;
  duration_ms?: number;
  error_message?: string;
  log?: string;
  created_at: string;
}

/** Execution batch (one trigger = one batch) */
export interface RunGroup {
  id: string;
  name: string;
  status: BatchStatus;
  triggered_by: string;
  test_run_count: number;
  passed_count: number;
  failed_count: number;
  error_count: number;
  started_at?: string;
  finished_at?: string;
  created_at: string;
}

/** Trigger a new execution run */
export interface TriggerRunRequest {
  test_case_ids: string[];
  device_id?: string;
}

/** Parameters for listing runs */
export interface RunListParams {
  page?: number;
  size?: number;
  status?: RunStatus | BatchStatus;
  case_id?: string;
  batch_id?: string;
}

/** Report summary (aggregated statistics) */
export interface ReportSummary {
  total_cases: number;
  automated_cases: number;
  total_runs: number;
  pass_rate: number;
  fail_rate: number;
  runs_by_day: Array<{ date: string; passed: number; failed: number; error: number }>;
}

/** Detailed report for a specific batch */
export interface ReportDetail {
  batch: RunGroup;
  runs: TestRun[];
  summary: {
    total: number;
    passed: number;
    failed: number;
    error: number;
    pass_rate: number;
    total_duration_ms: number;
  };
}
