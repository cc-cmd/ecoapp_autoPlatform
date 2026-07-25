import React, { useEffect } from 'react';
import { Form, Input, Select, Button, Space, Spin, message } from 'antd';
import type { TestCase, UpdateCaseRequest } from '@/types';
import { useUpdateCase } from '@/hooks/useCases';

const { TextArea } = Input;
const { Option } = Select;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CaseFormProps {
  /** The test case to edit. */
  caseData?: TestCase;
  /** Whether data is still loading. */
  loading?: boolean;
}

// ---------------------------------------------------------------------------
// CaseForm
// ---------------------------------------------------------------------------

/**
 * Form for viewing and editing test case metadata.
 * Fields: name, priority, platform, category, steps.
 */
const CaseForm: React.FC<CaseFormProps> = ({ caseData, loading = false }) => {
  const [form] = Form.useForm<UpdateCaseRequest>();
  const { mutateAsync: updateCase, isPending: isUpdating } = useUpdateCase();

  // Populate form when caseData changes
  useEffect(() => {
    if (caseData) {
      form.setFieldsValue({
        name: caseData.name,
        priority: caseData.priority,
        platform: caseData.platform,
        is_automated: caseData.is_automated,
        steps: caseData.steps,
      });
    }
  }, [caseData, form]);

  const handleSave = async () => {
    if (!caseData) return;

    try {
      const values = await form.validateFields();
      // TODO: Call updateCase mutation
      await updateCase({ id: caseData.id, data: values });
      message.success('保存成功');
    } catch (error) {
      if (error instanceof Error) {
        message.error(error.message);
      }
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <Form form={form} layout="vertical" disabled={!caseData}>
      <Form.Item
        name="name"
        label="用例名称"
        rules={[{ required: true, message: '请输入用例名称' }]}
      >
        <Input placeholder="请输入用例名称" />
      </Form.Item>

      <Space style={{ width: '100%' }} size={16}>
        <Form.Item
          name="priority"
          label="优先级"
          rules={[{ required: true, message: '请选择优先级' }]}
          style={{ width: 200 }}
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
          style={{ width: 200 }}
        >
          <Select placeholder="请选择平台">
            <Option value="android">Android</Option>
            <Option value="ios">iOS</Option>
          </Select>
        </Form.Item>

        <Form.Item name="is_automated" label="是否自动化" style={{ width: 200 }}>
          <Select>
            <Option value={true}>是</Option>
            <Option value={false}>否</Option>
          </Select>
        </Form.Item>
      </Space>

      <Form.Item name="steps" label="测试步骤">
        <TextArea rows={6} placeholder="请输入测试步骤，每行一步" />
      </Form.Item>

      <Form.Item>
        <Button type="primary" onClick={handleSave} loading={isUpdating}>
          保存
        </Button>
      </Form.Item>
    </Form>
  );
};

export default CaseForm;
