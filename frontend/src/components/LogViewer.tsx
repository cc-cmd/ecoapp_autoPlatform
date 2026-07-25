import React, { useRef, useEffect } from 'react';
import { Spin, Typography } from 'antd';

const { Text } = Typography;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface LogViewerProps {
  /** Log content to display. */
  log?: string;
  /** Whether the log is still loading. */
  loading?: boolean;
}

// ---------------------------------------------------------------------------
// LogViewer
// ---------------------------------------------------------------------------

/**
 * Monospace, dark-themed log viewer with auto-scroll to bottom.
 * Displays execution logs in a pre-formatted block.
 */
const LogViewer: React.FC<LogViewerProps> = ({ log, loading = false }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new log content arrives
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [log]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 24 }}>
        <Spin tip="加载日志中..." />
      </div>
    );
  }

  if (!log) {
    return (
      <div style={{ textAlign: 'center', padding: 24 }}>
        <Text type="secondary">暂无日志</Text>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="log-container"
      style={{
        background: '#1e1e1e',
        color: '#d4d4d4',
        fontFamily: "'SF Mono', Monaco, 'Cascadia Code', Consolas, monospace",
        fontSize: 13,
        padding: 16,
        borderRadius: 6,
        maxHeight: 500,
        overflow: 'auto',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-all',
        lineHeight: 1.6,
      }}
    >
      {log}
    </div>
  );
};

export default LogViewer;
