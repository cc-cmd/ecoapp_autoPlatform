import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Card, Form, Input, Button, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuth } from '@/hooks/useAuth';
import type { LoginRequest } from '@/types';

const { Title } = Typography;

// ---------------------------------------------------------------------------
// Validation rules
// ---------------------------------------------------------------------------

const usernameRules = [
  { required: true, message: '请输入用户名' },
  { min: 3, message: '用户名至少3个字符' },
];

const passwordRules = [
  { required: true, message: '请输入密码' },
  { min: 8, message: '密码至少8个字符' },
  {
    pattern: /^(?=.*[a-zA-Z])(?=.*\d)/,
    message: '密码必须包含字母和数字',
  },
];

// ---------------------------------------------------------------------------
// LoginPage
// ---------------------------------------------------------------------------

/**
 * Login page with centered card layout.
 * Calls useAuth().login() and redirects to /dashboard on success.
 */
const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm<LoginRequest>();

  const handleSubmit = async (values: LoginRequest) => {
    setLoading(true);
    try {
      // TODO: Implement actual login API call
      await authLogin(values);
      message.success('登录成功');
      navigate('/dashboard', { replace: true });
    } catch (error: unknown) {
      // TODO: Handle specific error codes from API
      const errMsg = error instanceof Error ? error.message : '登录失败，请检查用户名和密码';
      message.error(errMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: '#f0f2f5',
      }}
    >
      <Card style={{ width: 400, boxShadow: '0 2px 8px rgba(0,0,0,0.09)' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <Title level={3}>EcoFlow 自动化测试平台</Title>
          <Title level={5} type="secondary">
            请登录以继续
          </Title>
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          autoComplete="off"
          requiredMark={false}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={usernameRules}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="请输入用户名"
              size="large"
              autoFocus
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="密码"
            rules={passwordRules}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请输入密码"
              size="large"
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 8 }}>
            <Button type="primary" htmlType="submit" loading={loading} block size="large">
              登录
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Link to="/register">没有账号？去注册</Link>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default LoginPage;
