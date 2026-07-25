import React, { useState } from 'react';
import { Card, Typography, Button, message } from 'antd';
import { PlayCircleOutlined } from '@ant-design/icons';
import { useTriggerRun } from '@/hooks/useRuns';
import CaseSelectionTable from './CaseSelectionTable';
import RunQueue from './RunQueue';

const { Title } = Typography;

/**
 * Execution panel page with case selection for triggering runs
 * and the batch queue table for tracking execution progress.
 */
const RunsPage: React.FC = () => {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const { mutateAsync: triggerRun, isPending: isTriggering } = useTriggerRun();

  const handleTriggerRun = async () => {
    if (selectedIds.size === 0) {
      message.warning('请至少选择一个用例');
      return;
    }

    try {
      // TODO: Call triggerRun mutation
      await triggerRun({ test_case_ids: Array.from(selectedIds) });
      message.success('执行已触发');
      setSelectedIds(new Set());
    } catch {
      message.error('触发执行失败');
    }
  };

  return (
    <div>
      <Title level={4} style={{ marginBottom: 24 }}>
        执行面板
      </Title>

      {/* Case selection for triggering */}
      <Card
        title="选择用例"
        style={{ marginBottom: 16 }}
        extra={
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={handleTriggerRun}
            loading={isTriggering}
            disabled={selectedIds.size === 0}
          >
            执行所选 ({selectedIds.size})
          </Button>
        }
      >
        <CaseSelectionTable
          selectedIds={selectedIds}
          onSelectionChange={setSelectedIds}
        />
      </Card>

      {/* Run queue */}
      <Card title="执行队列">
        <RunQueue />
      </Card>
    </div>
  );
};

export default RunsPage;
