#!/usr/bin/env python3
"""
Simple Configuration Test
========================

Test basic configuration imports without other dependencies.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))


def test_basic_imports():
    """Test basic imports"""
    print("🧪 Testing Basic Imports...")

    try:
        from tipm.config.settings import PolicyLayerConfig, TradeFlowConfig

        print("✅ Basic configuration imports successful")

        # Test creating objects
        policy = PolicyLayerConfig(
            name="test_policy", description="Test policy", enabled=True, weight=0.5
        )
        print("✅ PolicyLayerConfig creation successful")

        trade = TradeFlowConfig(
            name="test_trade", description="Test trade", enabled=True, threshold=0.6
        )
        print("✅ TradeFlowConfig creation successful")

        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


if __name__ == "__main__":
    success = test_basic_imports()
    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Tests failed!")
