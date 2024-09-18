const { withExpo } = require("@expo/next-adapter");
const withTM = require("next-transpile-modules")([
  "react-native-web",
  "react-native-url-polyfill"
]);

module.exports = withTM(
  withExpo({
    projectRoot: __dirname,
  })
);
