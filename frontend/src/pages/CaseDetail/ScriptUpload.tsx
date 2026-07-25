import React from 'react';
import { Upload, Button, message } from 'antd';
import { DownloadOutlined, InboxOutlined } from '@ant-design/icons';
import { useUploadScript } from '@/hooks/useCases';
import type { UploadProps } from 'antd';

const { Dragger } = Upload;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScriptUploadProps {
  /** Test case ID. */
  caseId: string;
  /** Existing script path (if any). */
  scriptPath?: string;
}

// ---------------------------------------------------------------------------
// ScriptUpload
// ---------------------------------------------------------------------------

/**
 * Script upload area (Dragger) for .py files, plus download button for existing scripts.
 */
const ScriptUpload: React.FC<ScriptUploadProps> = ({ caseId, scriptPath }) => {
  const { mutateAsync: uploadScript, isPending: isUploading } = useUploadScript();

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    accept: '.py',
    showUploadList: false,
    customRequest: async (options) => {
      const { file, onSuccess, onError } = options;
      try {
        // TODO: Call uploadScript mutation
        await uploadScript({ id: caseId, file: file as File });
        message.success('脚本上传成功');
        onSuccess?.(null);
      } catch (error) {
        const errMsg = error instanceof Error ? error.message : '上传失败';
        message.error(errMsg);
        onError?.(new Error(errMsg));
      }
    },
  };

  const handleDownload = () => {
    // TODO: Implement script download via API
    message.info('下载功能待实现');
  };

  return (
    <div>
      <Dragger {...uploadProps} disabled={isUploading}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">点击或拖拽 .py 文件到此区域上传</p>
        <p className="ant-upload-hint">仅支持 Python 脚本文件 (.py)</p>
      </Dragger>

      {scriptPath && (
        <div style={{ marginTop: 12 }}>
          <span style={{ marginRight: 12, color: '#888' }}>已上传: {scriptPath}</span>
          <Button icon={<DownloadOutlined />} onClick={handleDownload}>
            下载脚本
          </Button>
        </div>
      )}
    </div>
  );
};

export default ScriptUpload;
