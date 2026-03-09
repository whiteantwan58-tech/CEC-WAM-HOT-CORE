const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying PSI Coin contracts with account:", deployer.address);
  console.log("Account balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "ETH");

  // ── Deploy PSICoin ────────────────────────────────────────────────────────
  // Genesis supply: 100 million PSI (10% of max supply)
  const genesisSupply = ethers.parseEther("100000000");

  const PSICoin = await ethers.getContractFactory("PSICoin");
  const psiCoin = await PSICoin.deploy(deployer.address, genesisSupply);
  await psiCoin.waitForDeployment();

  const psiCoinAddress = await psiCoin.getAddress();
  console.log("PSICoin deployed to:", psiCoinAddress);

  // ── Deploy PSICoinStaking ─────────────────────────────────────────────────
  const PSICoinStaking = await ethers.getContractFactory("PSICoinStaking");
  const staking = await PSICoinStaking.deploy(psiCoinAddress, deployer.address);
  await staking.waitForDeployment();

  const stakingAddress = await staking.getAddress();
  console.log("PSICoinStaking deployed to:", stakingAddress);

  console.log("\n✅ Deployment complete.");
  console.log("  PSICoin   :", psiCoinAddress);
  console.log("  Staking   :", stakingAddress);
  console.log("\n⚠️  Save these addresses. Add them to your .env file (never commit .env).");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
