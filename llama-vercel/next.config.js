/** @type {import('next').NextConfig} */
// Configuración principal de Next.js para el proyecto
const nextConfig = {
  webpack: (config) => {
    // Configuración de alias para evitar ciertos módulos en el bundle
    // Ver más en https://webpack.js.org/configuration/resolve/#resolvealias
    config.resolve.alias = {
      ...config.resolve.alias,
      sharp$: false,
      "onnxruntime-node$": false,
      mongodb$: false,
    };
    return config;
  },
  experimental: {
    // Permite incluir paquetes externos en los server components
    serverComponentsExternalPackages: ["llamaindex"],
    outputFileTracingIncludes: {
      "/*": ["./cache/**/*"],
    },
  },
};

module.exports = nextConfig;
