import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Typography, Spin, Button, Result } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useCase } from '@/hooks/useCases';
import CaseForm from './CaseForm';
import ScriptUpload from './ScriptUpload';
import RunHistory from './RunHistory';

const { Title } = Typography;

/**
 * Test case detail page with case form, script upload, and execution history.
 * Uses case ID from route params.
 */
const CaseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: caseData, isLoading, isError } = useCase(id!);

  if (!id) {
    return <div>无效的用例 ID</div>;
  }

  if (isError) {
    return (
      <Result
        status="error"
        title="加载用例详情失败"
        subTitle="请检查用例 ID 是否正确或刷新页面重试"
        extra={
          <Button type="primary" onClick={() => navigate('/cases')}>
            返回用例列表
          </Button>
        }
      />
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 24 }}>
        <Button
          type="text"
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/cases')}
          style={{ marginRight: 12 }}
        >
          返回
        </Button>
        <Title level={4} style={{ margin: 0 }}>用例详情</Title>
      </div>

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: 48 }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          {/* Case form */}
          <Card title="基本信息" style={{ marginBottom: 16 }}>
            <CaseForm caseData={caseData} loading={isLoading} />
          </Card>

          {/* Script upload */}
          <Card title="脚本管理" style={{ marginBottom: 16 }}>
            <ScriptUpload caseId={id} scriptPath={caseData?.script_path} />
          </Card>

          {/* Run history */}
          <Card title="执行历史">
            <RunHistory caseId={id} />
          </Card>
        </>
      )}
    </div>
  );
};

export default CaseDetailPage;
