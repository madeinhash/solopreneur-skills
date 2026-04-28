// src/lib/AntdRegistry.tsx
'use client';

import React from 'react';
import { StyleProvider } from '@ant-design/cssinjs';
import { ConfigProvider, App } from 'antd';
import 'antd/dist/reset.css';

export default function AntdRegistry({ children }: { children: React.ReactNode }) {
  return (
    <StyleProvider hashPriority="high">
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#718096', // 主色改为灰色
            borderRadius: 8,
            fontFamily: 'inherit', // 字体继承
          },
          components: {
            Button: {
              controlHeight: 32,
              controlHeightLG: 40,
              controlHeightSM: 24,
            },
          },
        }}
      >
        <App>{children}</App>
      </ConfigProvider>
    </StyleProvider>
  );
}