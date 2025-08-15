/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: "export",
  trailingSlash: true,
  distDir: "out",
  images: {
    unoptimized: true,
    domains: ["localhost"],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
};

module.exports = nextConfig;
