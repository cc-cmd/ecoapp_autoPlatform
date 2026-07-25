import React, { useCallback, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Table, Button, Input, Select, Space, Tag, Modal, Form, message, Alert } from 'antd';
import { PlusOutlined, SearchOutlined, EditOutlined } from '@ant-design/icons';
import { useCases, useCreateCase } from '@/hooks/useCases';
import type { TestCase, TestCaseListParams, CreateCaseRequest, Priority, Platform } from '@/types';

const { Option } = Select;

// ---------------------------------------------------------------------------
// Columns
// ---------------------------------------------------------------------------

interface CaseTableProps {
  categoryId?: string;
}

/**
 * Test case table with search, filtering, inline editing, pagination, and create modal.
 * Features 300ms debounced search and antd Table with row hover actions.
 * Search/priority/page are synced to URL search params.
 */
const CaseTable: React.FC<CaseTableProps> = ({ categoryId }) => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const search = searchParams.get('search') || '';
  const priority = (searchParams.get('priority') as Priority | '') || '';
  const page = parseInt(searchParams.get('page') || '1', 10);

  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [createForm] = Form.useForm<CreateCaseRequest>();
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();

  const params: TestCaseListParams = {
    page,
    size: 20,
    search: search || undefined,
    category_id: categoryId,
    priority: priority || undefined,
  };

  const { data, isLoading, isError } = useCases(params);
  const { mutateAsync: createCase, isPending: isCreating } = useCreateCase();
  // TODO: useDeleteCase for delete functionality

  // 300ms debounced search — writes to URL params
  const handleSearchChange = useCallback((value: string) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        if (value) next.set('search', value);
        else next.delete('search');
        next.set('page', '1');
        return next;
      });
    }, 300);
  }, [setSearchParams]);

  const handlePriorityChange = (value: Priority | '') => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) next.set('priority', value);
      else next.delete('priority');
      next.set('page', '1');
      return next;
    });
  };

  const handlePageChange = (p: number) => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (p > 1) next.set('page', String(p));
      else next.delete('page');
      return next;
    });
  };

  const handleCreate = async () => {
    try {
      const values = await createForm.validateFields();
      // TODO: Call createCase mutation
      await createCase(values);
      message.success('用例创建成功');
      setCreateModalOpen(false);
      createForm.resetFields();
    } catch (error) {
      if (error instanceof Error) {
        message.error(error.message);
      }
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      ellipsis: true,
      render: (name: string, record: TestCase) => (
        <a onClick={() => navigate(`/cases/${record.id}`)}>{name}</a>
      ),
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 100,
      render: (priority: Priority) => {
        const colorMap: Record<Priority, string> = {
          P0: 'red',
          P1: 'orange',
          P2: 'blue',
          P3: 'default',
        };
        return <Tag color={colorMap[priority]}>{priority}</Tag>;
      },
    },
    {
      title: '分类',
      dataIndex: 'category_name',
      key: 'category_name',
      width: 150,
      ellipsis: true,
    },
    {
      title: '自动化',
      dataIndex: 'is_automated',
      key: 'is_automated',
      width: 100,
      render: (val: boolean) => (val ? <Tag color="green">是</Tag> : <Tag>否</Tag>),
    },
    {
      title: '平台',
      dataIndex: 'platform',
      key: 'platform',
      width: 100,
      render: (platform: Platform) => (
        <Tag>{platform === 'android' ? 'Android' : 'iOS'}</Tag>
      ),
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 180,
    },
    {
      title: '操作',
      key: 'actions',
      width: 80,
      render: (_: unknown, record: TestCase) => (
        <Button
          type="link"
          icon={<EditOutlined />}
          onClick={() => navigate(`/cases/${record.id}`)}
        />
      ),
    },
  ];

  return (
    <div>
      {/* Search & filter bar */}
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Space>
          <Input
            placeholder="搜索用例名称..."
            prefix={<SearchOutlined />}
            defaultValue={search}
            onChange={(e) => handleSearchChange(e.target.value)}
            style={{ width: 240 }}
            allowClear
          />
          <Select
            placeholder="优先级"
            value={priority || undefined}
            onChange={(val) => handlePriorityChange(val as Priority | '')}
            allowClear
            style={{ width: 120 }}
          >
            <Option value="P0">P0</Option>
            <Option value="P1">P1</Option>
            <Option value="P2">P2</Option>
            <Option value="P3">P3</Option>
          </Select>
        </Space>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setCreateModalOpen(true)}>
          新建用例
        </Button>
      </Space>

      {/* Error state */}
      {isError && (
        <Alert
          message="加载用例列表失败"
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      {/* Table */}
      <Table
        dataSource={data?.items}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        pagination={{
          current: page,
          pageSize: 20,
          total: data?.total ?? 0,
          onChange: handlePageChange,
          showSizeChanger: false,
          showTotal: (total) => `共 ${total} 条`,
        }}
        locale={{ emptyText: '暂无用例数据' }}
        size="middle"
      />

      {/* Create case modal */}
      <Modal
        title="新建用例"
        open={createModalOpen}
        onOk={handleCreate}
        onCancel={() => {
          setCreateModalOpen(false);
          createForm.resetFields();
        }}
        confirmLoading={isCreating}
        destroyOnClose
      >
        <Form form={createForm} layout="vertical">
          <Form.Item
            name="name"
            label="用例名称"
            rules={[{ required: true, message: '请输入用例名称' }]}
          >
            <Input placeholder="请输入用例名称" />
          </Form.Item>
          <Form.Item
            name="priority"
            label="优先级"
            rules={[{ required: true, message: '请选择优先级' }]}
          >
            <Select placeholder="请选择优先级">
              <Option value="P0">P0</Option>
              <Option value="P1">P1</Option>
              <Option value="P2">P2</Option>
              <Option value="P3">P3</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="platform"
            label="平台"
            rules={[{ required: true, message: '请选择平台' }]}
          >
            <Select placeholder="请选择平台">
              <Option value="android">Android</Option>
              <Option value="ios">iOS</Option>
            </Select>
          </Form.Item>
          <Form.Item name="is_automated" label="是否自动化" initialValue={false}>
            <Select>
              <Option value={true}>是</Option>
              <Option value={false}>否</Option>
            </Select>
          </Form.Item>
          <Form.Item name="category_id" label="分类">
            {/* TODO: Replace with TreeSelect from CategoryTree */}
            <Select placeholder="请选择分类">
              <Option value="">无</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CaseTable;
