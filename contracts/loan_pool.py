"""
FiduciaLens Loan Pool Smart Contract
Implements core lending logic: deposit collateral, borrow, and repay
"""

from pyteal import *

def approval_program():
    """Main approval program for the loan pool contract"""
    
    # Define operation handlers
    on_creation = Seq([
        App.globalPut(Bytes("TotalCollateral"), Int(0)),
        App.globalPut(Bytes("TotalBorrow"), Int(0)),
        App.globalPut(Bytes("MaxLTV"), Int(50)),  # 50% max loan-to-value
        App.globalPut(Bytes("InterestRate"), Int(5)),  # 5% APR (simple linear)
        Approve()
    ])
    
    # Handle opt-in for local state
    on_opt_in = Seq([
        App.localPut(Txn.sender(), Bytes("Collateral"), Int(0)),
        App.localPut(Txn.sender(), Bytes("Debt"), Int(0)),
        App.localPut(Txn.sender(), Bytes("CreditScore"), Int(0)),
        App.localPut(Txn.sender(), Bytes("LastInterestUpdate"), Int(0)),  # Timestamp for interest calculation
        Approve()
    ])
    
    # Deposit collateral
    @Subroutine(TealType.uint64)
    def calculate_interest(principal, last_update):
        """Calculate accrued interest using simple linear rate (5% APR)"""
        # Interest = Principal * Rate * Time
        # Rate: 5% per year = 5/100 = 0.05
        # Time: seconds since last update / seconds in year
        # To avoid decimals: (principal * 5 * seconds_elapsed) / (100 * 31536000)
        # Simplified: (principal * seconds_elapsed) / 630720000
        
        seconds_elapsed = Global.latest_timestamp() - last_update
        interest = If(
            seconds_elapsed > Int(0),
            (principal * seconds_elapsed) / Int(630720000),  # 31536000 * 20 for more precision
            Int(0)
        )
        return interest
    
    # Deposit collateral
    @Subroutine(TealType.none)
    def deposit():
        """Deposit ALGO as collateral"""
        return Seq([
            # Ensure payment transaction is attached
            Assert(Gtxn[Txn.group_index() - Int(1)].type_enum() == TxnType.Payment),
            Assert(Gtxn[Txn.group_index() - Int(1)].receiver() == Global.current_application_address()),
            
            # Update global state
            App.globalPut(
                Bytes("TotalCollateral"), 
                App.globalGet(Bytes("TotalCollateral")) + Gtxn[Txn.group_index() - Int(1)].amount()
            ),
            
            # Update local state  
            App.localPut(
                Txn.sender(), 
                Bytes("Collateral"), 
                App.localGet(Txn.sender(), Bytes("Collateral")) + Gtxn[Txn.group_index() - Int(1)].amount()
            )
        ])
    
    # Borrow against collateral
    @Subroutine(TealType.none)
    def borrow():
        """Borrow ALGO against deposited collateral"""
        borrow_amount = Btoi(Txn.application_args[1])
        user_collateral = App.localGet(Txn.sender(), Bytes("Collateral"))
        user_debt = App.localGet(Txn.sender(), Bytes("Debt"))
        credit_score = Btoi(Txn.application_args[2]) if Txn.application_args.length() > Int(2) else Int(0)
        
        # Calculate max borrow based on LTV
        max_ltv = App.globalGet(Bytes("MaxLTV"))
        # Adjust LTV based on credit score (higher score = better terms)
        adjusted_ltv = If(
            credit_score >= Int(70),
            max_ltv + Int(10),  # 60% LTV for good credit
            max_ltv
        )
        
        max_borrow = (user_collateral * adjusted_ltv) / Int(100)
        
        return Seq([
            # Validate borrow amount
            Assert(borrow_amount > Int(0)),
            Assert(user_collateral > Int(0)),
            Assert(user_debt + borrow_amount <= max_borrow),
            
            # Store credit score if provided
            If(
                Txn.application_args.length() > Int(2),
                App.localPut(Txn.sender(), Bytes("CreditScore"), credit_score),
                Seq([])
            ),
            
            # Send borrowed ALGO to user
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: borrow_amount,
            }),
            InnerTxnBuilder.Submit(),
            
            # Update state
            App.globalPut(
                Bytes("TotalBorrow"), 
                App.globalGet(Bytes("TotalBorrow")) + borrow_amount
            ),
            App.localPut(
                Txn.sender(), 
                Bytes("Debt"), 
                user_debt + borrow_amount
            ),
            App.localPut(
                Txn.sender(),
                Bytes("LastInterestUpdate"),
                Global.latest_timestamp()
            ),
        ])
    
    # Repay debt
    @Subroutine(TealType.none)
    def repay():
        """Repay borrowed ALGO (with accrued interest)"""
        repay_amount = Gtxn[Txn.group_index() - Int(1)].amount()
        user_debt = App.localGet(Txn.sender(), Bytes("Debt"))
        last_update = App.localGet(Txn.sender(), Bytes("LastInterestUpdate"))
        
        # Calculate accrued interest
        accrued_interest = calculate_interest(user_debt, last_update)
        total_debt = user_debt + accrued_interest
        
        return Seq([
            # Ensure payment transaction is attached
            Assert(Gtxn[Txn.group_index() - Int(1)].type_enum() == TxnType.Payment),
            Assert(Gtxn[Txn.group_index() - Int(1)].receiver() == Global.current_application_address()),
            
            # Validate repayment
            Assert(repay_amount > Int(0)),
            Assert(repay_amount <= total_debt),
            
            # Update state
            App.globalPut(
                Bytes("TotalBorrow"), 
                App.globalGet(Bytes("TotalBorrow")) - repay_amount
            ),
            App.localPut(
                Txn.sender(), 
                Bytes("Debt"), 
                If(
                    repay_amount >= total_debt,
                    Int(0),  # Fully repaid
                    total_debt - repay_amount  # Partial repayment
                )
            ),
            App.localPut(
                Txn.sender(),
                Bytes("LastInterestUpdate"),
                Global.latest_timestamp()
            ),
        ])
    
    # Withdraw collateral
    @Subroutine(TealType.none)
    def withdraw():
        """Withdraw collateral after repaying debt"""
        withdraw_amount = Btoi(Txn.application_args[1])
        user_collateral = App.localGet(Txn.sender(), Bytes("Collateral"))
        user_debt = App.localGet(Txn.sender(), Bytes("Debt"))
        
        return Seq([
            # Can only withdraw if no debt
            Assert(user_debt == Int(0)),
            Assert(withdraw_amount > Int(0)),
            Assert(withdraw_amount <= user_collateral),
            
            # Send ALGO back to user
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: withdraw_amount,
            }),
            InnerTxnBuilder.Submit(),
            
            # Update state
            App.globalPut(
                Bytes("TotalCollateral"), 
                App.globalGet(Bytes("TotalCollateral")) - withdraw_amount
            ),
            App.localPut(
                Txn.sender(), 
                Bytes("Collateral"), 
                user_collateral - withdraw_amount
            )
        ])
    
    # Liquidate undercollateralized position
    @Subroutine(TealType.none)
    def liquidate():
        """Liquidate an undercollateralized position"""
        target_address = Txn.application_args[1]
        
        # Get target user's state
        target_collateral = App.localGet(target_address, Bytes("Collateral"))
        target_debt = App.localGet(target_address, Bytes("Debt"))
        
        # Calculate if position is liquidatable
        # LTV = (Debt / Collateral) * 100
        # Liquidatable if LTV > MaxLTV (default 50%)
        max_ltv = App.globalGet(Bytes("MaxLTV"))
        current_ltv = (target_debt * Int(100)) / target_collateral
        
        # Calculate liquidation penalty (10% of collateral goes to liquidator)
        liquidation_penalty = target_collateral / Int(10)
        collateral_to_pool = target_collateral - liquidation_penalty
        
        return Seq([
            # Validate liquidation conditions
            Assert(target_debt > Int(0)),
            Assert(target_collateral > Int(0)),
            Assert(current_ltv > max_ltv),  # Position must be underwater
            
            # Send penalty to liquidator
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: liquidation_penalty,
            }),
            InnerTxnBuilder.Submit(),
            
            # Update global state (collateral stays in pool to cover debt)
            App.globalPut(
                Bytes("TotalCollateral"), 
                App.globalGet(Bytes("TotalCollateral")) - liquidation_penalty
            ),
            App.globalPut(
                Bytes("TotalBorrow"), 
                App.globalGet(Bytes("TotalBorrow")) - target_debt
            ),
            
            # Clear user's position
            App.localPut(target_address, Bytes("Collateral"), Int(0)),
            App.localPut(target_address, Bytes("Debt"), Int(0)),
        ])
    
    # Main program logic
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.OptIn, on_opt_in],
        [Txn.on_completion() == OnComplete.CloseOut, Approve()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.application_args[0] == Bytes("deposit"), Seq([deposit(), Approve()])],
        [Txn.application_args[0] == Bytes("borrow"), Seq([borrow(), Approve()])],
        [Txn.application_args[0] == Bytes("repay"), Seq([repay(), Approve()])],
        [Txn.application_args[0] == Bytes("withdraw"), Seq([withdraw(), Approve()])],
        [Txn.application_args[0] == Bytes("liquidate"), Seq([liquidate(), Approve()])],
    )
    
    return program

def clear_state_program():
    """Clear state program - always approve"""
    return Approve()

if __name__ == "__main__":
    # Compile the contract
    with open("loan_pool_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=8)
        f.write(compiled)
    
    with open("loan_pool_clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=8)
        f.write(compiled)
    
    print("✅ Contract compiled successfully!")
    print("   - loan_pool_approval.teal")
    print("   - loan_pool_clear.teal")
