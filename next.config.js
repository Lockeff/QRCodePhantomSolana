const { withExpo } = require("@expo/next-adapter");
const withTM = require("next-transpile-modules")([
  "react-native-web",
  "react-native-url-polyfill"
]);

module.exports = withTM(
  withExpo({
    projectRoot: __dirname,
    webpack: (config, { isServer }) => {
      if (!isServer) {
        config.resolve.fallback = {
          fs: false,
          module: false,
          dgram: false,
          dns: false,
          net: false,
          tls: false,
          child_process: false
        };
      }
      return config;
    }
  })
);
