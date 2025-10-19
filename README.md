<div align="center">

# 🏦 TrustLens

**On-Chain Credit Scoring & DeFi Lending on Algorand**

[![Algorand](https://img.shields.io/badge/Algorand-TestNet-00D1B2?style=for-the-badge&logo=algorand)](https://testnet.algoexplorer.io/application/748013252)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PyTeal](https://img.shields.io/badge/Smart_Contract-PyTeal-7B3FF2?style=for-the-badge)](https://pyteal.readthedocs.io/)

![TrustLens Dashboard](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.32.29.png)

**Democratizing DeFi Lending through Transparent On-Chain Credit Scoring**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#%EF%B8%8F-architecture) • [API Docs](#-api-endpoints) • [Contributing](#-contributing)

</div>

---

## 🎯 What is TrustLens?

TrustLens is a **decentralized lending platform** built on Algorand that revolutionizes DeFi by introducing **fair, transparent credit scoring**. Unlike traditional DeFi protocols that treat all users equally, TrustLens analyzes on-chain behavior to reward responsible users with better loan terms.

### Key Innovation

- **📊 7-Factor On-Chain Credit Score**: FICO-like scoring (0-850) based on wallet analytics
- **💰 Dynamic LTV Ratios**: 60-75% loan-to-value based on creditworthiness and market conditions
- **🛡️ DeFi Stability Layer**: Real-time volatility monitoring + oracle anomaly detection
- **📄 Document Verification**: Cryptographic signatures for +400 credit boost
- **🏦 Smart Contract Lending**: Fully on-chain deposit, borrow, repay, withdraw, liquidate
- **🎓 Educational UI**: 20+ interactive tooltips explaining DeFi concepts

### The Problem We Solve

| Traditional DeFi | TrustLens |
|-----------------|-----------|
| Fixed 50% LTV for everyone | Dynamic 60-75% LTV based on credit |
| No credit history considered | 7-factor on-chain analysis |
| Price manipulation risks | Multi-oracle validation with anomaly detection |
| Static risk management | Real-time volatility-adjusted LTV |
| Emoji-based UI | Professional icon system (Lucide) |

---

## ✨ Features

### 🔷 Core Lending Features

<div align="center">

![Borrow & Lend Interface](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.32.46.png)

</div>

- **Deposit Collateral**: Lock ALGO to enable borrowing
- **Borrow Funds**: Take loans at 60-75% LTV based on credit score
- **Repay Loans**: Partial or full repayment with 5% APR interest
- **Withdraw**: Retrieve collateral after repaying debt
- **Liquidation**: Underwater positions liquidated by community (10% penalty)

### 📊 Credit Scoring System

<div align="center">

![Credit Score Dashboard](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.33.03.png)

</div>

**7 Transparent Factors:**

| Factor | Weight | What It Measures |
|--------|---------|------------------|
| 🕐 Wallet Age | 25% | Account longevity (1+ years = excellent) |
| 💸 Transaction History | 20% | Consistent activity (100+ txns ideal) |
| 💰 Balance Stability | 20% | Maintained balance over 30-90 days |
| 🎯 DApp Participation | 20% | Ecosystem engagement (5+ apps) |
| 🗳️ Governance | 15% | Algorand governance participation |
| 📈 Asset Diversity | Bonus | Holding multiple ASAs |
| ⚡ Recent Activity | Bonus | Last 30 days transaction velocity |

**Credit Score Benefits:**

- **750-850** (Excellent): 75% LTV, premium rates
- **700-749** (Good): 70% LTV
- **650-699** (Fair): 65% LTV
- **<650** (New): 60% LTV

### 🛡️ DeFi Stability Layer

**Advanced Risk Management System** combining:

#### 1. Volatility Indicator
- Real-time volatility calculation: `σ / μ × 100%`
- Color-coded risk bars (green/yellow/red)
- **Dynamic LTV adjustment**: Low volatility → 75% LTV, High volatility → 50% LTV
- 30-period rolling window analysis
- Prevents over-leveraging during volatile markets

#### 2. Oracle Anomaly Detector
- Cross-checks main oracle against backup feeds (Chainlink + DEX TWAP)
- Flags deviations >5%
- Automatic price update pause on anomalies
- **Proof-of-Sanity system**: Only verified data reaches smart contracts
- Flash loan attack protection

#### 3. Unified Dashboard
- System health score (0-100)
- Real-time monitoring every 10-30 seconds
- Professional Lucide icon system
- Educational tooltips for all features

### 📄 Document Verification System

<div align="center">

![Document Upload](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.33.17.png)

</div>

**Cryptographic Signature Validation:**

| Document Type | Credit Boost | Requirements |
|---------------|--------------|--------------|
| 🛂 Passport | +80-120 pts | Government ID with HMAC signature |
| 🚗 Driver's License | +60-100 pts | State/country issued |
| 📋 Tax Return | +55-90 pts | IRS verification |
| 🏦 Bank Statement | +45-75 pts | Last 1-3 months |
| 💼 Employment Letter | +40-65 pts | Company letterhead |
| 📧 Utility Bill | +30-50 pts | Recent (60 days) |

**Security Features:**
- HMAC-SHA256 cryptographic signatures
- Trusted issuer registry (government, banks, IRS)
- Variable boost ranges (70-100% for signed, 40-70% for unsigned)
- Document hash verification (SHA256)
- No PII storage (hashes only)

### 📈 Real-Time Monitoring

- **Health Bar**: Visual borrowing capacity (green/yellow/red zones)
- **Live Activity Feed**: WebSocket-powered transaction updates
- **Interactive Charts**: 6 visualization types with Recharts
- **Pool Statistics**: Total collateral, borrows, utilization rate
- **Transaction History**: Complete audit trail

---

## ⚙️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                     Pera Wallet Integration                      │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 15)                         │
│  • 7 Interactive Tabs (Stability, Credit, Borrow, Documents...) │
│  • Real-time WebSocket Updates & Live Activity Feed             │
│  • Professional Lucide Icons (replaces all emojis)               │
│  • Recharts Data Visualization                                   │
└────────┬───────────────────────────────┬────────────────────────┘
         │                               │
         │ REST API                      │ Blockchain Txns
         ▼                               ▼
┌─────────────────────────┐    ┌─────────────────────────────────┐
│  BACKEND (FastAPI)      │    │  SMART CONTRACT (PyTeal)        │
│  • Credit Score Engine  │    │  • Deposit/Borrow/Repay         │
│  • Document Verification│    │  • Dynamic LTV (60-75%)         │
│  • WebSocket Server     │    │  • Liquidation Protection       │
│  • Volatility Monitoring│    │  • Global/Local State           │
│  • Oracle Validation    │    │  • App ID: 748013252            │
└─────────┬───────────────┘    └────────────┬────────────────────┘
          │                                 │
          │ Blockchain Queries              │ State Updates
          ▼                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│               ALGORAND TESTNET BLOCKCHAIN                        │
│  • Transaction History & Wallet Analytics                        │
│  • Price Oracles & Market Data                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Smart Contract** | PyTeal, TEAL | Lending operations, state management |
| **Backend** | FastAPI, Python 3.11+ | Credit scoring, document verification, WebSocket |
| **Frontend** | Next.js 15, React 18, TypeScript | UI, wallet integration, real-time updates |
| **Styling** | TailwindCSS, Lucide Icons | Professional design system |
| **Charts** | Recharts | Interactive data visualization |
| **Blockchain** | Algorand TestNet | Decentralized ledger |
| **Wallet** | Pera Wallet SDK | Transaction signing |

---

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.11+** (for backend & contracts)
- **Algorand Wallet** (Pera Wallet recommended)
- **TestNet ALGO** (get from [faucet](https://bank.testnet.algorand.network))

### 1. Smart Contract Setup

```bash
cd contracts

# Install dependencies
pip install -r requirements.txt

# Compile the contract
python loan_pool.py

# Deploy to TestNet (requires funded account)
python deploy.py
```

**Note**: Save the Application ID from deployment - you'll need it for backend configuration.

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your configuration:
# - SECRET_KEY (for signing attestations)
# - APP_ID (from contract deployment)

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend-nextjs

# Install dependencies
npm install

# Run development server
npm run dev
```

The UI will be available at `http://localhost:3000`

### 4. First-Time Usage

1. **Connect Wallet**: Click "Connect Wallet" and approve in Pera Wallet
2. **Check Network**: Ensure you're on Algorand TestNet
3. **Get TestNet ALGO**: Visit [faucet](https://bank.testnet.algorand.network) if balance is low
4. **Opt-In**: Click "Opt-In to Contract" (~0.1 ALGO one-time fee)
5. **Deposit**: Send ALGO as collateral
6. **Check Credit Score**: View your on-chain credit rating
7. **Borrow**: Take a loan based on your LTV
8. **Upload Documents**: Boost credit score with verified documents
9. **Monitor Health**: Watch the health bar to avoid liquidation

---

## 📋 API Endpoints

### Credit Scoring

```http
POST /api/credit-score
Content-Type: application/json

{
  "address": "ALGORAND_ADDRESS_HERE"
}

Response:
{
  "score": 850,
  "base_score": 750,
  "document_boost": 100,
  "factors": {
    "wallet_age": { "score": 200, "weight": 0.25 },
    "transaction_count": { "score": 150, "weight": 0.20 },
    ...
  },
  "signature": "HMAC_SIGNATURE"
}
```

### Document Verification

```http
POST /api/documents/upload
Content-Type: application/json

{
  "address": "ALGO_ADDRESS",
  "document_type": "passport",
  "content": "base64_encoded_content",
  "issuer_id": "DEMO_GOVT",
  "issuer_signature": "HMAC_SIGNATURE"
}

Response:
{
  "success": true,
  "credit_boost": 95,
  "signature_valid": true,
  "message": "Document verified successfully"
}
```

### Pool Statistics

```http
GET /api/pool-stats/{app_id}

Response:
{
  "total_collateral": 100000000,
  "total_borrow": 45000000,
  "utilization_rate": 0.45,
  "active_users": 12
}
```

### User Position

```http
POST /api/user-stats
Content-Type: application/json

{
  "address": "...",
  "app_id": 748013252
}

Response:
{
  "collateral": 10000000,
  "debt": 4500000,
  "ltv": 0.45,
  "health": 0.90
}
```

**Full API documentation:** http://localhost:8000/docs

---

## 🧪 Testing

### Testing Document Verification

```bash
cd backend

# Generate sample documents (6 valid, 2 invalid)
python generate_sample_documents.py

# Run automated test suite
python test_document_verification.py
```

**Expected Output:**
```
Test 1/8: PASSPORT - ✅ VALID SIGNATURE
✅ PASS: Valid document accepted
   Credit Boost: +95 points
   Signature Valid: True

...

Test 7/8: PASSPORT - ❌ INVALID SIGNATURE
✅ PASS: Invalid document correctly rejected

TEST SUMMARY
✅ Passed: 8/8
Success Rate: 100.0%
```

### Testing Frontend

1. Open http://localhost:3000
2. Click "Connect Wallet"
3. Approve connection in Pera Wallet
4. Navigate through all 7 tabs
5. Test deposit, borrow, repay, withdraw
6. Upload sample documents
7. View DeFi Stability Layer

---

## 🏗️ Project Structure

```
TrustLens/
├── contracts/                 # Smart contracts
│   ├── loan_pool.py          # Main lending contract (PyTeal)
│   ├── loan_pool_approval.teal # Compiled TEAL
│   ├── loan_pool_clear.teal
│   └── deploy.py             # Deployment script
├── backend/                   # FastAPI backend
│   ├── main.py               # API server + WebSocket
│   ├── document_verification.py  # Signature validation
│   ├── generate_sample_documents.py  # Test data generator
│   ├── test_document_verification.py # Test suite
│   └── requirements.txt
├── frontend-nextjs/           # Next.js 15 frontend
│   ├── app/                  # App router
│   ├── components/           # React components
│   │   ├── Dashboard.tsx     # Main dashboard with 7 tabs
│   │   ├── DeFiStabilityLayer.tsx  # Volatility + Oracle monitoring
│   │   ├── VolatilityIndicator.tsx
│   │   ├── OracleAnomalyDetector.tsx
│   │   ├── BorrowLendTab.tsx
│   │   ├── CreditScoreTab.tsx
│   │   ├── DocumentVerificationTab.tsx
│   │   └── ... (15+ components)
│   ├── context/              # Wallet & WebSocket context
│   ├── utils/                # Helpers & services
│   └── public/               # Static assets & screenshots
└── docs/                      # Documentation
    ├── DEFI_STABILITY_LAYER.md
    ├── ICON_AND_TESTING_GUIDE.md
    └── IMPLEMENTATION_SUMMARY.md
```

---

## 🔒 Security & Privacy

### Smart Contract Security

✅ **Audited Design Patterns:**
- No admin keys - fully decentralized
- Integer-only calculations (no floating point bugs)
- Comprehensive input validation
- Maximum LTV caps prevent over-borrowing
- Safe withdrawal checks

✅ **Liquidation Protection:**
- 10% penalty incentivizes liquidators
- Community-driven liquidation
- Protects pool from bad debt

### Document Verification Privacy

**Current (Demo Mode):**
- ✅ In-memory storage only (no database)
- ✅ SHA256 integrity checking
- ✅ HMAC-SHA256 signature validation
- ⚠️ Demo signatures for testing

**Production Architecture (Planned):**
1. **Zero-Knowledge Proofs**: Verify without storing sensitive data
2. **OCR-Only Processing**: Extract data, discard document
3. **Blockchain Attestation**: Immutable verification record
4. **GDPR/CCPA Compliant**: Right to deletion, data minimization

### Data Protection

- **No PII Storage**: Credit scores from public blockchain data only
- **User Control**: Connect/disconnect wallet anytime
- **TestNet Only**: No real money at risk during testing
- **Transparent**: All smart contract code public on AlgoExplorer

---

## 📊 Project Statistics

- **Lines of Code:** 8,000+ (contracts + backend + frontend)
- **Features Implemented:** 30+
- **Contract Deployments:** 7 iterations
- **API Endpoints:** 15+ RESTful + WebSocket
- **React Components:** 20+ with professional icon system
- **Chart Types:** 6 interactive visualizations
- **Test Coverage:** 8 document verification tests
- **Documentation Files:** 10+ markdown files

---

## 🛠️ Development

### Running Tests

**Backend:**
```bash
cd backend
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html  # View coverage report
```

**Document Verification:**
```bash
cd backend
python test_document_verification.py
```

**Frontend:**
```bash
cd frontend-nextjs
npm run build        # Production build
npm run lint         # Check for errors
```

---

## 🎯 Roadmap

### ✅ Completed (Phase 1-4)
- ✅ Core lending smart contract (deposit, borrow, repay, withdraw)
- ✅ 7-factor credit scoring engine
- ✅ Document verification with cryptographic signatures
- ✅ DeFi Stability Layer (volatility + oracle monitoring)
- ✅ Professional icon system (Lucide React)
- ✅ Real-time WebSocket updates
- ✅ Interactive charts (Recharts)
- ✅ Educational tooltips (20+)
- ✅ Test suite for document verification

### 🚧 In Progress (Phase 5)
- Interest accrual visualization
- Cross-browser compatibility testing
- Mobile responsiveness improvements
- MainNet deployment preparation

### 📋 Planned (Phase 6+)
- Multi-asset collateral (USDC, other ASAs)
- Flash loan protection enhancements
- Production oracle integration (Chainlink)
- Governance token for platform decisions
- Zero-knowledge proof implementation
- Mobile app (React Native)

---

## 🤝 Contributing

This project is built for the **Algorand DeFi Hackathon**. Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Algorand Foundation** for the robust blockchain infrastructure
- **Pera Wallet** for seamless wallet integration
- **FastAPI** for the high-performance backend framework
- **Next.js Team** for the excellent React framework
- **PyTeal Community** for smart contract development resources
- **Lucide** for the beautiful icon library

---

## 📞 Support & Contact

- **Live Demo:** http://localhost:3000 (after setup)
- **Smart Contract:** [AlgoExplorer](https://testnet.algoexplorer.io/application/748013252)
- **API Documentation:** http://localhost:8000/docs
- **Issues:** [GitHub Issues](https://github.com/TheDarkEyezor/TrustLens/issues)

---

<div align="center">

**Built with ❤️ for the Algorand Ecosystem**

*Making DeFi lending fair, transparent, and accessible to everyone*

[⬆ Back to Top](#-trustlens)

</div>
