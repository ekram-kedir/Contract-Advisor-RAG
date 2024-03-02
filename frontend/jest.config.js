module.exports = {
  preset: "ts-jest",
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
  testPathIgnorePatterns: [
    "<rootDir>/.next/",
    "<rootDir>/node_modules/",
    "<rootDir>/__tests__/mocks/",
  ],
  moduleNameMapper: {
    "^@/(.*)": "<rootDir>/$1",
    "\\.(css)$": "identity-obj-proxy",
  },
  transform: {
    "^.+\\.(ts|tsx|js|jsx)$": "babel-jest",
    "\\.(jpg|jpeg|png|gif|svg)$": "<rootDir>/mockTransform.js",
  },
  testEnvironment: "jsdom",
};
