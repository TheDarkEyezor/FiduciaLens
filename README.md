# 🏦 FiduciaLens - On-Chain Credit Scoring & DeFi Lending on Algorand# FiduciaLens - On-Chain Credit Scoring & Collateral Stability Dashboard



<div align="center">🏆 **Algorand DeFi Hackathon Project**



![FiduciaLens Dashboard](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.32.29.png)Enable fairer DeFi lending by combining on-chain credit scoring, collateral stability visualization, and smart contracts on Algorand.



**Democratizing DeFi Lending through Transparent On-Chain Credit Scoring**## 🎯 Project Overview



[![Algorand](https://img.shields.io/badge/Algorand-TestNet-00D1B2?style=for-the-badge&logo=algorand)](https://testnet.algoexplorer.io/application/748013252)FiduciaLens revolutionizes DeFi lending by:

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)- **📊 On-Chain Credit Scoring**: Calculate credit scores based on wallet activity and verified claims

[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)- **💰 Smart Contract Lending**: Deposit collateral, borrow, and repay loans on Algorand

[![PyTeal](https://img.shields.io/badge/Smart_Contract-PyTeal-7B3FF2?style=for-the-badge)](https://pyteal.readthedocs.io/)- **📈 Collateral Stability Visualizer**: Simulate how price fluctuations affect pool health and liquidation risk



</div>## �️ System Architecture



---```mermaid

graph TB

## 🎯 What is FiduciaLens?    subgraph "User Interface"

        A[Pera Wallet] -->|Connect| B[Next.js Frontend]

FiduciaLens is a **decentralized lending platform** built on Algorand that revolutionizes DeFi by introducing **fair, transparent credit scoring**. Unlike traditional DeFi protocols that treat all users equally (and risk equally), FiduciaLens analyzes on-chain behavior to reward responsible users with better loan terms.    end

    

### The Problem We Solve    subgraph "Frontend Layer - Next.js 15 + React + TailwindCSS"

        B -->|API Calls| C[FastAPI Backend]

**Traditional DeFi:** Everyone gets the same 50% LTV, regardless of their history          B -->|Transactions| D[Smart Contract]

**FiduciaLens:** Responsible users earn up to 60% LTV through proven on-chain behavior + verified documents        B -->|WebSocket| E[Real-time Updates]

    end

### Key Innovation    

    subgraph "Backend Layer - FastAPI + Python"

- 🔍 **7-Factor On-Chain Credit Score** (0-850 range, like FICO)        C -->|Query Blockchain| D

- 📄 **Document Verification** (+400 point boost from real-world credentials)        C -->|Credit Score Calculation| F[Credit Scoring Engine]

- 🏦 **Smart Contract Lending** (deposit, borrow, repay, withdraw, liquidate)        C -->|Price Data| G[Oracle Simulation]

- 📊 **Real-Time Risk Monitoring** (health bar, activity feed, WebSocket updates)        C -->|WebSocket Events| E

- 🎓 **Educational Experience** (20+ contextual tooltips explaining DeFi concepts)        F -->|Wallet Analytics| H[Algorand API]

    end

---    

    subgraph "Blockchain Layer - Algorand TestNet"

## ✨ Features        D[Smart Contract - PyTeal]

        D -->|Store State| I[Global State]

### 🔷 Core Lending Features        D -->|User Data| J[Local State]

        H[Algorand Node API]

<div align="center">        K[Transaction History]

    end

![Borrow & Lend Interface](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.32.46.png)    

    subgraph "Data Visualization"

</div>        B -->|Recharts| L[6 Chart Types]

        L -->|Display| M[Collateral Stability]

- **Deposit Collateral**: Lock ALGO to enable borrowing        L -->|Display| N[Credit Score Factors]

- **Borrow Funds**: Take loans at 50-60% LTV based on credit score        L -->|Display| O[Pool Health Metrics]

- **Repay Loans**: Partial or full repayment with instant processing    end

- **Withdraw**: Retrieve collateral after repaying debt    

- **Forced Liquidation**: Underwater positions can be liquidated by anyone (10% penalty)    style A fill:#4CAF50

    style B fill:#2196F3

### 📊 Credit Scoring System    style C fill:#FF9800

    style D fill:#9C27B0

<div align="center">    style F fill:#FF5722

```

![Credit Score Dashboard](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.33.03.png)

### Component Breakdown

</div>

**Frontend (Next.js)**

**7 Transparent Factors:**- 🎨 **UI Components**: 15+ React components with TailwindCSS styling

- 🔗 **Wallet Integration**: Pera Wallet SDK for seamless transactions

| Factor | Weight | What It Measures |- 📊 **Data Visualization**: Recharts library for 6 interactive chart types

|--------|---------|------------------|- 🔄 **Real-time Updates**: WebSocket connection for live activity feed

| 🕐 Wallet Age | 25% | Account longevity (1+ years = excellent) |- 💾 **State Management**: React hooks + localStorage for persistence

| 💸 Transaction History | 20% | Consistent activity (100+ txns ideal) |- 🎓 **Educational Tooltips**: 18 contextual tooltips explaining DeFi concepts

| 💰 Balance Stability | 20% | Maintained balance over 30-90 days |

| 🎯 DApp Participation | 20% | Ecosystem engagement (5+ apps) |**Backend (FastAPI)**

| 🗳️ Governance | 15% | Algorand governance participation |- 🔐 **API Endpoints**: 10+ RESTful endpoints for all operations

| 📈 Asset Diversity | Bonus | Holding multiple ASAs |- 📡 **WebSocket Server**: Real-time event broadcasting (deposits, borrows, repays)

| ⚡ Recent Activity | Bonus | Last 30 days transaction velocity |- 🧮 **Credit Score Engine**: 5-factor scoring algorithm:

  - Wallet Age (25%)

**Score Benefits:**  - Transaction History (20%)

- **750-850** (Excellent): 60% LTV, premium rates  - Balance Stability (20%)

- **700-749** (Good): 55% LTV  - App Participation (20%)

- **650-699** (Fair): 52% LTV  - Governance Participation (15%)

- **<650** (Building): 50% LTV- 🎯 **Oracle Simulation**: Mock price feeds for collateral valuation

- 📈 **Analytics**: Transaction tracking and pool metrics

### 📄 Document Verification System

**Smart Contract (PyTeal/TEAL)**

<div align="center">- 🏦 **Lending Operations**: Deposit, borrow, repay, withdraw

- 📊 **State Management**: Global and local state for pool and user data

![Document Upload](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.33.17.png)- 🔒 **Access Control**: Wallet-based authorization

- 💰 **LTV Enforcement**: Dynamic loan-to-value ratios (50-60% based on credit score)

</div>- ✅ **Safety Checks**: Prevents over-borrowing and undercollateralized withdrawals



**Instant Credit Boost:**### Data Flow



| Document Type | Credit Boost | Requirements |1. **User Connection**: Pera Wallet connects → Frontend detects TestNet/MainNet

|---------------|--------------|--------------|2. **Credit Score**: Frontend requests → Backend analyzes wallet via Algorand API → Returns score

| 🛂 Passport | +100 points | Government ID with photo |3. **Deposit**: User signs transaction → Contract updates global + local state → Frontend refreshes

| 🚗 Driver's License | +80 points | State/country issued |4. **Borrow**: Backend fetches credit score → Calculates max LTV → User signs → Contract validates and transfers

| 📋 Tax Return | +70 points | Most recent year |5. **Repay**: User signs repayment → Contract updates debt → Backend recalculates credit score → Frontend auto-refreshes

| 🏦 Bank Statement | +60 points | Last 1-3 months |6. **Real-time Feed**: All transactions emit WebSocket events → All connected clients receive updates

| 💼 Employment Letter | +50 points | Company letterhead |7. **Visualization**: Frontend polls contract state → Recharts renders 6 chart types → User sees live metrics

| 📧 Utility Bill | +40 points | Recent (60 days) |

## �🏗️ Project Structure

**Maximum Boost:** +400 points (upload all 6 types)  

**Privacy:** Zero-knowledge architecture planned (see [Security](#-security--privacy))```

fiducialens/

### 📈 Real-Time Monitoring├── contracts/          # PyTeal smart contracts

│   ├── loan_pool.py   # Main lending contract

- **Health Bar**: Visual indicator of borrowing capacity usage│   ├── deploy.py      # Deployment script

  - 🟢 Green (0-70%): Safe zone│   └── requirements.txt

  - 🟡 Yellow (70-90%): Warning├── backend/           # FastAPI backend

  - 🔴 Red (90-100%): Critical - liquidation risk!│   ├── main.py        # API endpoints

- **Live Activity Feed**: Real-time transaction updates via WebSocket│   ├── requirements.txt

- **Interactive Charts**: 6 chart types powered by Recharts│   └── .env.example

- **Pool Statistics**: Total collateral, borrows, utilization rate├── frontend/          # React + Tailwind UI

│   ├── src/

### 🎓 Educational Features│   │   ├── components/

│   │   ├── context/

- **20+ Interactive Tooltips**: Hover over any ? icon to learn│   │   ├── services/

- **DeFi Concept Explainers**: Credit scores, LTV, collateral, liquidation│   │   └── main.tsx

- **Guided Onboarding**: Step-by-step first-time user experience│   └── package.json

- **Risk Warnings**: Clear alerts before dangerous actions└── plan.md           # Project roadmap

```

---

## 🚀 Quick Start

## 🏗️ Architecture

### Prerequisites

### System Overview

- Python 3.9+

```- Node.js 18+

┌─────────────────────────────────────────────────────────────────┐- Algorand TestNet account with ALGO

│                         USER INTERFACE                           │- Pera Wallet (for frontend testing)

│                     Pera Wallet Integration                      │

└────────────────┬────────────────────────────────────────────────┘### 1. Smart Contract Setup

                 │

┌────────────────▼────────────────────────────────────────────────┐```bash

│                    FRONTEND (Next.js 15)                         │cd contracts

│  • 6 Interactive Tabs (Dashboard, Credit, Borrow, Activity,     │

│    Documents, Visualizer)                                        │# Install dependencies

│  • Real-time WebSocket Updates                                   │pip install -r requirements.txt

│  • 15+ React Components with Dark Glassmorphism Theme            │

│  • Recharts for Data Visualization                               │# Compile the contract

└────────┬───────────────────────────────┬────────────────────────┘python loan_pool.py

         │                               │

         │ API Calls                     │ Transactions# Deploy to TestNet (requires funded account)

         ▼                               ▼python deploy.py

┌─────────────────────────┐    ┌─────────────────────────────────┐```

│  BACKEND (FastAPI)      │    │  SMART CONTRACT (PyTeal)        │

│  • Credit Score Engine  │    │  • Deposit Collateral           │**Note**: Save the Application ID from deployment - you'll need it for backend configuration.

│  • Document Verification│    │  • Borrow Funds                 │

│  • WebSocket Server     │    │  • Repay Loans                  │### 2. Backend Setup

│  • Oracle Simulation    │    │  • Withdraw Collateral          │

│  • 10+ REST Endpoints   │    │  • Liquidate Positions          │```bash

└─────────┬───────────────┘    └────────────┬────────────────────┘cd backend

          │                                 │

          │ Query Blockchain                │ On-Chain State# Install dependencies

          ▼                                 ▼pip install -r requirements.txt

┌─────────────────────────────────────────────────────────────────┐

│               ALGORAND TESTNET BLOCKCHAIN                        │# Create .env file

│  • App ID: 748013252                                             │cp .env.example .env

│  • Global State: Pool statistics                                 │

│  • Local State: User positions (collateral, debt)                │# Edit .env and add your configuration:

│  • Transaction History & Wallet Analytics                        │# - SECRET_KEY (for signing attestations)

└─────────────────────────────────────────────────────────────────┘# - APP_ID (from contract deployment)

```

# Run the server

### Technology Stackpython main.py

```

**Smart Contract Layer:**

- **Language:** PyTeal (Python → TEAL compiler)The API will be available at `http://localhost:8000`

- **Functions:** 5 (deposit, borrow, repay, withdraw, liquidate)

- **State Management:** Global (pool) + Local (user positions)### 3. Frontend Setup

- **Safety:** Integer-only math, comprehensive validation

```bash

**Backend Layer:**cd frontend

- **Framework:** FastAPI (Python 3.11+)

- **APIs:** 10+ RESTful endpoints + WebSocket server# Install dependencies

- **Credit Engine:** 7-factor scoring algorithmnpm install

- **Document System:** Upload, verify, track (6 types)

- **Oracle:** Simulated price feeds (production-ready)# Run development server

npm run dev

**Frontend Layer:**```

- **Framework:** Next.js 15 (React 18, TypeScript)

- **Styling:** TailwindCSS + Dark Glassmorphism DesignThe UI will be available at `http://localhost:3000`

- **Charts:** Recharts (6 interactive visualizations)

- **Wallet:** Pera Wallet SDK## 🔧 Configuration

- **State:** React hooks + localStorage persistence

### Backend (.env)

---```bash

SECRET_KEY=your-secret-key-here

## 🔒 Security & PrivacyAPP_ID=your-deployed-app-id

ALGORAND_NETWORK=testnet

### Smart Contract SecurityAPI_HOST=0.0.0.0

API_PORT=8000

✅ **Audited Design Patterns:**```

- No admin keys - fully decentralized

- Integer-only calculations (no floating point bugs)### Frontend (.env)

- Comprehensive input validation on all functions```bash

- Maximum LTV caps prevent over-borrowingVITE_API_URL=http://localhost:8000

- Safe withdrawal checks (can't withdraw while undercollateralized)VITE_APP_ID=your-deployed-app-id

```

✅ **Liquidation Protection:**

- 10% penalty incentivizes liquidators## 📋 Features

- Community-driven liquidation (any wallet can call)

- Protects pool from bad debt accumulation### Tier 1 - Core MVP ✅



### Document Verification Privacy- **🟢 Lending Smart Contract**: PyTeal contract with deposit, borrow, repay, and withdraw functions

- **🟢 Credit Scoring**: Off-chain computation based on wallet age, transactions, balance, and app participation

**Current (Demo Mode):**- **🟢 Signed Credit Attestation**: HMAC-signed scores for verification

- ✅ In-memory storage only (no database)- **🟢 Frontend Wallet Connect**: Pera Wallet integration on TestNet

- ✅ SHA256 integrity checking- **🟢 Basic Dashboard UI**: Three-tab interface (Score, Borrow/Lend, Visualizer)

- ⚠️ Mock verification (accepts all uploads for testing)

### Tier 2 - Enhancements 🚧

**Production Architecture (Designed, not yet implemented):**

- **🟡 Collateral Stability Visualizer**: Interactive charts showing pool health under price fluctuations

```- **🟡 Score Weight Integration**: Dynamic LTV based on credit scores

📄 User Upload- **🟡 Oracle Mock**: Simulated price feeds (ready for implementation)

    ↓

🔐 OCR Extraction (AWS Textract / Google Vision)### Tier 3 - Stretch Goals 📝

    ↓

🔍 Name/Address Validation (cross-document consistency)- Document verification

    ↓- Oracle anomaly detection

✅ Identity Verification (Stripe Identity / Onfido / Jumio)- SBT-like proof tokens

    ↓- Multi-collateral pools

🧮 Zero-Knowledge Proof Generation (no PII storage)

    ↓## 🔐 Security Considerations

⛓️ Blockchain Attestation (verifiable on-chain)

    ↓- All smart contract inputs are validated

🎯 Credit Boost Applied (without storing documents)- Maximum LTV capped at 50% (60% for high credit scores)

```- No admin key control - fully decentralized

- Personal data stored as hashes only

**Privacy Guarantees:**- Signature verification for credit attestations

1. **Zero-Knowledge Proofs**: Verify without storing sensitive data

2. **OCR-Only Processing**: Extract data, discard document## 📊 API Endpoints

3. **Blockchain Attestation**: Immutable verification record

4. **GDPR/CCPA Compliant**: Right to deletion, data minimization### Credit Scoring

5. **Service Integration**: Stripe Identity ($1-3/verification)```bash

POST /api/credit-score

### Production Security Implementation PlanBody: { "address": "ALGORAND_ADDRESS" }

Response: { "score": 75, "factors": {...}, "signature": "..." }

**Phase 1: Document Processing Pipeline**```

- AWS Textract for OCR (99%+ accuracy)

- Google Vision API as fallback### Pool Statistics

- Document type classification (passport vs license)```bash

- Data extraction (name, address, DOB, ID numbers)GET /api/pool-stats/{app_id}

Response: { "total_collateral": 10000, "total_borrow": 4000, ... }

**Phase 2: Identity Verification**```

- **Stripe Identity**: $1-3 per verification

  - Document authenticity check### User Statistics

  - Liveness detection (selfie matching)```bash

  - Government database verificationPOST /api/user-stats

- **Onfido**: $2-5 per check (alternative)Body: { "address": "...", "app_id": 123 }

- **Jumio**: $3-8 per check (enterprise option)Response: { "collateral": 1000, "debt": 400, ... }

```

**Phase 3: Zero-Knowledge Proofs**

- zk-SNARKs implementation using snarkjs## 🧪 Testing

- Prove "user has valid passport" without revealing passport details

- Generate proof: `P(passport_valid) → true/false`### Test Credit Scoring

- Verifier validates proof on-chain (cheap, ~0.002 ALGO gas)```bash

curl -X POST http://localhost:8000/api/credit-score \

**Phase 4: Blockchain Attestation**  -H "Content-Type: application/json" \

- Smart contract stores:  -d '{"address": "YOUR_ALGORAND_ADDRESS"}'

  - Document hash (SHA256)```

  - Verification timestamp

  - Verification provider signature### Test Frontend

  - Credit boost amount1. Open http://localhost:3000

- NO storage of:2. Click "Connect Wallet"

  - Personal names3. Approve connection in Pera Wallet

  - Addresses4. Navigate through tabs to test features

  - ID numbers

  - Document images## 📱 Smart Contract Operations



**Cost Analysis:**### Deposit Collateral

- Per-user verification cost: $5-15 (one-time)```python

- Benefits: +400 credit score points# Group transaction: Payment + App Call

- Value unlock: 10% higher LTV = borrow $10,000 more per $100k collateral# Payment: Send ALGO to app address

- ROI: Massive for serious borrowers# App Call: "deposit" with payment reference

```

**Data Protection:**

- All PII deleted after verification### Borrow

- Only cryptographic proofs retained```python

- GDPR Article 17 compliant (right to erasure)# App Call: "borrow" with amount and credit score

- CCPA compliant (data minimization)# Credit score used to determine max LTV

- SOC 2 Type II certification (production)```



**See Full Details:** [DOCUMENT_VERIFICATION_SECURITY.md](https://github.com/yourusername/FiduciaLens/blob/main/DOCUMENT_VERIFICATION_SECURITY.md) (400+ lines)### Repay

```python

### Data Protection# Group transaction: Payment + App Call

# Payment: Repayment amount to app

- **No PII Storage**: Credit scores calculated from public blockchain data# App Call: "repay" with payment reference

- **User Control**: Connect/disconnect wallet anytime```

- **Testnet Only**: No real money at risk during testing

- **Transparent**: All smart contract code is public on AlgoExplorer### Withdraw

```python

---# App Call: "withdraw" with amount

# Only allowed when debt = 0

## 🖼️ Screenshots```



### Dashboard Overview## 🛠️ Development

![Dashboard](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.32.29.png)

*Main dashboard showing pool statistics, health bar, and navigation*### Frontend Development

```bash

### Credit Score Analysisnpm run dev     # Development server

![Credit Score](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.33.03.png)npm run build   # Production build

*7-factor credit scoring breakdown with animated gauge*npm run preview # Preview production build

```

### Borrow & Lend Interface

![Borrow & Lend](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.32.46.png)### Backend Development

*Deposit collateral, borrow funds, repay loans, withdraw - all in one tab*```bash

# Run with auto-reload

### Document Verificationuvicorn main:app --reload --host 0.0.0.0 --port 8000

![Documents](frontend-nextjs/public/Screenshot%202025-10-19%20at%2008.33.17.png)```

*Upload identity/financial documents for instant +400 point credit boost*

### Contract Development

---```bash

# Compile contract

## 🚀 Quick Startpython loan_pool.py



### Prerequisites# Generate TEAL files

# - loan_pool_approval.teal

- **Node.js 18+** (for frontend)# - loan_pool_clear.teal

- **Python 3.11+** (for backend & contracts)```

- **Algorand Wallet** (Pera Wallet recommended)

- **TestNet ALGO** (get from [faucet](https://bank.testnet.algorand.network))## 📄 License



### InstallationMIT License - Built for Algorand Hackathon



```bash## 🤝 Contributing

# Clone repository

git clone https://github.com/yourusername/FiduciaLens.gitThis is a hackathon project. Feel free to fork and extend!

cd FiduciaLens

## 📞 Support

# Install backend dependencies

cd backendFor questions or issues, please refer to the project documentation or Algorand developer resources.

pip install -r requirements.txt

---

# Install frontend dependencies

cd ../frontend-nextjs**Built with ❤️ for the Algorand Ecosystem**

npm install
```

### Configuration

**Backend** (`backend/.env`):
```bash
APP_ID=748013252
SECRET_KEY=your-secret-key-for-signing
ALGORAND_NETWORK=testnet
API_HOST=0.0.0.0
API_PORT=8000
```

**Frontend** (environment variables handled by Next.js):
```bash
# Automatically uses APP_ID from backend
NEXT_PUBLIC_APP_ID=748013252
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
# or: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend-nextjs
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### First-Time Usage

1. **Connect Wallet**: Click "Connect Wallet" and approve in Pera Wallet
2. **Check Network**: Ensure you're on Algorand TestNet
3. **Get TestNet ALGO**: Visit faucet if balance is low
4. **Opt-In**: Click "Opt-In to Contract" (~0.1 ALGO one-time fee)
5. **Deposit**: Send ALGO as collateral
6. **Check Credit Score**: View your on-chain credit rating
7. **Borrow**: Take a loan based on your LTV
8. **Upload Documents**: Boost credit score by +400 points
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

Response: {
  "score": 850,
  "base_score": 750,
  "document_boost": 100,
  "factors": { ... },
  "signature": "HMAC_SIGNATURE"
}
```

### Document Verification
```http
POST /api/documents/upload
{
  "wallet_address": "...",
  "document_type": "passport",
  "file_data": "base64_encoded_file",
  "consent": true
}

GET /api/documents/{wallet_address}
GET /api/documents/types
GET /api/credit-score/{wallet_address}/with-documents
```

### Pool Statistics
```http
GET /api/pool-stats/{app_id}

Response: {
  "total_collateral": 100000000,
  "total_borrow": 45000000,
  "utilization_rate": 0.45,
  "active_users": 12
}
```

### User Position
```http
POST /api/user-stats
{
  "address": "...",
  "app_id": 748013252
}

Response: {
  "collateral": 10000000,
  "debt": 4500000,
  "ltv": 0.45,
  "health": 0.90
}
```

**Full API documentation:** http://localhost:8000/docs

---

## 🧪 Smart Contract Functions

### 1. Deposit Collateral
```python
# Group transaction: Payment + App Call
txn1 = PaymentTxn(sender, sp, app_address, amount)
txn2 = ApplicationCallTxn(sender, sp, app_id, 
                          on_complete=OnComplete.NoOpOC,
                          app_args=["deposit"])
```

### 2. Borrow Funds
```python
# Requires credit score attestation
txn = ApplicationCallTxn(sender, sp, app_id,
                         on_complete=OnComplete.NoOpOC,
                         app_args=["borrow", amount, credit_score, signature])
```

### 3. Repay Loan
```python
# Group transaction: Payment + App Call
txn1 = PaymentTxn(sender, sp, app_address, repay_amount)
txn2 = ApplicationCallTxn(sender, sp, app_id,
                          on_complete=OnComplete.NoOpOC,
                          app_args=["repay"])
```

### 4. Withdraw Collateral
```python
# Only if debt = 0 OR remaining collateral keeps LTV safe
txn = ApplicationCallTxn(sender, sp, app_id,
                         on_complete=OnComplete.NoOpOC,
                         app_args=["withdraw", amount])
```

### 5. Liquidate Position
```python
# Anyone can liquidate underwater position
# Liquidator receives 10% penalty from borrower's collateral
txn = ApplicationCallTxn(sender, sp, app_id,
                         on_complete=OnComplete.NoOpOC,
                         app_args=["liquidate", target_address])
```

---

## 📊 Project Statistics

- **Lines of Code:** 5,000+ (contracts + backend + frontend)
- **Features Implemented:** 25+
- **Contract Deployments:** 7 (iterative bug fixes + feature additions)
- **Test Coverage:** 50% (core features tested)
- **Documentation Files:** 15+ markdown files
- **Interactive Tooltips:** 20+ educational explainers
- **API Endpoints:** 10+ RESTful + WebSocket
- **React Components:** 15+ with dark glassmorphism theme
- **Chart Types:** 6 interactive visualizations

---

## 🛠️ Development

### Running Tests

**Backend:**
```bash
cd backend
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html  # View coverage report
```

**Smart Contract:**
```bash
cd contracts
python loan_pool.py  # Compile to TEAL
python deploy.py     # Deploy to TestNet
```

**Frontend:**
```bash
cd frontend-nextjs
npm run build        # Production build
npm run lint         # Check for errors
```

### Project Structure

```
FiduciaLens/
├── contracts/                 # Smart contracts
│   ├── loan_pool.py          # Main lending contract (PyTeal)
│   ├── deploy.py             # Deployment script
│   └── requirements.txt
├── backend/                   # FastAPI backend
│   ├── main.py               # API server + credit scoring
│   ├── document_verification.py  # Document upload system
│   ├── requirements.txt
│   └── tests/                # Unit tests
├── frontend-nextjs/           # Next.js 15 frontend
│   ├── app/                  # Next.js app router
│   ├── components/           # React components
│   ├── context/              # Wallet & WebSocket context
│   ├── utils/                # Helpers & services
│   └── public/               # Static assets & screenshots
└── docs/                      # Documentation
    └── DOCUMENT_VERIFICATION_SECURITY.md  # Privacy architecture
```

---

## 🎯 Roadmap

### ✅ Completed (Phase 1-3)
- Core lending smart contract
- 7-factor credit scoring
- Document verification (demo mode)
- Forced liquidation
- Real-time WebSocket updates
- Dark glassmorphism UI
- Educational tooltips
- 6 interactive charts

### 🚧 In Progress (Phase 4)
- Production document verification (OCR + identity APIs)
- Interest accrual on loans
- Liquidation visualization on charts
- Concurrent backend with thread safety
- Cross-browser compatibility testing

### 📋 Planned (Phase 5+)
- Multi-asset collateral (USDC, other ASAs)
- Flash loan protection
- Oracle integration (real price feeds)
- Governance token for platform decisions
- Mobile-responsive optimizations
- MainNet deployment

---

## 🤝 Contributing

This is a hackathon project built for the **Algorand DeFi Hackathon**. Contributions, issues, and feature requests are welcome!

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

---

## 📞 Support & Contact

- **AlgoExplorer:** [View Contract](https://testnet.algoexplorer.io/application/748013252)
- **Issues:** [GitHub Issues](https://github.com/yourusername/FiduciaLens/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/FiduciaLens/discussions)

---

<div align="center">

**Built with ❤️ for the Algorand Ecosystem**

*Making DeFi lending fair, transparent, and accessible to everyone*

[⬆ Back to Top](#-FiduciaLens---on-chain-credit-scoring--defi-lending-on-algorand)

</div>
