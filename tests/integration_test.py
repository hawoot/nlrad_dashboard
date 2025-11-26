"""
Integration test script to validate backend before UI development.

Run this script to ensure backend is working correctly:
    python tests/integration_test.py
"""
from backend.server import initialize_backend
from backend.core.executor import get_executor
from backend.core.registry import get_registry


def test_backend_initialization():
    """Test that backend initializes correctly."""
    print("Testing backend initialization...")
    initialize_backend()
    print("✓ Backend initialized successfully")


def test_tool_discovery():
    """Test that tools are discovered."""
    print("\nTesting tool discovery...")
    registry = get_registry()
    tools = registry.list_all_tools()

    print(f"✓ Discovered {len(tools)} tools:")
    for tool_path in tools:
        print(f"  - {tool_path}")


def test_timeline_tool():
    """Test timeline tool execution."""
    print("\nTesting timeline tool...")
    executor = get_executor()

    result = executor.execute(
        user="integration-test",
        tool_path="RAD/ingestor/timeline",
        params={
            'desk': 'Options',
            'date': '2024-01-15'
        }
    )

    if result.success:
        print("✓ Timeline tool executed successfully")
        print(f"  - Records: {result.data['summary']['total_records']}")
    else:
        print(f"✗ Timeline tool failed: {result.error_message}")
        return False

    return True


def test_force_load_tool():
    """Test force load tool execution."""
    print("\nTesting force load tool...")
    executor = get_executor()

    result = executor.execute(
        user="integration-test",
        tool_path="RAD/ingestor/force_load",
        params={
            'table_name': 'Inflation Env',
            'config_data': [
                {'configName': 'Config1', 'key': 'test.key', 'group': 'TEST'},
            ]
        }
    )

    if result.success:
        print("✓ Force load tool executed successfully")
        print(f"  - Rows processed: {result.data['rows_processed']}")
    else:
        print(f"✗ Force load tool failed: {result.error_message}")
        return False

    return True


def test_error_handling():
    """Test error handling."""
    print("\nTesting error handling...")
    executor = get_executor()

    # Test invalid desk
    result = executor.execute(
        user="integration-test",
        tool_path="RAD/ingestor/timeline",
        params={
            'desk': 'InvalidDesk',
            'date': '2024-01-15'
        }
    )

    if not result.success and result.error_type == "ParameterValidationError":
        print("✓ Parameter validation error handled correctly")
    else:
        print("✗ Error handling failed")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("BACKEND INTEGRATION TEST")
    print("=" * 60)

    try:
        test_backend_initialization()
        test_tool_discovery()
        timeline_ok = test_timeline_tool()
        force_ok = test_force_load_tool()
        error_ok = test_error_handling()

        print("\n" + "=" * 60)
        if timeline_ok and force_ok and error_ok:
            print("ALL TESTS PASSED ✓")
            print("Backend is ready for UI development!")
        else:
            print("SOME TESTS FAILED ✗")
            print("Please fix issues before proceeding to UI")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
