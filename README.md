# MemView: GUI-Based Memory Monitor & Process Killer

## 📋 Project Overview

**MemView** is a cross-platform desktop application that monitors real-time memory usage of running processes and provides an intuitive GUI for process management. Built with Python, it demonstrates strong system-level programming skills relevant to embedded systems and memory management.

## 🎯 Why This Project is Perfect for Qualcomm Associate Engineer Role

### Technical Skills Demonstrated:
- **Memory Organization**: Direct interaction with system memory via `psutil`
- **System-Level Programming**: Process management, signals, and OS interaction
- **Cross-Platform Development**: Compatible with macOS, Linux, and Windows
- **Real-Time Monitoring**: Threaded auto-refresh and live data updates
- **GUI Development**: Professional desktop application with `tkinter`

### Qualcomm-Relevant Concepts:
- Memory management and optimization
- System resource monitoring
- Process lifecycle management
- Real-time data processing
- Cross-platform compatibility

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Create project directory:**
```bash
mkdir memview-project
cd memview-project
```

2. **Create virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install psutil
```

4. **Save the main application:**
Save the Python code as `memview.py`

5. **Run the application:**
```bash
python memview.py
```

## 🔧 Technical Architecture

### Core Components

1. **Process Monitor Engine**
   - Uses `psutil` library for cross-platform process information
   - Gathers PID, name, memory usage, CPU usage, and status
   - Implements efficient data collection with error handling

2. **GUI Framework**
   - Built with `tkinter` for native look and feel
   - Sortable table with `ttk.Treeview`
   - Responsive design with proper grid layout

3. **Memory Management**
   - Real-time memory tracking in MB
   - Total system memory calculation
   - Memory usage sorting and filtering

4. **Process Control**
   - Safe process termination with confirmation dialogs
   - Platform-specific signal handling (SIGTERM/SIGKILL)
   - Error handling for access denied scenarios

### Key Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| **Real-time Monitoring** | Updates every 3 seconds | Threading with `time.sleep()` |
| **Memory Sorting** | Sort by memory usage (descending) | Custom sorting algorithm |
| **Process Killing** | Kill processes via GUI or keyboard | `psutil.Process.terminate()` |
| **Keyboard Shortcuts** | Cmd+K (Mac), Ctrl+K (Windows/Linux) | Event binding |
| **Auto-refresh** | Toggle automatic updates | Boolean variable with thread control |
| **Cross-platform** | Works on macOS, Linux, Windows | Platform detection with `platform.system()` |

## 💻 Usage Instructions

### Basic Operations

1. **Launch Application:**
   ```bash
   python memview.py
   ```

2. **Monitor Processes:**
   - Processes are automatically loaded and sorted by memory usage
   - Click column headers to sort by different criteria
   - Auto-refresh updates every 3 seconds (toggle with checkbox)

3. **Kill a Process:**
   - **Method 1:** Select process and click "Kill Selected"
   - **Method 2:** Double-click on process row
   - **Method 3:** Use keyboard shortcut (Cmd+K on Mac, Ctrl+K on Windows/Linux)
   - **Method 4:** Use "Kill by PID" for specific process ID

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+K` (Mac) / `Ctrl+K` (Win/Linux) | Kill selected process |
| `Cmd+R` (Mac) / `Ctrl+R` (Win/Linux) | Refresh process list |
| `F5` | Refresh process list |
| `Delete` | Kill selected process |
| `Cmd+Q` (Mac) / `Ctrl+Q` (Win/Linux) | Quit application |

## 🛠️ Advanced Features

### 1. Process Filtering
The application can be extended with filtering capabilities:
```python
def filter_processes(self, min_memory=0, process_name=""):
    # Filter processes by memory threshold or name
    pass
```

### 2. Memory Graphs
Add real-time memory usage graphs:
```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_memory_graph(self):
    # Create real-time memory usage graph
    pass
```

### 3. Process Details
Show detailed process information:
```python
def show_process_details(self, pid):
    # Show detailed process information in popup
    pass
```

## 📁 Project Structure

```
memview-project/
├── memview.py              # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── screenshots/           # Application screenshots
├── docs/                  # Additional documentation
└── tests/                 # Unit tests (optional)
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Application launches without errors
- [ ] Process list loads correctly
- [ ] Sorting works for all columns
- [ ] Process killing works with confirmation
- [ ] Keyboard shortcuts function properly
- [ ] Auto-refresh toggles correctly
- [ ] Cross-platform compatibility verified

### Unit Tests (Optional Enhancement)
```python
import unittest
from memview import MemViewApp

class TestMemView(unittest.TestCase):
    def test_process_retrieval(self):
        # Test process data retrieval
        pass
    
    def test_memory_calculation(self):
        # Test memory usage calculations
        pass
```

## 🔒 Security Considerations

### Process Killing Permissions
- Application requires appropriate permissions to kill processes
- Some system processes may require administrator/sudo privileges
- User confirmation dialogs prevent accidental process termination

### Error Handling
- Graceful handling of access denied errors
- Protection against killing critical system processes
- Proper exception handling for process operations

## 📊 Performance Optimization

### Memory Efficiency
- Efficient process data collection
- Minimal memory footprint for GUI components
- Proper cleanup of resources

### CPU Usage
- Threaded auto-refresh to prevent GUI freezing
- Optimized sorting algorithms
- Efficient data structures for process storage

## 🌟 Potential Enhancements

### 1. System Resource Monitoring
- CPU usage graphs
- Disk I/O monitoring
- Network activity tracking

### 2. Process Analytics
- Memory usage trends
- Process startup/shutdown tracking
- Resource usage alerts

### 3. Advanced Features
- Process grouping by application
- Memory leak detection
- System performance recommendations

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

1. **System Programming**: Direct interaction with OS processes and memory
2. **GUI Development**: Professional desktop application design
3. **Threading**: Real-time data updates without blocking UI
4. **Error Handling**: Robust error management and user feedback
5. **Cross-Platform Development**: Code that works across different operating systems

### Code Quality Highlights:
- Clean, readable code structure
- Proper separation of concerns
- Comprehensive error handling
- Cross-platform compatibility
- Professional UI design

