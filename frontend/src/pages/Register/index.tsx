import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Card, Form, Input, Button, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { isAxiosError } from 'axios';
import { useAuth } from '@/hooks/useAuth';
import type { RegisterRequest } from '@/types';

const { Title } = Typography;

// ---------------------------------------------------------------------------
// Validation rules
// ---------------------------------------------------------------------------

const usernameRules = [
  { required: true, message: '请输入用户名' },
  { min: 3, message: '用户名至少3个字符' },
  { max: 64, message: '用户名最多64个字符' },
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
// RegisterPage
// ---------------------------------------------------------------------------

/**
 * Register page with centered card layout.
 * Calls useAuth().register() and shows a link to login on success.
 * Per PRD-01: registration does NOT auto-login the user.
 */
const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register: authRegister } = useAuth();
  const [loading, setLoading] = useState(false);
  const [registered, setRegistered] = useState(false);
  const [form] = Form.useForm<RegisterRequest & { confirmPassword: string }>();

  const handleSubmit = async ({ username, password }: RegisterRequest) => {
    setLoading(true);
    try {
      await authRegister({ username, password });
      setRegistered(true);
      message.success('注册成功！请前往登录');
    } catch (error: unknown) {
      if (isAxiosError(error) && error.response?.data?.message) {
        message.error(error.response.data.message);
      } else {
        message.error('注册失败，请稍后重试');
      }
    } finally {
      setLoading(false);
    }
  };

  if (registered) {
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
        <Card style={{ width: 400, boxShadow: '0 2px 8px rgba(0,0,0,0.09)', textAlign: 'center' }}>
          <Title level={4} style={{ color: '#52c41a' }}>注册成功！</Title>
          <p style={{ marginBottom: 24, color: '#666' }}>
            您的账号已创建，请前往登录页面进行登录。
          </p>
          <Button type="primary" size="large" block onClick={() => navigate('/login')}>
            去登录
          </Button>
        </Card>
      </div>
    );
  }

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
            创建新账号
          </Title>
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          requiredMark={false}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={usernameRules}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="请输入用户名（3-64字符）"
              size="large"
              autoFocus
              disabled={loading}
              autoComplete="username"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="密码"
            rules={passwordRules}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请输入密码（至少8位，含字母和数字）"
              autoComplete="new-password"
              size="large"
              disabled={loading}
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            label="确认密码"
            dependencies={['password']}
            rules={[
              { required: true, message: '请再次输入密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请再次输入密码"
              size="large"
              disabled={loading}
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 8 }}>
            <Button type="primary" htmlType="submit" loading={loading} block size="large">
              注册
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            已有账号？<Link to="/login">去登录</Link>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default RegisterPage;
