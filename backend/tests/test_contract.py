"""
FiduciaLens Smart Contract Test Suite
Tests PyTeal contract logic and compilation
"""
import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "contracts"))

from loan_pool import approval_program, clear_state_program

class TestContractCompilation:
    """Test contract compilation"""
    
    def test_approval_program_compiles(self):
        """Test that approval program compiles to TEAL"""
        try:
            teal = approval_program()
            assert teal is not None
            assert len(teal) > 0
            print(f"✅ Approval program compiled: {len(teal)} characters")
        except Exception as e:
            pytest.fail(f"Approval program compilation failed: {e}")
    
    def test_clear_state_program_compiles(self):
        """Test that clear state program compiles to TEAL"""
        try:
            teal = clear_state_program()
            assert teal is not None
            assert len(teal) > 0
            print(f"✅ Clear state program compiled: {len(teal)} characters")
        except Exception as e:
            pytest.fail(f"Clear state program compilation failed: {e}")
    
    def test_approval_teal_contains_operations(self):
        """Test that approval TEAL contains expected operations"""
        teal = approval_program()
        
        # Check for deposit operation
        assert "deposit" in teal or "Deposit" in teal, "Missing deposit operation"
        
        # Check for borrow operation
        assert "borrow" in teal or "Borrow" in teal, "Missing borrow operation"
        
        # Check for repay operation
        assert "repay" in teal or "Repay" in teal, "Missing repay operation"
        
        # Check for withdraw operation
        assert "withdraw" in teal or "Withdraw" in teal, "Missing withdraw operation"
        
        print("✅ All operations found in TEAL")
    
    def test_approval_teal_has_global_state(self):
        """Test that approval TEAL manages global state"""
        teal = approval_program()
        
        # Check for global state keys
        assert "TotalCollateral" in teal or "total_collateral" in teal, "Missing total collateral"
        assert "TotalBorrow" in teal or "total_borrow" in teal, "Missing total borrow"
        
        print("✅ Global state keys found")
    
    def test_approval_teal_has_local_state(self):
        """Test that approval TEAL manages local state"""
        teal = approval_program()
        
        # Check for local state keys
        assert "Collateral" in teal or "collateral" in teal, "Missing collateral"
        assert "Debt" in teal or "debt" in teal, "Missing debt"
        assert "CreditScore" in teal or "credit_score" in teal, "Missing credit score"
        
        print("✅ Local state keys found")


class TestContractLogic:
    """Test contract business logic"""
    
    def test_teal_files_exist(self):
        """Test that compiled TEAL files exist"""
        contracts_dir = Path(__file__).parent.parent.parent / "contracts"
        approval_file = contracts_dir / "loan_pool_approval.teal"
        clear_file = contracts_dir / "loan_pool_clear.teal"
        
        assert approval_file.exists(), f"Approval TEAL not found: {approval_file}"
        assert clear_file.exists(), f"Clear TEAL not found: {clear_file}"
        
        # Check file sizes
        approval_size = approval_file.stat().st_size
        clear_size = clear_file.stat().st_size
        
        assert approval_size > 0, "Approval TEAL is empty"
        assert clear_size > 0, "Clear TEAL is empty"
        
        print(f"✅ Approval TEAL: {approval_size} bytes")
        print(f"✅ Clear TEAL: {clear_size} bytes")


class TestContractSecurity:
    """Test contract security features"""
    
    def test_teal_has_txn_checks(self):
        """Test that TEAL performs transaction checks"""
        teal = approval_program()
        
        # Should check transaction types
        assert "txn" in teal.lower(), "Missing transaction checks"
        
        # Should check sender
        assert "sender" in teal.lower() or "Sender" in teal, "Missing sender checks"
        
        print("✅ Security checks found")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
