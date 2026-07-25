import React from 'react';
import { Tag } from 'antd';
import type { DeviceStatus, RunStatus, BatchStatus } from '@/types';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type StatusType = 'device' | 'run' | 'batch';

interface StatusTagProps {
  /** The status value to display. */
  status: DeviceStatus | RunStatus | BatchStatus;
  /** The type of status, determines color mapping. */
  type: StatusType;
}

// ---------------------------------------------------------------------------
// Color mappings
// ---------------------------------------------------------------------------

const deviceStatusColors: Record<DeviceStatus, string> = {
  online: 'green',
  busy: 'orange',
  offline: 'default',
};

const runStatusColors: Record<RunStatus, string> = {
  queued: 'blue',
  running: 'processing',
  passed: 'green',
  failed: 'red',
  error: 'red',
};

const batchStatusColors: Record<BatchStatus, string> = {
  queued: 'blue',
  running: 'processing',
  completed: 'green',
};

const deviceStatusLabels: Record<DeviceStatus, string> = {
  online: '在线',
  busy: '忙碌',
  offline: '离线',
};

const runStatusLabels: Record<RunStatus, string> = {
  queued: '排队中',
  running: '运行中',
  passed: '通过',
  failed: '失败',
  error: '错误',
};

const batchStatusLabels: Record<BatchStatus, string> = {
  queued: '排队中',
  running: '运行中',
  completed: '已完成',
};

// ---------------------------------------------------------------------------
// StatusTag
// ---------------------------------------------------------------------------

/**
 * Colored tag component for displaying device / run / batch status.
 */
const StatusTag: React.FC<StatusTagProps> = ({ status, type }) => {
  let color: string;
  let label: string;

  switch (type) {
    case 'device':
      color = deviceStatusColors[status as DeviceStatus] || 'default';
      label = deviceStatusLabels[status as DeviceStatus] || String(status);
      break;
    case 'run':
      color = runStatusColors[status as RunStatus] || 'default';
      label = runStatusLabels[status as RunStatus] || String(status);
      break;
    case 'batch':
      color = batchStatusColors[status as BatchStatus] || 'default';
      label = batchStatusLabels[status as BatchStatus] || String(status);
      break;
    default:
      color = 'default';
      label = String(status);
  }

  return <Tag color={color}>{label}</Tag>;
};

export default StatusTag;
