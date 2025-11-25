
# 📘 Dashboard Application - Complete Architecture Document

## Executive Summary

A professional web dashboard application replacing spreadsheet-based workflows for 50-100 traders at JPMorgan Chase. Built with Voila + ipywidgets for UI, structured backend for business logic, comprehensive logging for debugging, and clean architectural separation.

**Key principles:**
- Crystal clear layer separation (UI ↔ Service ↔ Tools ↔ Models)
- All code in Python scripts (notebook only calls entry point)
- Dynamic tool discovery and navigation
- Comprehensive logging for production support
- Professional, slick UI
- No architectural soup

---

## Project Structure

```
dashboard/
│
├── notebook.ipynb                  # ONLY contains: from ui.app import create_app
│
├── backend/                        # Business logic layer
│   ├── core/                       # Infrastructure
│   │   ├── __init__.py
│   │   ├── base_tool.py           # Tool interface contract
│   │   ├── registry.py            # Tool discovery & cataloguing
│   │   ├── executor.py            # Execution orchestration + logging
│   │   ├── model_loader.py        # Shared resource management
│   │
│   ├── models/                     # Domain logic
│   │   ├── __init__.py
│   │   ├── ingestor_timeline.py   # Timeline business logic
│   │   ├── ingestor_force.py      # Force load business logic
│   │
│   ├── tools/                      # Executable units
│   │   ├── __init__.py
│   │   ├── RAD/
│   │   │   ├── __init__.py
│   │   │   ├── ingestor/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── timeline_tool.py
│   │   │   │   ├── force_load_tool.py
│   │   │
│   │   ├── DD/
│   │       ├── __init__.py
│   │
│   ├── lib/                        # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py              # Logging configuration
│   │   ├── errors.py              # Error types
│   │   ├── result.py              # Result wrapper
│   │   ├── user.py                # User identification
│   │
│   ├── server.py                   # Backend bootstrap
│
├── ui/                             # Frontend layer
│   ├── __init__.py
│   ├── app.py                     # Main entry point
│   │
│   ├── components/                 # Reusable UI components
│   │   ├── __init__.py
│   │   ├── navigation.py          # Sidebar accordion navigation
│   │   ├── content_area.py        # Main content container
│   │   ├── tool_loader.py         # Dynamic tool UI loading
│   │   ├── error_display.py       # Error message rendering
│   │
│   ├── tools/                      # Tool-specific UIs
│   │   ├── __init__.py
│   │   ├── RAD/
│   │   │   ├── __init__.py
│   │   │   ├── ingestor/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── timeline_ui.py
│   │   │   │   ├── force_load_ui.py
│   │   │
│   │   ├── DD/
│   │       ├── __init__.py
│   │
│   ├── lib/                        # UI utilities
│   │   ├── __init__.py
│   │   ├── widget_factory.py      # Reusable widget builders
│   │   ├── layout_helpers.py      # Layout patterns
│   │
│   ├── styles/                     # Visual design
│       ├── __init__.py
│       ├── theme.py               # Colors, fonts, spacing
│
├── config/                         # Configuration
│   ├── __init__.py
│   ├── settings.py                # Application settings
│
├── requirements.txt
└── README.md
```

---

## Architecture Layers

### Layer Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  Notebook (notebook.ipynb)                                  │
│  - Calls: from ui.app import create_app                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  UI Layer (ui/)                                             │
│  - app.py: Main layout orchestration                        │
│  - components/: Navigation, content area, error display     │
│  - tools/: Tool-specific UIs (forms + result rendering)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Service Layer (backend/core/executor.py)                   │
│  - Single entry point for all tool executions               │
│  - Logging with context (user, request_id, params)          │
│  - Error handling and Result wrapping                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Tool Layer (backend/tools/)                                │
│  - Thin adapters between UI and models                      │
│  - Parameter validation                                     │
│  - Model coordination                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Model Layer (backend/models/)                              │
│  - Rich domain objects with business logic                  │
│  - Database queries                                         │
│  - Data transformation                                      │
│  - Calculations                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Infrastructure (backend/core/)                             │
│  - Registry: Tool discovery                                 │
│  - ModelLoader: Shared resources (DB, cache)                │
│  - Logger: Structured logging                               │
└─────────────────────────────────────────────────────────────┘
```

**Key rule:** Each layer only talks downward. No upward or sideways dependencies.

---

## Backend Architecture

### backend/core/base_tool.py

**Purpose:** Defines the contract that all tools must implement.

**Contains:**
- `ExecutionContext` dataclass: Carries request_id, user, timestamp, logger, params
- `BaseTool` abstract base class: Interface for all tools

**Key elements:**
```python
@dataclass
class ExecutionContext:
    request_id: str          # UUID for tracing
    user: str                # For logging and audit
    timestamp: datetime      # When execution started
    tool_path: str          # e.g., "RAD/ingestor/timeline"
    params: Dict[str, Any]  # Input parameters
    logger: Logger          # Pre-configured with context

class BaseTool(ABC):
    category: str           # e.g., "RAD/ingestor"
    name: str              # e.g., "timeline"
    description: str       # Human-readable description
    
    @abstractmethod
    def run(self, context: ExecutionContext, **params) -> Any:
        """Execute tool logic. Return plain Python objects."""
        pass
    
    @property
    def full_path(self) -> str:
        """Returns category/name"""
        pass
```

**Responsibilities:**
- Define execution context structure
- Enforce tool interface
- Provide metadata access

**Does NOT:**
- Contain business logic
- Handle errors (executor does)
- Know about UI

---

### backend/core/registry.py

**Purpose:** Auto-discovers all tools and provides hierarchical structure for navigation.

**Key class:**
```python
class Registry:
    def __init__(self):
        self._tools: Dict[str, Type[BaseTool]] = {}
        self._structure: Dict[str, Dict] = {}
        self._discover_tools()
```

**Public methods:**
- `get_tool(path: str) -> BaseTool`: Instantiate a tool by path
- `get_categories() -> List[str]`: Top-level categories (["RAD", "DD"])
- `get_subcategories(category: str) -> List[str]`: Subcategories under a category
- `get_tools_in_category(category: str) -> List[str]`: Tool names in a category
- `get_structure() -> Dict`: Full hierarchical structure for UI

**How discovery works:**
1. Walks `backend/tools/` directory tree
2. Imports all Python modules
3. Finds classes inheriting from `BaseTool`
4. Registers them with their full path
5. Builds hierarchical structure dictionary

**Structure format:**
```python
{
    'RAD': {
        'ingestor': {
            '_tools': ['timeline', 'force_load']
        },
        'pricing': {
            '_tools': ['curve_builder']
        }
    },
    'DD': {
        # ...
    }
}
```

**Singleton pattern:** Loaded once per process via `get_registry()` function.

**Responsibilities:**
- Tool discovery
- Path resolution
- Navigation structure provision

**Does NOT:**
- Execute tools
- Handle errors
- Manage state

**Failure modes:**
- Raises `ValueError` on duplicate tool paths
- Import errors during discovery are propagated

---

### backend/core/executor.py

**Purpose:** Central orchestration point for all tool executions. Handles logging, error handling, context management.

**Key class:**
```python
class ToolExecutor:
    def __init__(self):
        self.registry = get_registry()
    
    def execute(
        self, 
        user: str, 
        tool_path: str, 
        params: Dict[str, Any]
    ) -> Result:
        """Execute a tool with full observability"""
```

**Execution flow:**
1. Generate unique request_id (UUID)
2. Create ExecutionContext with logger
3. Log execution start with all context
4. Resolve tool from registry
5. Call tool.run(context, **params)
6. Log execution completion with duration
7. Return Result.success(data)

**Error handling:**
- `ToolNotFoundError`: Tool path doesn't exist → Return error Result
- `ToolExecutionError`: Expected business errors → Log warning, return error Result
- `Exception`: Unexpected errors → Log error with traceback, return error Result

**Logging structure:**
```python
logger.info("Tool execution started", extra={
    "request_id": "uuid",
    "user": "nidhal.benmaghnia",
    "tool_path": "RAD/ingestor/timeline",
    "params": {...}
})
```

**Singleton pattern:** Accessed via `get_executor()` function.

**Responsibilities:**
- Single entry point for tool execution
- Request ID generation
- Context creation
- Structured logging
- Error catching and wrapping
- Execution timing

**Does NOT:**
- Contain business logic
- Know about UI
- Store state between executions

---

### backend/core/model_loader.py

**Purpose:** Manages shared resources that are expensive to create (DB connections, caches, configs).

**Pattern:**
```python
class ModelLoader:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str, factory: Callable) -> Any:
        """Get or create a resource"""
        if key not in self._cache:
            self._cache[key] = factory()
        return self._cache[key]
```

**Usage example:**
```python
loader = get_model_loader()
db = loader.get("db", lambda: create_db_connection())
```

**Responsibilities:**
- Load-once pattern for expensive resources
- Process-level caching
- Lazy initialization

**Does NOT:**
- Store per-user data
- Store per-request data
- Handle cleanup (assumes long-lived process)

---

### backend/models/

**Purpose:** Rich domain objects containing business logic.

**Example: ingestor_timeline.py**
```python
class IngestorTimelineModel:
    def __init__(self):
        self.db = get_model_loader().get("db", create_db_connection)
    
    def fetch_data(self, start: datetime, end: datetime) -> List[Dict]:
        """Query timeline data from database"""
        # DB query logic
        
    def process(self, raw_data: List[Dict]) -> Dict:
        """Transform and analyze timeline data"""
        # Business logic: aggregations, calculations, etc.
        
    def calculate_metrics(self, processed: Dict) -> Dict:
        """Compute key metrics"""
        # Domain calculations
```

**Characteristics:**
- Self-contained domain logic
- No UI dependencies
- No tool dependencies
- Pure Python data structures in/out
- Can use shared resources via model_loader

**Responsibilities:**
- Database queries
- Data transformations
- Business calculations
- Domain rules

**Does NOT:**
- Know about tools
- Know about UI
- Handle HTTP/serialization
- Manage execution context

---

### backend/tools/

**Purpose:** Thin adapters connecting UI → backend logic.

**Directory structure matches categories:**
```
tools/
    RAD/
        ingestor/
            timeline_tool.py
            force_load_tool.py
        pricing/
            curve_builder_tool.py
    DD/
        ...
```

**Example: timeline_tool.py**
```python
from backend.core.base_tool import BaseTool, ExecutionContext
from backend.models.ingestor_timeline import IngestorTimelineModel
from backend.lib.errors import ParameterValidationError
from datetime import datetime

class TimelineTool(BaseTool):
    category = "RAD/ingestor"
    name = "timeline"
    description = "Query and analyze ingestor timeline data"
    
    def run(self, context: ExecutionContext, start: str, end: str):
        # 1. Validate parameters
        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
        except ValueError as e:
            raise ParameterValidationError(
                f"Invalid date format: {e}",
                user_message="Please provide dates in YYYY-MM-DD format"
            )
        
        if start_dt >= end_dt:
            raise ParameterValidationError(
                "Start date must be before end date"
            )
        
        # 2. Log
        context.logger.info(f"Fetching timeline data from {start} to {end}")
        
        # 3. Delegate to model
        model = IngestorTimelineModel()
        raw_data = model.fetch_data(start_dt, end_dt)
        
        context.logger.info(f"Fetched {len(raw_data)} records")
        
        # 4. Process and return
        processed = model.process(raw_data)
        
        context.logger.info("Timeline processing complete")
        
        return processed
```

**Responsibilities:**
- Parameter validation
- Type conversion (strings → proper types)
- Model coordination
- Strategic logging points
- Return plain data structures

**Does NOT:**
- Contain business logic (models do)
- Render UI (tool UIs do)
- Handle errors globally (executor does)

---

### backend/lib/errors.py

**Purpose:** Define application-specific error types.

**Error hierarchy:**
```python
class ToolExecutionError(Exception):
    """Expected errors during tool execution"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.user_message = user_message or message

class ToolNotFoundError(Exception):
    """Tool path doesn't exist in registry"""
    pass

class ParameterValidationError(ToolExecutionError):
    """Invalid parameters passed to tool"""
    pass

class DataAccessError(ToolExecutionError):
    """Database or data source errors"""
    pass
```

**Usage pattern:**
- Tools raise specific errors for expected failures
- Executor catches and wraps them in Result objects
- UI displays user_message, logs full message + traceback

---

### backend/lib/result.py

**Purpose:** Wrapper for tool execution results. Makes success/failure explicit without exceptions reaching UI.

**Structure:**
```python
@dataclass
class Result:
    success: bool
    data: Optional[Any] = None
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    user_message: Optional[str] = None
    request_id: Optional[str] = None
    traceback: Optional[str] = None
    
    @staticmethod
    def success(data: Any, request_id: str) -> 'Result':
        """Create success result"""
        
    @staticmethod
    def error(
        message: str,
        request_id: str,
        error_type: str,
        user_message: Optional[str] = None,
        traceback: Optional[str] = None
    ) -> 'Result':
        """Create error result"""
```

**Usage in UI:**
```python
result = executor.execute(user, tool_path, params)

if result.success:
    display_data(result.data)
else:
    show_error(result.user_message, result.request_id)
    # Optionally log full traceback for debugging
```

---

### backend/lib/user.py

**Purpose:** User identification for logging and audit.

**Key function:**
```python
def get_current_user() -> str:
    """
    Get current user identifier.
    
    Strategies (in order):
    1. Check environment variable USER_ID
    2. Check system username
    3. Return "unknown"
    """
    return os.environ.get('USER_ID') or \
           os.environ.get('USER') or \
           "unknown"
```

**Usage:**
```python
from backend.lib.user import get_current_user

result = executor.execute(
    user=get_current_user(),
    tool_path="RAD/ingestor/timeline",
    params={...}
)
```

---

### backend/lib/logger.py

**Purpose:** Configure structured logging with context.

**Key function:**
```python
def get_logger(tool_path: str, user: str, request_id: str) -> Logger:
    """
    Create logger with pre-configured context.
    
    All log statements from this logger will include:
    - tool_path
    - user
    - request_id
    """
```

**Configuration:**
- Structured JSON logging
- Timestamped
- Includes context in every log line
- Configurable log level
- Output to console/file

**Note:** Details of lib.logger will be discussed during implementation phase.

---

### backend/server.py

**Purpose:** Bootstrap the backend. Initialize shared resources.

**Responsibilities:**
```python
def initialize_backend():
    """
    Initialize backend infrastructure:
    1. Load configuration
    2. Initialize database connections
    3. Warm up registry (discover tools)
    4. Configure logging
    5. Preload any heavy resources
    """
```

**Called by:** `ui/app.py` during application startup.

---

## Frontend Architecture

### ui/app.py

**Purpose:** Main entry point. Creates application layout and wires everything together.

**Key function:**
```python
def create_app():
    """
    Create and return the main application widget.
    This is the ONLY function called from the notebook.
    
    Returns:
        ipywidgets.Widget: Main application layout
    """
    # 1. Initialize backend
    initialize_backend()
    
    # 2. Get singleton instances
    registry = get_registry()
    executor = get_executor()
    
    # 3. Create components
    navigation = Navigation(registry)
    content_area = ContentArea()
    
    # 4. Wire navigation → content
    def on_tool_selected(tool_path):
        content_area.load_tool(tool_path, executor)
    
    navigation.on_tool_selected(on_tool_selected)
    
    # 5. Create layout
    main_layout = HBox([
        navigation.widget,
        content_area.widget
    ])
    
    # 6. Apply styling
    apply_theme(main_layout)
    
    return main_layout
```

**Responsibilities:**
- Backend initialization
- Component instantiation
- Event wiring
- Layout creation
- Theme application

**Does NOT:**
- Contain widget implementation
- Execute tools
- Handle results

**Notebook usage:**
```python
from ui.app import create_app

app = create_app()
display(app)
```

---

### ui/components/navigation.py

**Purpose:** Sidebar navigation with accordion/tree structure.

**Key class:**
```python
class Navigation:
    def __init__(self, registry):
        self.registry = registry
        self.callbacks = []
        self.widget = self._build_navigation()
    
    def _build_navigation(self):
        """Build accordion from registry structure"""
        structure = self.registry.get_structure()
        # Create Accordion widget with categories
        # Each category expands to show subcategories
        # Each subcategory shows tools as clickable items
    
    def on_tool_selected(self, callback):
        """Register callback for when user clicks a tool"""
        self.callbacks.append(callback)
    
    def _emit_tool_selected(self, tool_path):
        """Call all registered callbacks"""
        for callback in self.callbacks:
            callback(tool_path)
```

**Visual structure:**
```
┌──────────────────────┐
│ ▼ RAD                │
│   ▼ ingestor         │
│     • timeline       │ ← Clickable
│     • force_load     │ ← Clickable
│   ▶ pricing          │
│ ▶ DD                 │
└──────────────────────┘
```

**Responsibilities:**
- Query registry for structure
- Render accordion UI
- Handle expand/collapse
- Emit tool selection events

**Does NOT:**
- Execute tools
- Render tool UIs
- Display results

---

### ui/components/content_area.py

**Purpose:** Main content panel. Displays tool UIs and results.

**Key class:**
```python
class ContentArea:
    def __init__(self):
        self.widget = VBox()
        self.current_tool_ui = None
    
    def load_tool(self, tool_path: str, executor):
        """Load and display tool UI"""
        self.show_loading()
        
        tool_ui = load_tool_ui(tool_path, executor)
        self.current_tool_ui = tool_ui
        
        self.widget.children = [tool_ui.widget]
    
    def show_loading(self):
        """Display loading spinner"""
        self.widget.children = [
            HTML("<div class='loading'>Loading...</div>")
        ]
    
    def clear(self):
        """Clear content"""
        self.widget.children = []
```

**Responsibilities:**
- Container management
- Tool UI loading
- Loading state display

**Does NOT:**
- Implement tool UIs
- Execute tools
- Handle errors (tool UIs do)

---

### ui/components/tool_loader.py

**Purpose:** Dynamically load tool-specific UI modules.

**Key function:**
```python
def load_tool_ui(tool_path: str, executor) -> ToolUI:
    """
    Load the UI for a given tool.
    
    Args:
        tool_path: e.g., "RAD/ingestor/timeline"
        executor: Backend executor instance
        
    Returns:
        Tool UI instance
        
    Process:
        1. Convert path to module: "RAD/ingestor/timeline" 
           → "ui.tools.RAD.ingestor.timeline_ui"
        2. Import module
        3. Get UI class (e.g., TimelineUI)
        4. Instantiate with executor
        5. Return instance
    """
    # Convert path to module path
    module_path = f"ui.tools.{tool_path.replace('/', '.')}_ui"
    
    try:
        module = importlib.import_module(module_path)
        
        # Convention: UI class is CapitalizedToolName + "UI"
        # e.g., timeline → TimelineUI, force_load → ForceLoadUI
        class_name = _path_to_class_name(tool_path)
        ui_class = getattr(module, class_name)
        
        return ui_class(executor, tool_path)
        
    except (ImportError, AttributeError) as e:
        raise UINotFoundError(
            f"No UI found for tool: {tool_path}. "
            f"Expected: {module_path}.{class_name}"
        )
```

**Naming convention:**
- Tool: `timeline_tool.py` → class `TimelineTool`
- UI: `timeline_ui.py` → class `TimelineUI`

**Responsibilities:**
- Dynamic module import
- UI class instantiation
- Error handling for missing UIs

---

### ui/components/error_display.py

**Purpose:** Consistent error message rendering.

**Key function:**
```python
def create_error_widget(result: Result) -> Widget:
    """
    Create styled error display from Result object.
    
    Shows:
    - User-friendly message
    - Request ID for support
    - Optionally: full error details (collapsed)
    """
    return VBox([
        HTML(f"<div class='error-alert'>{result.user_message}</div>"),
        HTML(f"<div class='request-id'>Request ID: {result.request_id}</div>"),
        # Expandable details section
        create_details_section(result) if result.traceback else None
    ])
```

**Visual design:**
```
┌────────────────────────────────────────┐
│ ⚠️ An error occurred                   │
│                                        │
│ Please provide dates in YYYY-MM-DD     │
│ format                                 │
│                                        │
│ Request ID: 550e8400-e29b-41d4-a716... │
│ [Show Details ▼]                       │
└────────────────────────────────────────┘
```

---

### ui/tools/RAD/ingestor/timeline_ui.py

**Purpose:** Custom UI for timeline tool. Parameter form + result rendering.

**Structure:**
```python
class TimelineUI:
    def __init__(self, executor, tool_path):
        self.executor = executor
        self.tool_path = tool_path
        
        # Create widgets
        self.start_date = create_date_picker("Start Date")
        self.end_date = create_date_picker("End Date")
        self.submit_button = create_submit_button("Run Query", self._on_submit)
        self.result_area = VBox()
        
        # Build layout
        self.widget = self._build_ui()
    
    def _build_ui(self):
        """Build the complete UI"""
        return VBox([
            HTML("<h2>Timeline Query</h2>"),
            HTML("<p>Query ingestor timeline data for analysis</p>"),
            
            # Parameter form
            create_form_layout([
                self.start_date,
                self.end_date
            ]),
            
            self.submit_button,
            
            # Results area
            self.result_area
        ])
    
    def _on_submit(self, button):
        """Handle form submission"""
        # Get parameters
        params = {
            'start': self.start_date.value.isoformat(),
            'end': self.end_date.value.isoformat()
        }
        
        # Show loading
        self.result_area.children = [HTML("<div class='loading'>Running query...</div>")]
        
        # Execute tool
        result = self.executor.execute(
            user=get_current_user(),
            tool_path=self.tool_path,
            params=params
        )
        
        # Display result
        if result.success:
            self._render_result(result.data)
        else:
            self._show_error(result)
    
    def _render_result(self, data):
        """Render timeline-specific result"""
        # Custom visualization for timeline data
        # Could include: tables, charts, summaries
        self.result_area.children = [
            HTML("<h3>Results</h3>"),
            create_data_table(data['records']),
            create_summary_panel(data['metrics']),
            create_timeline_chart(data['timeline'])
        ]
    
    def _show_error(self, result):
        """Display error"""
        self.result_area.children = [create_error_widget(result)]
```

**Responsibilities:**
- Parameter form creation
- Form validation (basic UI-level)
- Executor invocation
- Result rendering (tool-specific)
- Error display

**Does NOT:**
- Contain business logic
- Access backend models directly
- Manage navigation

---

### ui/lib/widget_factory.py

**Purpose:** Reusable widget builders with consistent styling.

**Key functions:**
```python
def create_date_picker(label: str, default: Optional[date] = None) -> DatePicker:
    """Create styled date picker with label"""
    
def create_dropdown(
    label: str, 
    options: List[str], 
    default: Optional[str] = None
) -> Dropdown:
    """Create styled dropdown with label"""
    
def create_text_input(label: str, placeholder: str = "") -> Text:
    """Create styled text input with label"""
    
def create_submit_button(text: str, on_click: Callable) -> Button:
    """Create styled submit button"""
    
def create_data_table(data: pd.DataFrame) -> Widget:
    """Create professional data table"""
    
def create_chart(chart_type: str, data: Dict) -> Widget:
    """Create chart (using plotly or similar)"""
```

**Benefits:**
- Consistent styling across all tools
- Reduces boilerplate
- Centralized style updates

---

### ui/lib/layout_helpers.py

**Purpose:** Common layout patterns.

**Key functions:**
```python
def create_form_layout(fields: List[Widget]) -> VBox:
    """
    Create 2-column form layout:
    Label | Input
    Label | Input
    """
    
def create_sidebar_layout(sidebar: Widget, content: Widget) -> HBox:
    """
    Create sidebar + content layout with proper spacing:
    [Sidebar | Content          ]
    """
    
def create_card(title: str, content: Widget) -> VBox:
    """
    Create card with title and content:
    ┌──────────────┐
    │ Title        │
    ├──────────────┤
    │ Content      │
    └──────────────┘
    """
    
def create_tabs(tabs: Dict[str, Widget]) -> Tab:
    """Create tabbed interface"""
```

---

### ui/styles/theme.py

**Purpose:** Visual design system. Colors, fonts, spacing.

**Contents:**
```python
# Color palette
COLORS = {
    'primary': '#0066cc',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'error': '#dc3545',
    'background': '#ffffff',
    'surface': '#f8f9fa',
    'text': '#212529',
    'text_secondary': '#6c757d',
    'border': '#dee2e6',
}

# Typography
FONTS = {
    'family': '"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'size_heading': '20px',
    'size_subheading': '16px',
    'size_body': '14px',
    'size_small': '12px',
    'weight_normal': '400',
    'weight_medium': '500',
    'weight_bold': '700',
}

# Spacing
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
}

# Borders
BORDERS = {
    'radius': '4px',
    'width': '1px',
    'style': 'solid',
}

# Shadows
SHADOWS = {
    'sm': '0 1px 2px rgba(0,0,0,0.05)',
    'md': '0 4px 6px rgba(0,0,0,0.1)',
    'lg': '0 10px 15px rgba(0,0,0,0.1)',
}

def apply_theme(widget):
    """Apply theme to widget"""
    # Add CSS classes or inline styles
```

**Usage:**
```python
from ui.styles.theme import COLORS, FONTS, SPACING

button = Button(description="Submit")
button.style.button_color = COLORS['primary']
```

---

## Data Flow Examples

### Example 1: User Runs Timeline Query

**Step 1: User clicks timeline in navigation**
```
Navigation → emit('tool_selected', 'RAD/ingestor/timeline')
```

**Step 2: app.py receives event**
```python
def on_tool_selected(tool_path):
    content_area.load_tool(tool_path, executor)
```

**Step 3: ContentArea loads tool UI**
```python
content_area.load_tool("RAD/ingestor/timeline", executor)
  → tool_loader.load_tool_ui("RAD/ingestor/timeline", executor)
    → import ui.tools.RAD.ingestor.timeline_ui
      → return TimelineUI(executor, "RAD/ingestor/timeline")
```

**Step 4: TimelineUI renders**
```
Displays:
- Header
- Date pickers (start, end)
- Submit button
- Empty result area
```

**Step 5: User fills form and clicks Submit**
```python
TimelineUI._on_submit()
  params = {'start': '2024-01-01', 'end': '2024-03-01'}
  result = executor.execute(
      user='nidhal.benmaghnia',
      tool_path='RAD/ingestor/timeline',
      params=params
  )
```

**Step 6: Executor orchestrates**
```python
executor.execute()
  1. Generate request_id
  2. Create ExecutionContext
  3. Log execution start
  4. Get tool from registry
  5. Call tool.run(context, **params)
```

**Step 7: Tool executes**
```python
TimelineTool.run(context, start='2024-01-01', end='2024-03-01')
  1. Validate dates
  2. Log to context.logger
  3. Create IngestorTimelineModel()
  4. Call model.fetch_data(start_dt, end_dt)
  5. Call model.process(raw_data)
  6. Return processed data
```

**Step 8: Model executes business logic**
```python
IngestorTimelineModel.fetch_data()
  → Query Athena/HYDRA
  → Return raw records

IngestorTimelineModel.process()
  → Transform data
  → Calculate metrics
  → Return {records, metrics, timeline}
```

**Step 9: Executor returns Result**
```python
Result.success(
    data={records, metrics, timeline},
    request_id='550e8400-...'
)
```

**Step 10: TimelineUI renders result**
```python
TimelineUI._render_result(data)
  → Create data table
  → Create summary panel
  → Create timeline chart
  → Display in result_area
```

**User sees:**
```
┌──────────────────────────────────────┐
│ Timeline Query                       │
├──────────────────────────────────────┤
│ Results                              │
│                                      │
│ [Data Table with 150 records]        │
│                                      │
│ Summary:                             │
│ • Total ingests: 150                 │
│ • Success rate: 98.7%                │
│ • Avg duration: 2.3s                 │
│                                      │
│ [Timeline Chart showing activity]    │
└──────────────────────────────────────┘
```

---

### Example 2: Error Handling Flow

**User submits invalid date range (end before start)**

**Step 1-6:** Same as above

**Step 7: Tool validates and raises error**
```python
TimelineTool.run(context, start='2024-03-01', end='2024-01-01')
  if start_dt >= end_dt:
      raise ParameterValidationError(
          "Start date must be before end date"
      )
```

**Step 8: Executor catches error**
```python
except ToolExecutionError as e:
    logger.warning(f"Tool execution failed: {e}")
    return Result.error(
        message=str(e),
        request_id=request_id,
        error_type="ToolExecution",
        user_message=e.user_message
    )
```

**Step 9: TimelineUI displays error**
```python
TimelineUI._show_error(result)
  → create_error_widget(result)
```

**User sees:**
```
┌──────────────────────────────────────┐
│ ⚠️ An error occurred                 │
│                                      │
│ Start date must be before end date   │
│                                      │
│ Request ID: 550e8400-...             │
└──────────────────────────────────────┘
```

**Logs contain:**
```json
{
  "timestamp": "2024-11-25T10:30:45",
  "level": "WARNING",
  "tool_path": "RAD/ingestor/timeline",
  "user": "nidhal.benmaghnia",
  "request_id": "550e8400-...",
  "error_type": "ToolExecutionError",
  "message": "Start date must be before end date"
}
```

---

## Key Design Decisions

### 1. Why Separate Tool vs Tool UI?

**Tool (backend):**
- Business logic
- Reusable across UIs (could build CLI, API, different web UI)
- Testable without UI

**Tool UI (frontend):**
- Presentation logic
- User interaction
- Can be swapped/redesigned without touching backend

**Benefit:** Clean separation, testability, flexibility

---

### 2. Why ExecutionContext?

**Without context:**
```python
def run(self, start, end):
    # How do I log?
    # Who is the user?
    # What's the request ID?
```

**With context:**
```python
def run(self, context, start, end):
    context.logger.info("Starting query")
    # All logging automatically includes user, request_id
```

**Benefit:** Clean logging, traceability, debugging

---

### 3. Why Result Wrapper?

**Alternative 1: Raise exceptions to UI**
```python
# UI code becomes:
try:
    data = executor.execute(...)
    render(data)
except ToolExecutionError as e:
    show_error(e)
except Exception as e:
    show_error(e)
```

**Alternative 2: Result wrapper**
```python
result = executor.execute(...)
if result.success:
    render(result.data)
else:
    show_error(result)
```

**Benefits of Result:**
- No exception handling in UI
- Consistent error structure
- Request ID always available
- Explicit success/failure

---

### 4. Why Registry Auto-Discovery?

**Alternative: Manual registration**
```python
# In some config file:
register_tool("RAD/ingestor/timeline", TimelineTool)
register_tool("RAD/ingestor/force_load", ForceLoadTool)
# ... repeat for every tool
```

**Auto-discovery:**
- Just create `timeline_tool.py` with `class TimelineTool(BaseTool)`
- Registry finds it automatically
- Less boilerplate
- No forgetting to register

**Trade-off:** Slower startup (negligible), magic discovery (but explicit with `BaseTool` inheritance)

---

## Testing Strategy

### Backend Tests

**Unit tests for models:**
```python
def test_ingestor_timeline_fetch():
    model = IngestorTimelineModel()
    data = model.fetch_data(start, end)
    assert len(data) > 0
```

**Integration tests for tools:**
```python
def test_timeline_tool():
    context = create_test_context()
    tool = TimelineTool()
    result = tool.run(context, start="2024-01-01", end="2024-03-01")
    assert 'records' in result
```

**Registry tests:**
```python
def test_registry_discovers_all_tools():
    registry = Registry()
    assert 'RAD/ingestor/timeline' in registry._tools
```

### Frontend Tests

**Component tests:**
```python
def test_navigation_builds():
    nav = Navigation(mock_registry)
    assert nav.widget is not None
```

**End-to-end (manual for now):**
- Click through navigation
- Submit forms
- Verify results display
- Test error cases

---

## Deployment

### Local Development
```bash
voila notebook.ipynb --port 8866
```

### Voila Server Deployment
```bash
voila notebook.ipynb --no-browser --port 8866
```

### Multi-User Considerations

**Process isolation:** Voila creates separate kernel per user ✓

**Shared resources:**
- Database: Handle via connection pooling
- File system: Use user-specific paths if needed
- Logs: Include user in every log line

**Concurrency:**
- Models are instantiated per-request (no shared state)
- Registry/Executor are read-only after init (safe)
- DB connections via ModelLoader (thread-safe pooling)

---

## Support & Debugging Workflow

### When Trader Dave Says "My Timeline Is Wrong"

**Step 1: Find the execution**
```bash
grep "nidhal.benmaghnia" logs.json | grep "timeline" | tail -20
```

**Step 2: Get request ID**
```json
{
  "request_id": "550e8400-...",
  "user": "dave",
  "tool_path": "RAD/ingestor/timeline",
  "params": {"start": "2024-01-01", "end": "2024-03-01"}
}
```

**Step 3: See what happened**
```bash
grep "550e8400-..." logs.json
```

Shows:
- Execution start
- Parameters
- What was fetched from DB
- Processing steps
- Result or error

**Step 4: Reproduce**
```python
# In a notebook or script:
context = create_test_context(user="dave", request_id="test")
tool = TimelineTool()
result = tool.run(context, start="2024-01-01", end="2024-03-01")
# See same result Dave saw
```

**Step 5: Fix and verify**
- Fix bug in model/tool
- Re-run with same params
- Verify fix

---

## Next Steps

### Phase 1: Foundation (Week 1)
1. Set up project structure
2. Implement base classes (BaseTool, Result, errors)
3. Implement Registry with auto-discovery
4. Implement Executor with logging
5. Create one model + tool (timeline)

### Phase 2: Basic UI (Week 2)
1. Implement app.py entry point
2. Implement Navigation component
3. Implement ContentArea component
4. Implement one tool UI (timeline)
5. Wire everything together

### Phase 3: Production Ready (Week 3)
1. Add error handling throughout
2. Implement widget_factory for consistency
3. Apply theme/styling
4. Add second tool to validate pattern
5. Testing and refinement

### Phase 4: Scale (Week 4+)
1. Add remaining tools
2. Build more sophisticated result renderers
3. Add user preferences
4. Performance optimization
5. Production deployment

---

## Summary

**Architecture principles:**
- ✅ Clear layer separation (UI ↔ Service ↔ Tool ↔ Model)
- ✅ All code in Python scripts (notebook only imports)
- ✅ Dynamic tool discovery and navigation
- ✅ Comprehensive logging with context
- ✅ Professional, slick UI
- ✅ Debuggable for production support

**Clean tree:**
```
backend/          # Business logic
  core/          # Infrastructure
  models/        # Domain logic
  tools/         # Executable units
  lib/           # Utilities

ui/              # Presentation
  components/    # Reusable UI
  tools/         # Tool-specific UIs
  lib/           # UI utilities
  styles/        # Visual design
```

**No soup:** Every file has one clear responsibility. Every layer talks only downward.
