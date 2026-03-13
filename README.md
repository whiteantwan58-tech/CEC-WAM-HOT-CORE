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
├── contracts/                      # Solidity smart contracts (Hardhat project)
│   ├── src/
│   │   ├── PSICoin.sol             # ERC-20 token (mintable, burnable, pausable)
│   │   └── PSICoinStaking.sol      # Freight-discount staking contract
│   ├── hardhat.config.js           # Hardhat configuration (dotenv-aware)
│   ├── package.json                # Node dependencies (Hardhat + OpenZeppelin)
│   ├── package-lock.json           # Locked dependency tree for reproducible CI
│   ├── scripts/
│   │   └── deploy.js               # Deployment script
│   └── test/
│       └── PSICoin.test.js         # Full contract test suite
├── index.html                      # PSI Coin public-facing dashboard (PWA + WebAuthn)
├── dashboard.html                  # Standalone HTML logistics dashboard
├── js/
│   └── encrypt.js                  # WebCrypto AES-GCM local encryption utility
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

## 🔑 Environment Variables

All sensitive credentials are managed via environment variables — **never committed to the repo**.

### Local Development

```bash
# 1. Copy the template
cp .env.example .env

# 2. Open .env and fill in your actual values
#    (NEVER commit the .env file — it is already in .gitignore)
```

Key variables (see `.env.example` for the full list):

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key (from platform.openai.com) |
| `ELEVENLABS_API_KEY` | ElevenLabs voice synthesis key |
| `GROQ_API_KEY` | Groq inference key |
| `GOOGLE_SHEETS_URL` | Published CSV URL for live logistics data |
| `EVE_SYSTEM_CODE` | EVE agent identity code |

### Cloud / CI Secrets

For Streamlit Cloud, GitHub Actions, or any other host, set each variable in the
host's **Secrets / Environment Variables** settings panel — never in a file that
gets committed.

- **Streamlit Cloud:** App Settings → Secrets (uses TOML syntax: `KEY = "value"`, not `.env` format)
- **GitHub Actions:** Repository Settings → Secrets and Variables → Actions
- **Railway / Render / Fly.io:** Dashboard → Environment → Add Variable

### Optional: Local Encryption Utility

`js/encrypt.js` provides an AES-GCM 256-bit helper (WebCrypto, no dependencies)
for encrypting sensitive strings before storing them in `localStorage`/IndexedDB.
**Keys are never stored** — you supply the passphrase on each call.

```javascript
// Encrypt a value:
const { ciphertext, iv, salt } = await CecCrypto.encrypt('my-api-key', 'my-passphrase');

// Decrypt later:
const plaintext = await CecCrypto.decrypt(ciphertext, iv, salt, 'my-passphrase');
```

> ⚠️ Requires a **secure context** (HTTPS or `localhost`). See `js/encrypt.js` for full docs.

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


