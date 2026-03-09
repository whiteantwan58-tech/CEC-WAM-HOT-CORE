require("@nomicfoundation/hardhat-toolbox");

// Load .env so MAINNET_RPC_URL / DEPLOYER_PRIVATE_KEY are available when
// production network blocks are uncommented. The try/catch means the config
// still loads cleanly when dotenv is not installed (e.g., fresh CI checkout
// before `npm ci`).
try {
  require("dotenv").config();
} catch (_) {}

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {},
    localhost: {
      url: "http://127.0.0.1:8545",
    },
    // Uncomment and set MAINNET_RPC_URL + DEPLOYER_PRIVATE_KEY in .env to deploy
    // mainnet: {
    //   url: process.env.MAINNET_RPC_URL || "",
    //   accounts: process.env.DEPLOYER_PRIVATE_KEY ? [process.env.DEPLOYER_PRIVATE_KEY] : [],
    // },
    // polygon: {
    //   url: process.env.POLYGON_RPC_URL || "",
    //   accounts: process.env.DEPLOYER_PRIVATE_KEY ? [process.env.DEPLOYER_PRIVATE_KEY] : [],
    // },
  },
  paths: {
    sources: "./src",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};
