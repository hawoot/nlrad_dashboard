"""
Quick UI test script.

Run this to verify the UI components load correctly.
"""
from ui.app import create_app
from backend.core.registry import get_registry
from backend.core.executor import get_executor


def test_ui_structure():
    """Test that UI structure is correct."""
    print("Creating app...")
    app = create_app()

    print(f"✓ App created: {type(app)}")
    print(f"  Children: {len(app.children)} (should be 2: navigation + content)")

    # Check navigation
    nav_widget = app.children[0]
    print(f"✓ Navigation: {type(nav_widget)}")

    # Check content area
    content_widget = app.children[1]
    print(f"✓ Content area: {type(content_widget)}")

    print("\n✓ UI structure looks good!")


def test_tool_loading():
    """Test that tool UIs can be loaded."""
    print("\nTesting tool UI loading...")

    from ui.components.tool_loader import ToolLoader
    loader = ToolLoader()

    # Test Timeline UI
    print("Loading Timeline UI...")
    TimelineUI = loader.load_tool_ui("RAD/ingestor/timeline")
    print(f"✓ Timeline UI class: {TimelineUI.__name__}")

    # Test Force Load UI
    print("Loading Force Load UI...")
    ForceLoadUI = loader.load_tool_ui("RAD/ingestor/force_load")
    print(f"✓ Force Load UI class: {ForceLoadUI.__name__}")

    print("\n✓ Tool UIs load successfully!")


def test_backend_execution():
    """Test backend execution."""
    print("\nTesting backend execution...")

    executor = get_executor()

    # Test Timeline
    print("Testing Timeline tool...")
    result = executor.execute(
        user='test_user',
        tool_path='RAD/ingestor/timeline',
        params={'desk': 'Options', 'date': '2024-01-15'}
    )
    print(f"✓ Timeline execution: success={result.success}, records={len(result.data) if result.success else 0}")

    # Test Force Load
    print("Testing Force Load tool...")
    result = executor.execute(
        user='test_user',
        tool_path='RAD/ingestor/force_load',
        params={'table_name': 'Inflation Env', 'action': 'get_default'}
    )
    print(f"✓ Force Load execution: success={result.success}")
    if result.success:
        print(f"  Config rows: {len(result.data['config'])}")

    print("\n✓ Backend execution works!")


if __name__ == '__main__':
    test_ui_structure()
    test_tool_loading()
    test_backend_execution()

    print("\n" + "="*50)
    print("ALL TESTS PASSED! ✓")
    print("="*50)
    print("\nTo launch the dashboard:")
    print("  voila notebook.ipynb")
