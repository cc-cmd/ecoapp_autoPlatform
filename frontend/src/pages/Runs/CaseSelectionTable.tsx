import React, { useState } from 'react';
import { Table, Button } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { useCases } from '@/hooks/useCases';
import type { TestCase } from '@/types';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CaseSelectionTableProps {
  /** Currently selected case IDs. */
  selectedIds: Set<string>;
  /** Callback when selection changes. */
  onSelectionChange: (ids: Set<string>) => void;
}

// ---------------------------------------------------------------------------
// CaseSelectionTable
// ---------------------------------------------------------------------------

/**
 * Table with checkbox selection for choosing test cases to execute.
 * Supports multi-page selection via Set<string> state.
 */
const CaseSelectionTable: React.FC<CaseSelectionTableProps> = ({
  selectedIds,
  onSelectionChange,
}) => {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useCases({ page, size: 20 });

  const columns: ColumnsType<TestCase> = [
    {
      title: '用例名称',
      dataIndex: 'name',
      key: 'name',
      ellipsis: true,
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 80,
    },
    {
      title: '平台',
      dataIndex: 'platform',
      key: 'platform',
      width: 100,
      render: (platform: string) => (platform === 'android' ? 'Android' : 'iOS'),
    },
    {
      title: '分类',
      dataIndex: 'category_name',
      key: 'category_name',
      width: 150,
      ellipsis: true,
    },
  ];

  const rowSelection = {
    selectedRowKeys: Array.from(selectedIds),
    onSelect: (record: TestCase) => {
      const next = new Set(selectedIds);
      if (next.has(record.id)) {
        next.delete(record.id);
      } else {
        next.add(record.id);
      }
      onSelectionChange(next);
    },
    onSelectAll: (selected: boolean, _selectedRows: TestCase[], changeRows: TestCase[]) => {
      const next = new Set(selectedIds);
      changeRows.forEach((row) => {
        if (selected) {
          next.add(row.id);
        } else {
          next.delete(row.id);
        }
      });
      onSelectionChange(next);
    },
  };

  return (
    <div>
      <div style={{ marginBottom: 8 }}>
        已选择 <strong>{selectedIds.size}</strong> 个用例
        {selectedIds.size > 0 && (
          <Button
            type="link"
            size="small"
            onClick={() => onSelectionChange(new Set())}
            style={{ marginLeft: 8 }}
          >
            清除选择
          </Button>
        )}
      </div>
      <Table
        dataSource={data?.items}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        rowSelection={rowSelection}
        pagination={{
          current: page,
          pageSize: 20,
          total: data?.total ?? 0,
          onChange: (p) => setPage(p),
          showSizeChanger: false,
        }}
        size="small"
        locale={{ emptyText: '暂无用例数据' }}
      />
    </div>
  );
};

export default CaseSelectionTable;
