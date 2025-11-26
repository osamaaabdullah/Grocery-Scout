import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "i5.walmartimages.com",
      },
      {
        protocol: "https",
        hostname: "i5.walmartimages.ca",
      },
      {
        protocol: "https",
        hostname: "product-images.metro.ca",
      },
      {
        protocol: "https",
        hostname: "digital.loblaws.ca",
      },
      {
        protocol: "https",
        hostname: "assets.loblaws.ca",
      }
    ],
    localPatterns: [
      {
        pathname: "/no_image.webp",
      },
    ],
  },
};

export default nextConfig;
