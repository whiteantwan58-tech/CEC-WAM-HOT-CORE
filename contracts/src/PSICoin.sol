// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PSICoin
 * @notice PSI Coin — Sovereign Quantum Logistics Token
 * @dev ERC-20 token for the CEC-WAM freight & logistics ecosystem.
 *      No presale. Staking-based freight discounts via PSICoinStaking.sol.
 *      Symbol: PSI  |  Decimals: 18  |  Max Supply: 1,000,000,000 PSI
 *
 *      Contact: https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE
 *      Private Beta — invite only
 */
contract PSICoin is ERC20, ERC20Burnable, ERC20Pausable, Ownable {
    // ─── Constants ───────────────────────────────────────────────────────────
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10 ** 18; // 1 billion PSI

    // ─── Authorised minters (staking rewards, ecosystem grants) ──────────────
    mapping(address => bool) public minters;

    // ─── Events ──────────────────────────────────────────────────────────────
    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);

    // ─── Errors ──────────────────────────────────────────────────────────────
    error ExceedsMaxSupply(uint256 requested, uint256 available);
    error CallerIsNotMinter(address caller);

    // ─── Constructor ─────────────────────────────────────────────────────────
    /**
     * @param initialOwner Address that receives ownership and the genesis supply.
     * @param genesisSupply Tokens minted at deployment (must be <= MAX_SUPPLY).
     */
    constructor(address initialOwner, uint256 genesisSupply)
        ERC20("PSI Coin", "PSI")
        Ownable(initialOwner)
    {
        if (genesisSupply > MAX_SUPPLY) {
            revert ExceedsMaxSupply(genesisSupply, MAX_SUPPLY);
        }
        if (genesisSupply > 0) {
            _mint(initialOwner, genesisSupply);
        }
    }

    // ─── Minter management ───────────────────────────────────────────────────
    modifier onlyMinter() {
        if (!minters[msg.sender]) revert CallerIsNotMinter(msg.sender);
        _;
    }

    function addMinter(address account) external onlyOwner {
        minters[account] = true;
        emit MinterAdded(account);
    }

    function removeMinter(address account) external onlyOwner {
        minters[account] = false;
        emit MinterRemoved(account);
    }

    // ─── Minting ─────────────────────────────────────────────────────────────
    /**
     * @notice Mint tokens (staking rewards, ecosystem distribution).
     * @dev Only authorised minters or the owner may call this.
     *      Total supply is hard-capped at MAX_SUPPLY.
     */
    function mint(address to, uint256 amount) external {
        if (msg.sender != owner() && !minters[msg.sender]) {
            revert CallerIsNotMinter(msg.sender);
        }
        uint256 available = MAX_SUPPLY - totalSupply();
        if (amount > available) {
            revert ExceedsMaxSupply(amount, available);
        }
        _mint(to, amount);
    }

    // ─── Pause / Unpause ─────────────────────────────────────────────────────
    function pause() external onlyOwner { _pause(); }
    function unpause() external onlyOwner { _unpause(); }

    // ─── Overrides ───────────────────────────────────────────────────────────
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Pausable)
    {
        super._update(from, to, value);
    }
}
