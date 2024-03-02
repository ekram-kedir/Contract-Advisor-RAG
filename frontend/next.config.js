/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
      },
    ],
  },
  reactStrictMode: true,
  images: {
    domains: ['res.cloudinary.com', 'picsum.photos']
  }
};

module.exports = {
  ...nextConfig,
  reactStrictMode: true,
  productionBrowserSourceMaps: true
};
