require("@nomicfoundation/hardhat-toolbox");

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
    // Production networks — set RPC URLs and private keys in .env (never commit)
    // mainnet: { url: process.env.MAINNET_RPC_URL, accounts: [process.env.DEPLOYER_PRIVATE_KEY] },
    // polygon: { url: process.env.POLYGON_RPC_URL, accounts: [process.env.DEPLOYER_PRIVATE_KEY] },
  },
  paths: {
    sources: "./",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};
