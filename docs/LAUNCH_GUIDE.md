# 🚀 NLRAD Dashboard - Launch Guide

This guide explains how to launch and use the NLRAD Dashboard.

---

## ✅ Prerequisites

Make sure you have:
- Python 3.7+ installed
- All dependencies installed: `pip install -r requirements.txt`

---

## 🎯 Quick Start

### 1. Test Everything Works
```bash
# Run comprehensive tests
python test_ui.py
```

You should see:
```
✓ UI structure looks good!
✓ Tool UIs load successfully!
✓ Backend execution works!
ALL TESTS PASSED! ✓
```

### 2. Launch the Dashboard

**Option A: Production Mode (Recommended)**
```bash
voila notebook.ipynb --port 8866
```

**Option B: Development Mode (For Debugging)**
```bash
jupyter notebook notebook.ipynb
```

### 3. Open in Browser

- **Voila**: Navigate to `http://localhost:8866`
- **Jupyter**: Use the URL shown in the terminal

---

## 🖥️ Using the Dashboard

### Dashboard Layout

The dashboard has two main sections:

```
┌─────────────────────────────────────────────────┐
│  NLRAD Dashboard                                │
├──────────────┬──────────────────────────────────┤
│              │                                  │
│  Navigation  │       Content Area               │
│  (Sidebar)   │                                  │
│              │   [Tool UI displays here]        │
│  RAD         │                                  │
│  └─ Ingestor │                                  │
│     ├─Timeline                                  │
│     └─Force   │                                  │
│       Load    │                                  │
│              │                                  │
└──────────────┴──────────────────────────────────┘
```

### Navigation

- **Left sidebar** shows all available tools organized by category
- Click any tool button to load it in the content area
- Tools are grouped hierarchically (RAD → Ingestor → Timeline/Force Load)

---

## 📊 Timeline Tool

### Purpose
Query timeline data by desk and date.

### How to Use

1. **Select Desk** from dropdown:
   - Options
   - Exotics
   - Inflation
   - LDFX
   - FXG

2. **Select Date** using date picker (defaults to today)

3. **Click "Query Timeline"** button

4. **View Results**:
   - Success message showing number of records found
   - Table with columns:
     - **TS**: Timestamp
     - **COB**: Close of Business date
     - **data**: Data path
     - **overwrite**: Boolean flag (✓/✗)
   - Alternating row colors for readability
   - Colored boolean values (green ✓ / red ✗)

### Example Output
```
✓ Success
Found 10 timeline records

┌─────────────────────┬────────────┬──────────────────────┬───────────┐
│ TS                  │ COB        │ data                 │ overwrite │
├─────────────────────┼────────────┼──────────────────────┼───────────┤
│ 2024-01-15 09:00:00 │ 2024-01-15 │ /NLRAD/Options/path_0│ ✗         │
│ 2024-01-15 10:00:00 │ 2024-01-15 │ /NLRAD/Options/path_1│ ✓         │
└─────────────────────┴────────────┴──────────────────────┴───────────┘
```

---

## 🔧 Force Load Tool

### Purpose
Manage force load configurations with editable tables.

### How to Use

1. **Select Table** from dropdown:
   - Inflation Env
   - Options ScenarioGamma

2. **Click "Load Table"** to fetch default configuration

3. **View Table Info**:
   - Table name
   - Description
   - Number of rows

4. **Edit Configuration**:
   - Click any cell to edit its value
   - Changes are saved automatically when you click outside the cell

5. **Manage Rows**:
   - **Add Row**: Click to add empty row at bottom
   - **Remove Last Row**: Click to delete the last row

6. **Submit Changes**: Click "Submit Changes" to save

### Table Columns

**Both tables have these columns:**
- **configName**: Configuration name (required)
- **key**: Configuration key (required)
- **group**: Configuration group (required)

### Example Workflow

```
1. Select "Inflation Env" → Click "Load Table"
2. Table loads with 3 default rows
3. Edit configName in row 1: "Config1" → "MyConfig"
4. Click "Add Row" → New empty row appears
5. Fill in new row values
6. Click "Submit Changes"
7. Success message: "Successfully saved 4 rows for Inflation Env"
```

---

## 🎨 Understanding ipywidgets

The UI uses **ipywidgets**, interactive widgets for Jupyter notebooks.

### Common Widgets You'll See

| Widget | Purpose | Example |
|--------|---------|---------|
| `Dropdown` | Select from options | Desk selection |
| `DatePicker` | Pick a date | Date selection |
| `Button` | Trigger action | Submit button |
| `Text` | Text input | Table cell editing |
| `Output` | Display dynamic content | Results area |
| `HTML` | Static HTML content | Headers, messages |
| `VBox` | Vertical layout | Stacking widgets |
| `HBox` | Horizontal layout | Side-by-side widgets |

### Event Flow

```
User clicks button
    ↓
on_click handler called
    ↓
Clear output area, show loading
    ↓
Execute tool via backend
    ↓
Get result (success or error)
    ↓
Display result in output area
```

---

## 🐛 Troubleshooting

### Dashboard doesn't load

**Problem**: Error when running `voila notebook.ipynb`

**Solution**:
```bash
# Check dependencies
pip install -r requirements.txt

# Test backend
python -c "from backend.server import initialize_backend; initialize_backend()"

# Run tests
python test_ui.py
```

### Tool doesn't appear in navigation

**Problem**: Added new tool but it doesn't show

**Solution**:
1. Make sure tool is added to registry dictionary in [backend/core/registry.py](backend/core/registry.py)
2. Restart voila/jupyter
3. Check for import errors in terminal

### Error when clicking tool

**Problem**: Error message appears when using tool

**Solution**:
1. Check the error details (click "Technical Details" accordion)
2. Look at terminal/console for JSON logs
3. Check parameter validation in tool code
4. Verify tool path matches UI path

### Changes not appearing

**Problem**: Made code changes but nothing happens

**Solution**:
- **Voila**: Must restart voila server
- **Jupyter**: Kernel → Restart & Clear Output, then re-run cell

---

## 📁 File Structure Quick Reference

```
nlrad_dashboard/
├── notebook.ipynb          ← Entry point (single cell)
├── requirements.txt        ← Dependencies
├── test_ui.py             ← Test script
├── PROGRESS.md            ← Implementation progress
├── LAUNCH_GUIDE.md        ← This file
│
├── backend/
│   ├── core/
│   │   ├── registry.py    ← Tool registry (ADD NEW TOOLS HERE)
│   │   ├── executor.py    ← Executes tools
│   │   └── base_tool.py   ← Base class for tools
│   ├── tools/
│   │   └── RAD/ingestor/
│   │       ├── timeline_tool.py      ← Timeline backend
│   │       └── force_load_tool.py    ← Force load backend
│   └── models/
│       ├── ingestor_timeline.py  ← Timeline logic
│       └── ingestor_force.py     ← Force load logic
│
├── ui/
│   ├── app.py             ← Main UI (navigation + content)
│   ├── components/
│   │   ├── navigation.py      ← Sidebar navigation
│   │   ├── content_area.py    ← Content display
│   │   ├── tool_loader.py     ← Dynamic UI loading
│   │   └── error_display.py   ← Error rendering
│   └── tools/
│       └── RAD/ingestor/
│           ├── timeline_ui.py      ← Timeline UI
│           └── force_load_ui.py    ← Force load UI
│
└── config/
    └── settings.py        ← Configuration (desks, tables, etc.)
```

---

## 🔄 Adding a New Tool

Want to add a new tool? Follow these steps:

### 1. Create Backend Tool

Create `backend/tools/CATEGORY/SUBCATEGORY/my_tool_tool.py`:

```python
from backend.core.base_tool import BaseTool

class MyToolTool(BaseTool):
    category = "CATEGORY/SUBCATEGORY"
    name = "my_tool"
    description = "What my tool does"

    def run(self, context, param1, param2):
        # Your logic here
        return {"result": "success"}
```

### 2. Add to Registry

Edit [backend/core/registry.py](backend/core/registry.py):

```python
# At top, add import
from backend.tools.CATEGORY.SUBCATEGORY.my_tool_tool import MyToolTool

# In __init__, add to dictionary
self._tools = {
    'CATEGORY/SUBCATEGORY/my_tool': MyToolTool,
    # ... existing tools
}
```

### 3. Create UI

Create `ui/tools/CATEGORY/SUBCATEGORY/my_tool_ui.py`:

```python
import ipywidgets as widgets

class MyToolUI:
    def __init__(self, executor, tool_path):
        self.executor = executor
        self.tool_path = tool_path
        self.widget = self._build_ui()

    def _build_ui(self):
        # Create your widgets
        button = widgets.Button(description='Submit')
        button.on_click(self._on_submit)

        return widgets.VBox([button])

    def _on_submit(self, button):
        result = self.executor.execute(
            user='dashboard_user',
            tool_path=self.tool_path,
            params={'param1': 'value1'}
        )
        # Display result
```

### 4. Test

```bash
# Restart voila
voila notebook.ipynb --port 8866
```

Your new tool will appear in the navigation!

---

## 📝 Tips & Best Practices

### For Development

1. **Use Jupyter first** for debugging (see print statements, errors)
2. **Switch to Voila** for production (clean UI, no code visible)
3. **Check terminal** for JSON logs when debugging
4. **Use test_ui.py** to verify changes before launching

### For UI Code

1. **Add comments** to help understand ipywidgets
2. **Use layouts** to control widget sizing
3. **Clear output** before showing new content
4. **Show loading indicators** for async operations
5. **Use error_display** for consistent error messages

### For Backend Code

1. **Log liberally** - helps debugging
2. **Use user_message** in exceptions for friendly errors
3. **Return dictionaries** from tools (serializable)
4. **Validate inputs** early
5. **Keep models separate** from tools (clean architecture)

---

## 🎓 Learning Resources

### ipywidgets
- [Official Docs](https://ipywidgets.readthedocs.io/)
- [Widget List](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html)
- Check code comments in `ui/tools/RAD/ingestor/timeline_ui.py` for examples

### Voila
- [Official Docs](https://voila.readthedocs.io/)
- Turns Jupyter notebooks into standalone apps
- Hides code cells, shows only output

### Architecture
- See [README.md](README.md) for full architecture documentation
- Check [PROGRESS.md](PROGRESS.md) for implementation details

---

## 💡 Common Questions

**Q: Can I run this without Voila?**
A: Yes, use `jupyter notebook notebook.ipynb` for development mode.

**Q: How do I add authentication?**
A: Modify [backend/lib/user.py](backend/lib/user.py) and pass real user IDs from UI.

**Q: Can I use a real database?**
A: Yes! Update models in `backend/models/` to connect to your database instead of returning mock data.

**Q: How do I change the port?**
A: Use `voila notebook.ipynb --port XXXX` (default is 8866)

**Q: Can I customize colors/styling?**
A: Yes, edit the HTML styles in UI files (inline styles in widgets.HTML)

**Q: Why is the registry a dictionary now?**
A: Simplified from auto-discovery for clarity. Easier to understand and maintain.

---

## ✅ Next Steps

1. **Launch the dashboard** and try both tools
2. **Read the code comments** in UI files to learn ipywidgets
3. **Try adding a simple tool** following the guide above
4. **Customize styling** to match your preferences
5. **Connect real data sources** when ready

---

**Need help?** Check [README.md](README.md) for architecture details or [PROGRESS.md](PROGRESS.md) for implementation notes.

**Ready to launch?** Run: `voila notebook.ipynb --port 8866`
