// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PSICoinStaking
 * @notice Stake PSI Coin to earn freight discounts in the CEC-WAM logistics network.
 * @dev Discount tiers are determined by the amount of PSI staked.
 *      No presale. Stakers unlock freight cost reductions as a governance benefit.
 *
 *      Tier structure (adjustable by owner):
 *        Bronze  — ≥   10 000 PSI →  5 % freight discount
 *        Silver  — ≥   50 000 PSI → 10 % freight discount
 *        Gold    — ≥  250 000 PSI → 20 % freight discount
 *        Quantum — ≥ 1 000 000 PSI → 35 % freight discount
 *
 *      Contact: https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE
 */
contract PSICoinStaking is ReentrancyGuard, Ownable {
    using SafeERC20 for IERC20;

    // ─── State ────────────────────────────────────────────────────────────────
    IERC20 public immutable psiToken;

    struct Stake {
        uint256 amount;      // PSI staked (18 decimals)
        uint256 stakedAt;    // block.timestamp of stake
        uint256 unlocksAt;   // earliest withdrawal timestamp
    }

    mapping(address => Stake) public stakes;
    uint256 public totalStaked;

    // ─── Discount tiers ──────────────────────────────────────────────────────
    struct Tier {
        uint256 minStake;      // minimum PSI (18 dec) for this tier
        uint16  discountBps;   // discount in basis points (500 = 5 %, max 65535)
        string  name;
    }

    Tier[] public tiers;

    // ─── Lock period (default: 30 days) ──────────────────────────────────────
    uint256 public lockPeriod = 30 days;

    // ─── Events ──────────────────────────────────────────────────────────────
    event Staked(address indexed user, uint256 amount, uint256 unlocksAt);
    event Unstaked(address indexed user, uint256 amount);
    event TierUpdated(uint256 indexed index, uint256 minStake, uint16 discountBps, string name);
    event LockPeriodUpdated(uint256 newLockPeriod);

    // ─── Errors ──────────────────────────────────────────────────────────────
    error ZeroAmount();
    error AlreadyStaking();
    error NothingStaked();
    error StillLocked(uint256 unlocksAt);
    error InvalidTierIndex();

    // ─── Constructor ─────────────────────────────────────────────────────────
    constructor(address _psiToken, address initialOwner) Ownable(initialOwner) {
        psiToken = IERC20(_psiToken);

        // Initialise default tiers
        tiers.push(Tier({ minStake:      10_000 * 1e18, discountBps:  500, name: "Bronze"  }));
        tiers.push(Tier({ minStake:      50_000 * 1e18, discountBps: 1000, name: "Silver"  }));
        tiers.push(Tier({ minStake:     250_000 * 1e18, discountBps: 2000, name: "Gold"    }));
        tiers.push(Tier({ minStake:   1_000_000 * 1e18, discountBps: 3500, name: "Quantum" }));
    }

    // ─── Staking ─────────────────────────────────────────────────────────────
    /**
     * @notice Stake PSI to unlock a freight discount tier.
     * @param amount Amount of PSI (in wei) to stake. Must be > 0.
     */
    function stake(uint256 amount) external nonReentrant {
        if (amount == 0) revert ZeroAmount();
        if (stakes[msg.sender].amount > 0) revert AlreadyStaking();

        psiToken.safeTransferFrom(msg.sender, address(this), amount);

        uint256 unlock = block.timestamp + lockPeriod;
        stakes[msg.sender] = Stake({ amount: amount, stakedAt: block.timestamp, unlocksAt: unlock });
        totalStaked += amount;

        emit Staked(msg.sender, amount, unlock);
    }

    /**
     * @notice Add more PSI to an existing stake, resetting the lock period.
     */
    function addStake(uint256 amount) external nonReentrant {
        if (amount == 0) revert ZeroAmount();
        if (stakes[msg.sender].amount == 0) revert NothingStaked();

        psiToken.safeTransferFrom(msg.sender, address(this), amount);

        stakes[msg.sender].amount += amount;
        stakes[msg.sender].unlocksAt = block.timestamp + lockPeriod;
        totalStaked += amount;

        emit Staked(msg.sender, amount, stakes[msg.sender].unlocksAt);
    }

    /**
     * @notice Withdraw all staked PSI after the lock period expires.
     */
    function unstake() external nonReentrant {
        Stake memory s = stakes[msg.sender];
        if (s.amount == 0) revert NothingStaked();
        if (block.timestamp < s.unlocksAt) revert StillLocked(s.unlocksAt);

        uint256 amount = s.amount;
        delete stakes[msg.sender];
        totalStaked -= amount;

        psiToken.safeTransfer(msg.sender, amount);
        emit Unstaked(msg.sender, amount);
    }

    // ─── View helpers ────────────────────────────────────────────────────────
    /**
     * @notice Returns the discount tier for a given staker address.
     * @return tierIndex Index into the `tiers` array (-1 cast to uint256 means no tier).
     * @return discountBps Discount in basis points (0 if no tier qualifies).
     * @return tierName Name of the tier ("None" if not qualifying).
     */
    function getDiscount(address user)
        external
        view
        returns (uint256 tierIndex, uint16 discountBps, string memory tierName)
    {
        uint256 staked = stakes[user].amount;
        // Iterate tiers in descending order to find highest qualifying tier
        for (uint256 i = tiers.length; i > 0; ) {
            unchecked { --i; }
            if (staked >= tiers[i].minStake) {
                return (i, tiers[i].discountBps, tiers[i].name);
            }
        }
        return (type(uint256).max, 0, "None");
    }

    /**
     * @notice Returns the number of discount tiers.
     */
    function tierCount() external view returns (uint256) {
        return tiers.length;
    }

    // ─── Admin ───────────────────────────────────────────────────────────────
    function updateTier(uint256 index, uint256 minStake, uint16 discountBps, string calldata name)
        external
        onlyOwner
    {
        if (index >= tiers.length) revert InvalidTierIndex();
        tiers[index] = Tier({ minStake: minStake, discountBps: discountBps, name: name });
        emit TierUpdated(index, minStake, discountBps, name);
    }

    function addTier(uint256 minStake, uint16 discountBps, string calldata name)
        external
        onlyOwner
    {
        tiers.push(Tier({ minStake: minStake, discountBps: discountBps, name: name }));
        emit TierUpdated(tiers.length - 1, minStake, discountBps, name);
    }

    function setLockPeriod(uint256 newLockPeriod) external onlyOwner {
        lockPeriod = newLockPeriod;
        emit LockPeriodUpdated(newLockPeriod);
    }
}
