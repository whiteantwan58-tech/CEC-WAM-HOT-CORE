# PSI Coin · Sovereign Quantum Logistics Token

[![PSI Coin Contract Tests](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/psi-coin-tests.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/psi-coin-tests.yml)
[![Secret Scanning](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/secret-scanning.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/secret-scanning.yml)
[![CodeQL](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/codeql.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-363636?logo=solidity)](https://soliditylang.org/)
[![Deploy Dashboard](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/deploy-dashboard.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/deploy-dashboard.yml)

> **🔒 Private Beta — By Invitation Only**
>
> PSI Coin is the native utility and governance token of the **CEC-WAM Sovereign Quantum Logistics Network** —
> a next-generation freight & supply-chain platform powered by quantum-inspired AI.
> Token holders stake PSI to unlock tiered freight discounts, participate in governance,
> and earn rewards through the logistics ecosystem.

---

## 🪙 Token Overview

| Property       | Value                                     |
|----------------|-------------------------------------------|
| **Name**       | PSI Coin                                  |
| **Symbol**     | PSI                                       |
| **Standard**   | ERC-20 (Solidity 0.8.20, OpenZeppelin 5)  |
| **Max Supply** | 1,000,000,000 PSI                         |
| **Presale**    | ❌ None — no presale                      |
| **Use-case**   | Freight staking · Governance · Discounts  |
| **Network**    | EVM-compatible (Ethereum / Polygon / L2)  |
| **License**    | MIT                                       |

---

## 📦 Staking Tiers — Freight Discounts

Stake PSI Coin to unlock freight cost reductions in the CEC-WAM logistics network.

| Tier       | Minimum Stake    | Freight Discount |
|------------|------------------|-----------------|
| 🥉 Bronze  | 10,000 PSI       | 5%              |
| 🥈 Silver  | 50,000 PSI       | 10%             |
| 🥇 Gold    | 250,000 PSI      | 20%             |
| ⚛️ Quantum | 1,000,000 PSI    | 35%             |

Staking has a **30-day lock period**. Tokens are returned in full on withdrawal.

---

## 🏗️ Repository Structure

```
CEC-WAM-HOT-CORE/
├── contracts/                      # Solidity smart contracts
│   ├── PSICoin.sol                 # ERC-20 token (mintable, burnable, pausable)
│   ├── PSICoinStaking.sol          # Freight-discount staking contract
│   ├── hardhat.config.js           # Hardhat configuration
│   ├── package.json                # Node dependencies (Hardhat + OpenZeppelin)
│   ├── scripts/
│   │   └── deploy.js               # Deployment script
│   └── test/
│       └── PSICoin.test.js         # Full contract test suite
├── index.html                      # PSI Coin public-facing dashboard (PWA)
├── dashboard.html                  # Standalone HTML logistics dashboard
├── app.py                          # Streamlit live-data app (EVE HEI core)
├── streamlit_app.py                # Alternate Streamlit entry point
├── eve_voice_agent.py              # EVE AI voice agent
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
├── .env.example                    # Environment variable template (no secrets)
├── .gitignore                      # Excludes secrets, node_modules, artifacts
└── .github/workflows/              # CI/CD pipelines
    ├── psi-coin-tests.yml          # Solidity contract tests
    ├── secret-scanning.yml         # Gitleaks secret detection
    ├── codeql.yml                  # CodeQL static analysis
    └── deploy-dashboard.yml        # GitHub Pages deployment
```

---

## 🚀 Quick Start — Contracts

```bash
git clone https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE.git
cd CEC-WAM-HOT-CORE/contracts
npm install
npm run compile          # Compile Solidity contracts
npm test                 # Run full test suite
npm run deploy:local     # Deploy to local Hardhat node
```

> **Keys stay offline.** Never commit private keys or RPC URLs.
> Configure deployment credentials in `.env` (see `.env.example`).

---

## 📊 Live Dashboard

The PSI Coin sovereign dashboard is available at:

🌐 **[https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/](https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/)**

Open `index.html` locally for a zero-dependency standalone experience.

---

## 🔐 Security

- **No secrets committed** — all keys and credentials are managed via `.env` (local) or cloud secrets.
- Gitleaks scans every push and pull request (`secret-scanning.yml`).
- CodeQL static analysis runs on every push to `main` (`codeql.yml`).
- See [SECURITY.md](./SECURITY.md) for the vulnerability disclosure policy.

---

## 📬 Contact & Private Beta

PSI Coin is in **private beta**. Access is by invitation only.

- **GitHub:** [https://github.com/whiteantwan58-tech](https://github.com/whiteantwan58-tech)
- **Repository:** [https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE)
- **For partnership & beta enquiries:** open an issue or contact via GitHub.

---

## 🤝 License

This project is licensed under the [MIT License](./LICENSE).

© 2026 CEC-WAM / PSI Coin — Sovereign Quantum Logistics

---

## ⚙️ CEC-WAM Platform (EVE HEI Core)

The contracts above power the on-chain layer of the broader CEC-WAM platform,
which includes a live logistics dashboard and the EVE HEI AI voice assistant.


