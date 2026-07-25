import React, { useState } from 'react';
import { Row, Col, Card, Typography } from 'antd';
import CategoryTree from '@/components/CategoryTree';
import CaseTable from './CaseTable';

const { Title } = Typography;

/**
 * Cases management page with left category tree and right case table.
 * Selecting a category filters the displayed test cases.
 */
const CasesPage: React.FC = () => {
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | undefined>(undefined);

  return (
    <div>
      <Title level={4} style={{ marginBottom: 24 }}>
        用例管理
      </Title>

      <Row gutter={16}>
        {/* Left sidebar -- category tree */}
        <Col xs={24} sm={24} md={6} lg={5}>
          <Card title="分类筛选" size="small">
            <CategoryTree
              onSelect={(categoryId) => setSelectedCategoryId(categoryId)}
              selectedKeys={selectedCategoryId ? [selectedCategoryId] : ['all']}
            />
          </Card>
        </Col>

        {/* Main content -- case table */}
        <Col xs={24} sm={24} md={18} lg={19}>
          <Card>
            <CaseTable categoryId={selectedCategoryId} />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default CasesPage;
