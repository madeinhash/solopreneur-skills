import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false,
  images: {
  remotePatterns: [
    { protocol: 'https', hostname: '**' }
  ]
}
};

export default nextConfig;