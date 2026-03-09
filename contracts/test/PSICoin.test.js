const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PSICoin", function () {
  let psiCoin, owner, addr1, addr2;
  const MAX_SUPPLY = ethers.parseEther("1000000000"); // 1B PSI
  const GENESIS = ethers.parseEther("100000000");     // 100M PSI genesis

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    const PSICoin = await ethers.getContractFactory("PSICoin");
    psiCoin = await PSICoin.deploy(owner.address, GENESIS);
  });

  it("has correct name and symbol", async function () {
    expect(await psiCoin.name()).to.equal("PSI Coin");
    expect(await psiCoin.symbol()).to.equal("PSI");
  });

  it("mints genesis supply to owner", async function () {
    expect(await psiCoin.balanceOf(owner.address)).to.equal(GENESIS);
  });

  it("respects MAX_SUPPLY cap", async function () {
    const remaining = MAX_SUPPLY - GENESIS;
    await expect(psiCoin.mint(addr1.address, remaining + 1n)).to.be.reverted;
  });

  it("allows owner to add a minter", async function () {
    await psiCoin.addMinter(addr1.address);
    expect(await psiCoin.minters(addr1.address)).to.be.true;
  });

  it("allows minter to mint within cap", async function () {
    await psiCoin.addMinter(addr1.address);
    const amount = ethers.parseEther("1000");
    await psiCoin.connect(addr1).mint(addr2.address, amount);
    expect(await psiCoin.balanceOf(addr2.address)).to.equal(amount);
  });

  it("blocks non-minter from minting", async function () {
    await expect(
      psiCoin.connect(addr1).mint(addr2.address, ethers.parseEther("1"))
    ).to.be.reverted;
  });

  it("allows owner to pause and unpause transfers", async function () {
    await psiCoin.pause();
    await expect(
      psiCoin.transfer(addr1.address, ethers.parseEther("1"))
    ).to.be.reverted;

    await psiCoin.unpause();
    await psiCoin.transfer(addr1.address, ethers.parseEther("1"));
    expect(await psiCoin.balanceOf(addr1.address)).to.equal(ethers.parseEther("1"));
  });

  it("allows burning tokens", async function () {
    const burnAmount = ethers.parseEther("500");
    await psiCoin.burn(burnAmount);
    expect(await psiCoin.totalSupply()).to.equal(GENESIS - burnAmount);
  });
});

describe("PSICoinStaking", function () {
  let psiCoin, staking, owner, user1, user2;
  const GENESIS = ethers.parseEther("10000000"); // 10M PSI

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();

    const PSICoin = await ethers.getContractFactory("PSICoin");
    psiCoin = await PSICoin.deploy(owner.address, GENESIS);

    const PSICoinStaking = await ethers.getContractFactory("PSICoinStaking");
    staking = await PSICoinStaking.deploy(await psiCoin.getAddress(), owner.address);

    // Fund user1 with 500k PSI
    await psiCoin.transfer(user1.address, ethers.parseEther("500000"));
    await psiCoin.connect(user1).approve(await staking.getAddress(), ethers.MaxUint256);
  });

  it("allows a user to stake PSI", async function () {
    const amount = ethers.parseEther("50000");
    await staking.connect(user1).stake(amount);
    const s = await staking.stakes(user1.address);
    expect(s.amount).to.equal(amount);
  });

  it("returns correct tier for staked amount", async function () {
    await staking.connect(user1).stake(ethers.parseEther("50000"));
    const [, discountBps, tierName] = await staking.getDiscount(user1.address);
    expect(discountBps).to.equal(1000); // Silver = 10%
    expect(tierName).to.equal("Silver");
  });

  it("returns Gold tier for 250k stake", async function () {
    await staking.connect(user1).stake(ethers.parseEther("250000"));
    const [, discountBps, tierName] = await staking.getDiscount(user1.address);
    expect(discountBps).to.equal(2000); // Gold = 20%
    expect(tierName).to.equal("Gold");
  });

  it("prevents unstaking before lock period", async function () {
    await staking.connect(user1).stake(ethers.parseEther("10000"));
    await expect(staking.connect(user1).unstake()).to.be.reverted;
  });

  it("allows unstaking after lock period", async function () {
    const amount = ethers.parseEther("10000");
    await staking.connect(user1).stake(amount);

    // Fast-forward 31 days
    await ethers.provider.send("evm_increaseTime", [31 * 24 * 60 * 60]);
    await ethers.provider.send("evm_mine", []);

    const balBefore = await psiCoin.balanceOf(user1.address);
    await staking.connect(user1).unstake();
    const balAfter = await psiCoin.balanceOf(user1.address);
    expect(balAfter - balBefore).to.equal(amount);
  });

  it("returns None tier for unstaked address", async function () {
    const [, discountBps, tierName] = await staking.getDiscount(user2.address);
    expect(discountBps).to.equal(0);
    expect(tierName).to.equal("None");
  });
});
