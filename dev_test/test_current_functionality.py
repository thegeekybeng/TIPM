#!/usr/bin/env python3
"""
TIPM Current Functionality Test
===============================

This script tests the currently implemented components of the TIPM project
to verify functionality and identify any issues.
"""

import sys
from pathlib import Path
import logging

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_data_crawler():
    """Test data crawler functionality"""
    print("🕷️ Testing Data Crawler...")

    try:
        from data_crawler.core import DataCrawlerRAG
        from data_crawler.models import DataSource, DataSourceType
        from data_crawler.validators import DataQualityValidator, MLAnomalyDetector

        print("✅ Data crawler imports successful")

        # Test model creation
        validator = DataQualityValidator()
        print("✅ DataQualityValidator created successfully")

        anomaly_detector = MLAnomalyDetector()
        print("✅ MLAnomalyDetector created successfully")

        # Test data source creation
        test_source = DataSource(
            id="test_source",
            name="Test Data Source",
            description="A test data source for validation",
            source_type=DataSourceType.API,
            url="https://api.test.com",
        )
        print("✅ DataSource creation successful")

        # Test to_dict conversion
        source_dict = test_source.to_dict()
        print("✅ DataSource to_dict conversion successful")

        # Test from_dict conversion
        restored_source = DataSource.from_dict(source_dict)
        print("✅ DataSource from_dict conversion successful")

        print("✅ Data Crawler tests passed!")
        return True

    except Exception as e:
        print(f"❌ Data Crawler test failed: {e}")
        return False


def test_ml_models_import():
    """Test ML models import functionality"""
    print("🧠 Testing ML Models Import...")

    try:
        # Test if we can import the base structure
        from tipm.ml_models import MLModelManager

        print("✅ MLModelManager import successful")
        return True
    except ImportError as e:
        print(f"⚠️ ML Models not fully implemented yet: {e}")
        print("This is expected - ML models are in development")
        return False
    except Exception as e:
        print(f"❌ ML Models test failed: {e}")
        return False


def test_config_files():
    """Test configuration file accessibility"""
    print("⚙️ Testing Configuration Files...")

    config_files = [
        "tipm/config/settings.py",
        "tipm/config/layer_configs.py",
        "data_crawler/config/sources.json",
    ]

    all_good = True
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file} exists")
        else:
            print(f"⚠️ {config_file} not found")
            all_good = False

    return all_good


def test_requirements():
    """Test requirements.txt accessibility"""
    print("📦 Testing Requirements...")

    if Path("requirements.txt").exists():
        print("✅ requirements.txt exists")

        # Try to read it
        try:
            with open("requirements.txt", "r") as f:
                content = f.read()
                lines = content.strip().split("\n")
                print(f"✅ requirements.txt readable ({len(lines)} lines)")
                return True
        except Exception as e:
            print(f"❌ Error reading requirements.txt: {e}")
            return False
    else:
        print("❌ requirements.txt not found")
        return False


def test_project_structure():
    """Test overall project structure"""
    print("🏗️ Testing Project Structure...")

    expected_dirs = ["tipm", "data_crawler", "src", "tests"]

    expected_files = ["README.md", "setup.py", "package.json", "tailwind.config.js"]

    all_good = True

    # Check directories
    for dir_name in expected_dirs:
        if Path(dir_name).exists():
            print(f"✅ Directory {dir_name}/ exists")
        else:
            print(f"⚠️ Directory {dir_name}/ not found")
            all_good = False

    # Check files
    for file_name in expected_files:
        if Path(file_name).exists():
            print(f"✅ File {file_name} exists")
        else:
            print(f"⚠️ File {file_name} not found")
            all_good = False

    return all_good


def main():
    """Run all tests"""
    print("🎯 TIPM Project Functionality Test")
    print("=" * 50)

    test_results = []

    # Run tests
    test_results.append(("Project Structure", test_project_structure()))
    test_results.append(("Configuration Files", test_config_files()))
    test_results.append(("Requirements", test_requirements()))
    test_results.append(("Data Crawler", test_data_crawler()))
    test_results.append(("ML Models Import", test_ml_models_import()))

    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Project is ready for demo.")
    elif passed >= total * 0.8:
        print("⚠️ Most tests passed. Project is mostly ready.")
    else:
        print("❌ Several tests failed. Project needs attention.")

    print("\n📋 Next Steps:")
    if passed >= total * 0.8:
        print("1. Run the demo script: python demo_ml_models.py")
        print("2. Check the generated demo report")
        print("3. Review any warnings or issues")
    else:
        print("1. Fix the failing tests")
        print("2. Ensure all dependencies are installed")
        print("3. Verify project structure")

    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
