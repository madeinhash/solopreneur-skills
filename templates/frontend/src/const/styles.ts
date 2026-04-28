// src/const/styles.ts

// Colors
export const COLORS = {
  primary: '#1890ff',
  success: '#52c41a',
  warning: '#faad14',
  error: '#ff4d4f',
} as const;

// Common button styles
export const BUTTON_STYLES = {
  primary: {
    background: COLORS.primary,
    border: 'none',
    color: 'white',
  } as React.CSSProperties,
} as const;
