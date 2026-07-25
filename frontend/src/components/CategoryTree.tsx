import React, { useMemo } from 'react';
import { Tree, Spin } from 'antd';
import type { DataNode } from 'antd/es/tree';
import { useCategoryTree } from '@/hooks/useCategories';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CategoryTreeProps {
  /** Callback when a tree node is selected. */
  onSelect?: (categoryId: string | undefined) => void;
  /** Currently selected category keys. */
  selectedKeys?: string[];
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Transforms API category tree nodes into Ant Design Tree DataNode format.
 */
function buildTreeData(nodes: import('@/types').CategoryTreeNode[]): DataNode[] {
  return nodes.map((node) => ({
    key: node.id,
    title: node.name,
    children: node.children && node.children.length > 0 ? buildTreeData(node.children) : undefined,
  }));
}

// ---------------------------------------------------------------------------
// CategoryTree
// ---------------------------------------------------------------------------

/**
 * Category tree component with "全部用例" root node.
 * Wraps Ant Design Tree for test case category navigation.
 */
const CategoryTree: React.FC<CategoryTreeProps> = ({ onSelect, selectedKeys }) => {
  const { data: categories, isLoading } = useCategoryTree();

  const treeData = useMemo<DataNode[]>(() => {
    if (!categories) return [];
    const rootNode: DataNode = {
      key: 'all',
      title: '全部用例',
      children: buildTreeData(categories),
    };
    return [rootNode];
  }, [categories]);

  const handleSelect = (keys: React.Key[]) => {
    const key = keys[0] as string | undefined;
    // 'all' means no category filter
    onSelect?.(key === 'all' ? undefined : key);
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: 24 }}>
        <Spin size="small" />
      </div>
    );
  }

  return (
    <Tree
      showLine
      defaultExpandAll
      treeData={treeData}
      selectedKeys={selectedKeys}
      onSelect={handleSelect}
    />
  );
};

export default CategoryTree;
