"""
Test script to verify complete UI functionality.
"""
import sys
from backend.server import initialize_backend
from backend.core.registry import get_registry
from backend.core.executor import get_executor
from ui.registry import get_tool_ui_class, TOOL_UI_MAP

print("=" * 70)
print("NLRAD Dashboard - Complete UI Test")
print("=" * 70)

# Test 1: Backend initialization
print("\n[1] Testing backend initialization...")
try:
    initialize_backend()
    registry = get_registry()
    executor = get_executor()
    print(f"✓ Backend initialized successfully")
    print(f"  - Registered tools: {len(registry.list_all_tools())}")
except Exception as e:
    print(f"✗ Backend initialization failed: {e}")
    sys.exit(1)

# Test 2: Tool registration
print("\n[2] Testing tool registration...")
try:
    tools = registry.list_all_tools()
    expected_tools = ['RAD/Ingestor/Timeline', 'RAD/Ingestor/Force Load']

    for tool_path in expected_tools:
        if tool_path in tools:
            print(f"✓ Tool registered: {tool_path}")
        else:
            print(f"✗ Missing tool: {tool_path}")
            sys.exit(1)
except Exception as e:
    print(f"✗ Tool registration test failed: {e}")
    sys.exit(1)

# Test 3: UI registry
print("\n[3] Testing UI registry...")
try:
    for tool_path in expected_tools:
        ui_class = get_tool_ui_class(tool_path)
        print(f"✓ UI class found for: {tool_path} -> {ui_class.__name__}")
except Exception as e:
    print(f"✗ UI registry test failed: {e}")
    sys.exit(1)

# Test 4: Timeline tool execution
print("\n[4] Testing Timeline tool execution...")
try:
    result = executor.execute(
        user='test_user',
        tool_path='RAD/Ingestor/Timeline',
        params={
            'desk': 'Options',
            'date': '2025-01-15'
        }
    )

    if result.success:
        records = result.data.get('records', [])
        print(f"✓ Timeline tool executed successfully")
        print(f"  - Returned {len(records)} records")
        if records:
            print(f"  - Sample record keys: {list(records[0].keys())}")
    else:
        print(f"✗ Timeline tool failed: {result.error_message}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Timeline tool test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Force Load tool - get default config
print("\n[5] Testing Force Load tool - get default config...")
try:
    result = executor.execute(
        user='test_user',
        tool_path='RAD/Ingestor/Force Load',
        params={
            'table_name': 'Inflation Env',
            'action': 'get_default'
        }
    )

    if result.success:
        config = result.data.get('config', [])
        print(f"✓ Force Load get_default executed successfully")
        print(f"  - Returned {len(config)} config rows")
        if config:
            print(f"  - Sample config keys: {list(config[0].keys())}")
    else:
        print(f"✗ Force Load get_default failed: {result.error_message}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Force Load get_default test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Force Load tool - dry run
print("\n[6] Testing Force Load tool - dry run...")
try:
    test_config = [
        {'configName': 'TestConfig1', 'key': 'test.key1', 'group': 'TEST'},
        {'configName': 'TestConfig2', 'key': 'test.key2', 'group': 'TEST'}
    ]

    result = executor.execute(
        user='test_user',
        tool_path='RAD/Ingestor/Force Load',
        params={
            'table_name': 'Inflation Env',
            'action': 'force_load',
            'config': test_config,
            'dry_run': True
        }
    )

    if result.success:
        records = result.data.get('records', [])
        print(f"✓ Force Load dry run executed successfully")
        print(f"  - Returned {len(records)} records")
        if records:
            expected_columns = ['configName', 'key', 'group', 'LastLoadedTS',
                              'ProcessTS', 'COB', 'LoadID', 'DataSourceWindows']
            actual_columns = list(records[0].keys())
            missing = set(expected_columns) - set(actual_columns)
            if missing:
                print(f"✗ Missing columns: {missing}")
                sys.exit(1)
            print(f"  - All expected columns present: {expected_columns}")
            print(f"  - Sample record: {records[0]}")
    else:
        print(f"✗ Force Load dry run failed: {result.error_message}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Force Load dry run test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Force Load tool - force load run
print("\n[7] Testing Force Load tool - force load run...")
try:
    result = executor.execute(
        user='test_user',
        tool_path='RAD/Ingestor/Force Load',
        params={
            'table_name': 'Options ScenarioGamma',
            'action': 'force_load',
            'config': test_config,
            'dry_run': False
        }
    )

    if result.success:
        records = result.data.get('records', [])
        print(f"✓ Force Load run executed successfully")
        print(f"  - Returned {len(records)} records")
    else:
        print(f"✗ Force Load run failed: {result.error_message}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Force Load run test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 8: UI component creation
print("\n[8] Testing UI component creation...")
try:
    from ui.tools.RAD.ingestor.timeline_ui import TimelineUI
    from ui.tools.RAD.ingestor.force_load_ui import ForceLoadUI

    timeline_ui = TimelineUI(executor, 'RAD/Ingestor/Timeline')
    print(f"✓ Timeline UI created successfully")
    print(f"  - Widget type: {type(timeline_ui.widget)}")

    force_load_ui = ForceLoadUI(executor, 'RAD/Ingestor/Force Load')
    print(f"✓ Force Load UI created successfully")
    print(f"  - Widget type: {type(force_load_ui.widget)}")
    print(f"  - Dry run default: {force_load_ui.dry_run_checkbox.value}")
    print(f"  - Button text: {force_load_ui.submit_button.description}")
except Exception as e:
    print(f"✗ UI component creation test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 9: DataFrame component
print("\n[9] Testing DataFrame component...")
try:
    import pandas as pd
    from ui.components.dataframe_table import create_dataframe_table

    test_df = pd.DataFrame([
        {'col1': 'A', 'col2': 'B', 'col3': 'C'},
        {'col1': 'D', 'col2': 'E', 'col3': 'F'},
    ])

    table_widget = create_dataframe_table(test_df, title="Test Table")
    print(f"✓ DataFrame component created successfully")
    print(f"  - Widget type: {type(table_widget)}")
except Exception as e:
    print(f"✗ DataFrame component test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("All tests passed! ✓")
print("=" * 70)
print("\nThe NLRAD Dashboard is ready to use.")
print("To start the dashboard, run the Jupyter notebook and execute:")
print("  from ui.app import create_app")
print("  app = create_app()")
print("  app")
