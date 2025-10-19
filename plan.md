🧠 1️⃣ Project Overview (what you’ll demo)

Title: FiduciaLens — On-Chain Credit Scoring & Collateral Stability Dashboard on Algorand
Goal: Enable fairer DeFi lending by combining:

On-chain credit scoring (based on wallet activity + verified claims)

Collateral stability visualizer (show how volatile assets impact pool health)

Smart contracts on Algorand for lending logic (collateral, loans, repayments)

⚙️ 2️⃣ Technical Stack (finalized for hackathon)
Layer	Technology	Reason
Smart Contracts	PyTeal (Algorand)	Compiles to TEAL, easiest for hackathon use
Blockchain APIs	Algorand Python SDK, Algorand Indexer	For on-chain reads, state sync, and testnet deployment
Backend	Python FastAPI	Lightweight REST API to compute scores + sign attestations
Frontend	React + Tailwind	Fast UI dev + wallet integration
Wallet	Pera Wallet / WalletConnect	Algorand testnet wallet support
Data Visualization	Recharts / D3.js	Render collateral health, risk indicators
Deployment	Algorand TestNet, optional Vercel for frontend	Demo-ready setup
🩻 3️⃣ Feature Priority Breakdown (time-based)
Tier 1 — Essential (core MVP, must be demo-ready)

Estimated: 10–12 hours total

Feature	Purpose	Implementation Plan
🟢 Lending Smart Contract (minimal)	Core logic for collateral deposit, borrow, repay	PyTeal: stateful contract with 3 actions → deposit (collateral ASA), borrow (record debt, emit event), repay (clear debt). Keep all logic integer-based, no interest compounding.
🟢 Credit Scoring (off-chain)	Compute trust score	Python script: fetch wallet’s txn history via Indexer, simple heuristics (wallet age, number of successful transactions, repayment txns). Return normalized score 0–100.
🟢 Signed Credit Attestation	Verify user reliability	Server (FastAPI): after computing score, sign {address, score, expiry} with private key. Smart contract verifies signature when applying loan terms.
🟢 Frontend Wallet Connect	User interacts with testnet	React app with Pera Wallet integration. Display address, balance, connect/disconnect button.
🟢 Basic Dashboard UI	Unified control panel	Tabs: Score Summary, Borrow/Lend, Collateral Visualizer. Read state from backend (loan totals, collateral ratio).
Tier 2 — Secondary (adds demo polish & credibility)

Estimated: 5–6 hours

Feature	Purpose	Implementation Plan
🟡 Collateral Stability Visualizer	Show pool health dynamically	Frontend chart: pool utilization = totalBorrow / totalCollateral. Simulate 20–50% price drops with slider → display new ratios and liquidation thresholds.
🟡 Oracle Mock (Off-chain feed)	Simulate collateral price fluctuations	Server endpoint: fetch a token’s real-world price (e.g., from CoinGecko) every minute, push to smart contract global state using a signed txn (optional).
🟡 Score Weight Integration	Dynamic LTV based on credit score	PyTeal: before allowing borrow, check credit score claim; lower collateral requirement if score ≥ threshold.
🟡 Event Listener	Real-time contract updates	Backend listens for events via Indexer or Algod WebSocket, pushes updates to UI.
Tier 3 — Stretch Goals (only if >4 hours remain)
Feature	Purpose	Implementation Plan
🟠 Document Verification	Off-chain doc upload (optional KYC)	Integrate simple OCR + signed claim verifying “identity verified”. Link claim hash to credit score.
🟠 Oracle Anomaly Detector	Highlight price discrepancies	Compare mock price feed vs TWAP from Indexer; trigger alert on >5% deviation.
🟠 SBT-like Proof Token	Permanent on-chain credit proof	ASA token with metadata storing score & expiry, non-transferable logic.
🟠 Multi-collateral Pool	Allow multiple ASAs	Add mapping for asset types (1–2 max).
🔩 4️⃣ Smart Contract Scaffold (PyTeal Structure)

Contract name: LoanPool.py

# global state keys: TotalCollateral, TotalBorrow
# local state per user: Collateral, Debt

def approval_program():
    handle_noop = Seq([
        Cond(
            [Txn.application_args[0] == Bytes("deposit"), deposit()],
            [Txn.application_args[0] == Bytes("borrow"), borrow()],
            [Txn.application_args[0] == Bytes("repay"), repay()]
        )
    ])
    return handle_noop

def deposit():
    return Seq([
        App.globalPut(Bytes("TotalCollateral"), App.globalGet(Bytes("TotalCollateral")) + Txn.amount()),
        App.localPut(Txn.sender(), Bytes("Collateral"), Txn.amount()),
        Approve()
    ])

def borrow():
    return Seq([
        # verify signed claim (credit score)
        Assert(verify_claim(Txn.application_args[1])),
        App.globalPut(Bytes("TotalBorrow"), App.globalGet(Bytes("TotalBorrow")) + Btoi(Txn.application_args[2])),
        App.localPut(Txn.sender(), Bytes("Debt"), Btoi(Txn.application_args[2])),
        Approve()
    ])

def repay():
    return Seq([
        App.globalPut(Bytes("TotalBorrow"), App.globalGet(Bytes("TotalBorrow")) - App.localGet(Txn.sender(), Bytes("Debt"))),
        App.localPut(Txn.sender(), Bytes("Debt"), Int(0)),
        Approve()
    ])


(Verification stub can be simplified or mocked in demo.)

🧰 5️⃣ Implementation Plan (hour-by-hour outline)
Time Remaining	Tasks	Deliverable
T–21h → T–17h (4h)	Set up Algorand sandbox/testnet, wallet, SDKs, Git repo. Implement & deploy minimal PyTeal smart contract (deposit/borrow/repay).	On-chain contract + verified deployment
T–17h → T–13h (4h)	Write FastAPI backend: scoring endpoint, signature endpoint. Test signed claims.	Working backend + signed attestation JSON
T–13h → T–8h (5h)	Build React frontend: connect wallet, show balance, fetch credit score from backend, call borrow function.	UI + working wallet + transactions
T–8h → T–4h (4h)	Add Collateral Visualizer (chart from pool state), optional oracle price fetcher.	Real-time visual graph
T–4h → T–2h (2h)	End-to-end demo polish, record screen flow, fix state sync.	Polished demo
T–2h → Submission	Prepare README + short explainer slides/video.	Submission-ready
🔐 6️⃣ Safety / Security Priorities for Hackathon

Validate all smart contract inputs (non-negative values, sufficient collateral).

Cap borrowing relative to collateral ratio (e.g., max 50% LTV).

Avoid admin key control.

Keep oracle inputs manual or trusted (mocked) to avoid vulnerabilities.

Never store personal data or documents on-chain — store hashes only.