// src/lib/Fontawesome.tsx
import { config } from '@fortawesome/fontawesome-svg-core';
import '@fortawesome/fontawesome-svg-core/styles.css';

// 告诉 Font Awesome 不要自动添加 CSS，因为我们手动导入了
config.autoAddCss = false;

// 使用免费版图标:
// - @fortawesome/free-solid-svg-icons (实心图标)
// - @fortawesome/free-regular-svg-icons (线框图标)
// - @fortawesome/free-brands-svg-icons (品牌图标)
//
// 使用示例:
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faUser } from '@fortawesome/free-solid-svg-icons';
// <FontAwesomeIcon icon={faUser} />
