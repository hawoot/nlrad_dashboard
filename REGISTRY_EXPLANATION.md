# Registry System Explained

## Yes, there are TWO separate registries:

### 1. Backend Registry ([backend/core/registry.py](backend/core/registry.py))
**Purpose**: Maps tool paths to backend tool classes

**Location**: `backend/core/registry.py`

**What it does**:
- Registers all backend tools (the actual business logic)
- Maps tool paths like `'RAD/Ingestor/Timeline'` to tool classes like `TimelineTool`
- Used by the Executor to run tools

**Code**:
```python
# backend/core/registry.py
from backend.tools.RAD.ingestor.timeline_tool import TimelineTool
from backend.tools.RAD.ingestor.force_load_tool import ForceLoadTool

class ToolRegistry:
    def __init__(self):
        self._tools = {
            'RAD/Ingestor/Timeline': TimelineTool,
            'RAD/Ingestor/Force Load': ForceLoadTool,
        }
```

### 2. UI Registry ([ui/registry.py](ui/registry.py))
**Purpose**: Maps tool paths to UI classes

**Location**: `ui/registry.py`

**What it does**:
- Registers all UI components for tools
- Maps the SAME tool paths to UI classes like `TimelineUI`
- Used by ContentArea to load the right UI when user clicks a tool

**Code**:
```python
# ui/registry.py
from ui.tools.RAD.ingestor.timeline_ui import TimelineUI
from ui.tools.RAD.ingestor.force_load_ui import ForceLoadUI

TOOL_UI_MAP = {
    'RAD/Ingestor/Timeline': TimelineUI,
    'RAD/Ingestor/Force Load': ForceLoadUI,
}

def get_tool_ui_class(tool_path: str):
    return TOOL_UI_MAP[tool_path]
```

## Why Two Registries?

**Separation of Concerns**: Backend and UI are completely separate:
- Backend tools (in `backend/`) don't know about UI
- UI components (in `ui/`) don't import backend tools
- They only share the tool PATH as a common identifier

## How They Work Together

```
User clicks "Timeline" in navigation
         ↓
Navigation sends tool_path: 'RAD/Ingestor/Timeline'
         ↓
ContentArea.load_tool(tool_path='RAD/Ingestor/Timeline', executor)
         ↓
ContentArea uses UI Registry to find TimelineUI class
         ↓
Creates TimelineUI widget and displays it
         ↓
User fills in form and clicks "Query Timeline"
         ↓
TimelineUI calls executor.execute(tool_path='RAD/Ingestor/Timeline', params={...})
         ↓
Executor uses Backend Registry to find TimelineTool class
         ↓
Runs TimelineTool.run() and returns result
         ↓
TimelineUI displays the result
```

## Folder Structure

The tool path `'RAD/Ingestor/Timeline'` maps to:

**Backend**:
```
backend/tools/RAD/ingestor/timeline_tool.py
└── Contains: TimelineTool class
└── Registered in: backend/core/registry.py
```

**UI**:
```
ui/tools/RAD/ingestor/timeline_ui.py
└── Contains: TimelineUI class
└── Registered in: ui/registry.py
```

**Note**: The folder is lowercase `ingestor/`, but the display name in the tool path is capitalized `Ingestor`.

## Adding a New Tool

To add a new tool like `'RAD/Ingestor/Position'`:

1. **Backend** ([backend/tools/RAD/ingestor/position_tool.py](backend/tools/RAD/ingestor/position_tool.py)):
   ```python
   class PositionTool(BaseTool):
       category = "RAD/Ingestor"
       name = "Position"
       def run(self, context, ...):
           # business logic here
   ```

2. **Register Backend** ([backend/core/registry.py](backend/core/registry.py)):
   ```python
   from backend.tools.RAD.ingestor.position_tool import PositionTool

   self._tools = {
       'RAD/Ingestor/Timeline': TimelineTool,
       'RAD/Ingestor/Force Load': ForceLoadTool,
       'RAD/Ingestor/Position': PositionTool,  # ADD THIS
   }
   ```

3. **UI** ([ui/tools/RAD/ingestor/position_ui.py](ui/tools/RAD/ingestor/position_ui.py)):
   ```python
   class PositionUI:
       def __init__(self, executor, tool_path):
           self.executor = executor
           self.tool_path = tool_path
           self.widget = self._build_ui()
   ```

4. **Register UI** ([ui/registry.py](ui/registry.py)):
   ```python
   from ui.tools.RAD.ingestor.position_ui import PositionUI

   TOOL_UI_MAP = {
       'RAD/Ingestor/Timeline': TimelineUI,
       'RAD/Ingestor/Force Load': ForceLoadUI,
       'RAD/Ingestor/Position': PositionUI,  # ADD THIS
   }
   ```

That's it! Both registries use the same tool path as the key, so they stay in sync.
