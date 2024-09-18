module.exports = {
    webpack: (config, { isServer }) => {
      if (!isServer) {
        config.resolve.fallback = {
          fs: false,
          net: false,
          tls: false,
          dns: false,
          child_process: false,
          dgram: false,
          module: false,
          http2: false
        };
      }
      return config;
    }
  };
  