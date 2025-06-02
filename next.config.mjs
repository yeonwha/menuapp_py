/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  allowedDevOrigins: [`${process.env.NEXT_PUBLIC_HOSTNAME}`]
};

export default nextConfig;
