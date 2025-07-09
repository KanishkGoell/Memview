#!/usr/bin/env python3
"""
MemView: GUI-Based Memory Monitor & Process Killer
A desktop tool for monitoring real-time memory usage and managing processes
Compatible with macOS, Linux, and Windows

Author: Your Name
Created for: Qualcomm Associate Engineer Application Portfolio
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psutil
import os
import signal
import platform
import threading
import time
from datetime import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

class MemViewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MemView - Memory Monitor & Process Killer")
        self.root.geometry("1000x700")
        
        # System detection
        self.system = platform.system()
        self.is_mac = self.system == "Darwin"
        self.is_linux = self.system == "Linux"
        self.is_windows = self.system == "Windows"
        
        # Mac-specific optimizations
        if self.is_mac:
            self.root.createcommand('tk::mac::ReopenApplication', self.root.deiconify)
            self.root.createcommand('tk::mac::Quit', self.on_closing)
        
        # Auto-refresh settings
        self.auto_refresh = tk.BooleanVar(value=False)
        self.refresh_interval = 5
        self.refresh_thread = None
        self.running = True
        self.refresh_in_progress = False
        
        # Sorting variables
        self.sort_column = "memory"
        self.sort_reverse = True
        
        # Process collection timeout
        self.process_timeout = 10  # seconds
        
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        self.refresh_processes()
        self.start_auto_refresh()
        
    def setup_ui(self):
        """Create the main UI layout"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="MemView - Memory Monitor & Process Killer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        self.refresh_btn = ttk.Button(control_frame, text="🔄 Refresh", 
                                     command=self.refresh_processes)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="🗑️ Kill Selected", 
                  command=self.kill_selected_process).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="⚙️ Kill by PID", 
                  command=self.kill_by_pid).pack(side=tk.LEFT, padx=(0, 5))
        
        # Auto-refresh checkbox
        ttk.Checkbutton(control_frame, text="Auto-refresh", 
                       variable=self.auto_refresh).pack(side=tk.LEFT, padx=(10, 0))
        
        # System info
        system_info = f"System: {self.system} | Total RAM: {self.get_total_memory():.1f} GB"
        ttk.Label(control_frame, text=system_info).pack(side=tk.RIGHT)
        
        # Process table
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview with scrollbars
        self.tree = ttk.Treeview(table_frame, columns=("pid", "name", "memory", "cpu", "status"), 
                                show="headings", height=15)
        
        # Configure columns
        self.tree.heading("pid", text="PID", command=lambda: self.sort_by("pid"))
        self.tree.heading("name", text="Process Name", command=lambda: self.sort_by("name"))
        self.tree.heading("memory", text="Memory (MB)", command=lambda: self.sort_by("memory"))
        self.tree.heading("cpu", text="CPU (%)", command=lambda: self.sort_by("cpu"))
        self.tree.heading("status", text="Status", command=lambda: self.sort_by("status"))
        
        # Column widths
        self.tree.column("pid", width=80, anchor=tk.CENTER)
        self.tree.column("name", width=350, anchor=tk.W)
        self.tree.column("memory", width=120, anchor=tk.CENTER)
        self.tree.column("cpu", width=80, anchor=tk.CENTER)
        self.tree.column("status", width=100, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for table and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Double-click binding
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        if self.is_mac:
            # macOS shortcuts
            self.root.bind("<Command-k>", lambda e: self.kill_selected_process())
            self.root.bind("<Command-r>", lambda e: self.refresh_processes())
            self.root.bind("<Command-q>", lambda e: self.on_closing())
        else:
            # Windows/Linux shortcuts
            self.root.bind("<Control-k>", lambda e: self.kill_selected_process())
            self.root.bind("<Control-r>", lambda e: self.refresh_processes())
            self.root.bind("<Control-q>", lambda e: self.on_closing())
        
        # Universal shortcuts
        self.root.bind("<F5>", lambda e: self.refresh_processes())
        self.root.bind("<Delete>", lambda e: self.kill_selected_process())
        
    def get_total_memory(self):
        """Get total system memory in GB"""
        return psutil.virtual_memory().total / (1024**3)
    
    def get_single_process_info(self, pid):
        """Get info for a single process with timeout protection"""
        try:
            proc = psutil.Process(pid)
            
            # Get process info with minimal calls
            with proc.oneshot():  # Optimize multiple attribute access
                name = proc.name()
                try:
                    memory_info = proc.memory_info()
                    memory_mb = memory_info.rss / (1024 * 1024)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    memory_mb = 0.0
                
                try:
                    status = proc.status()
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    status = "unknown"
                
                return {
                    'pid': pid,
                    'name': name,
                    'memory': memory_mb,
                    'cpu': 0.0,  # Skip CPU to avoid hanging
                    'status': status
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
        except Exception:
            return None
    
    def get_processes(self):
        """Get list of all running processes with their details using threading"""
        print("Collecting process information...")
        
        # Get all PIDs first (fast operation)
        try:
            all_pids = psutil.pids()
        except Exception as e:
            print(f"Error getting PIDs: {e}")
            return []
        
        print(f"Found {len(all_pids)} PIDs to process")
        
        processes = []
        
        # Use ThreadPoolExecutor for parallel processing with timeout
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit all tasks
            future_to_pid = {
                executor.submit(self.get_single_process_info, pid): pid 
                for pid in all_pids
            }
            
            # Collect results with timeout
            try:
                for future in as_completed(future_to_pid, timeout=self.process_timeout):
                    try:
                        result = future.result(timeout=0.1)  # Quick timeout per process
                        if result:
                            processes.append(result)
                    except Exception:
                        continue  # Skip problematic processes
            except TimeoutError:
                print("Process collection timed out, using partial results")
                # Cancel remaining futures
                for future in future_to_pid:
                    future.cancel()
        
        print(f"Successfully collected {len(processes)} processes")
        return processes
    
    def refresh_processes(self):
        """Refresh the process list in a separate thread"""
        if self.refresh_in_progress:
            return
        
        def refresh_worker():
            try:
                self.refresh_in_progress = True
                self.root.after(0, lambda: self.status_var.set("Refreshing processes..."))
                self.root.after(0, lambda: self.refresh_btn.config(state='disabled'))
                
                # Get processes
                processes = self.get_processes()
                
                # Sort processes
                processes.sort(key=lambda x: x[self.sort_column], reverse=self.sort_reverse)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.update_process_list(processes))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Error refreshing processes: {str(e)}"))
                print(f"Error in refresh_processes: {e}")
            finally:
                self.refresh_in_progress = False
                self.root.after(0, lambda: self.refresh_btn.config(state='normal'))
        
        # Run refresh in background thread
        threading.Thread(target=refresh_worker, daemon=True).start()
    
    def update_process_list(self, processes):
        """Update the process list in the UI (must be called from main thread)"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Populate tree
        for proc in processes:
            self.tree.insert("", "end", values=(
                proc['pid'],
                proc['name'],
                f"{proc['memory']:.1f}",
                f"{proc['cpu']:.1f}",
                proc['status']
            ))
        
        # Update status
        total_processes = len(processes)
        total_memory = sum(proc['memory'] for proc in processes)
        self.status_var.set(f"Showing {total_processes} processes | "
                           f"Total Memory: {total_memory:.1f} MB | "
                           f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def sort_by(self, column):
        """Sort processes by specified column"""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = (column == "memory")
        
        self.refresh_processes()
    
    def kill_selected_process(self):
        """Kill the selected process"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a process to kill.")
            return
        
        # Get process details
        item = self.tree.item(selected_item[0])
        pid = int(item['values'][0])
        name = item['values'][1]
        
        # Confirm before killing
        response = messagebox.askyesno("Confirm Kill Process", 
                                     f"Are you sure you want to kill process:\n\n"
                                     f"PID: {pid}\n"
                                     f"Name: {name}\n\n"
                                     f"This action cannot be undone.")
        
        if response:
            self.kill_process(pid, name)
    
    def kill_by_pid(self):
        """Kill process by entering PID manually"""
        pid_str = simpledialog.askstring("Kill Process by PID", "Enter PID:")
        if pid_str:
            try:
                pid = int(pid_str)
                self.kill_process(pid, f"PID {pid}")
            except ValueError:
                messagebox.showerror("Invalid PID", "Please enter a valid numeric PID.")
    
    def kill_process(self, pid, name):
        """Kill a process by PID"""
        try:
            process = psutil.Process(pid)
            
            if self.is_windows:
                process.terminate()
                process.wait(timeout=3)
            else:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except psutil.TimeoutExpired:
                    process.kill()
            
            self.status_var.set(f"Successfully killed process: {name} (PID: {pid})")
            messagebox.showinfo("Success", f"Process {name} (PID: {pid}) has been killed.")
            
            # Refresh the process list
            self.refresh_processes()
            
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", f"Process with PID {pid} no longer exists.")
        except psutil.AccessDenied:
            messagebox.showerror("Permission Denied", 
                               f"Cannot kill process {name} (PID: {pid}). "
                               f"Try running as administrator/sudo.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to kill process: {str(e)}")
    
    def on_double_click(self, event):
        """Handle double-click on process item"""
        self.kill_selected_process()
    
    def start_auto_refresh(self):
        """Start the auto-refresh thread"""
        def refresh_worker():
            while self.running:
                if self.auto_refresh.get() and not self.refresh_in_progress:
                    self.root.after(0, self.refresh_processes)
                time.sleep(self.refresh_interval)
        
        self.refresh_thread = threading.Thread(target=refresh_worker, daemon=True)
        self.refresh_thread.start()
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        if self.refresh_thread:
            self.refresh_thread.join(timeout=1)
        self.root.quit()
        self.root.destroy()

def main():
    """Main application entry point"""
    try:
        import psutil
    except ImportError:
        print("Error: psutil module is required. Install it with: pip install psutil")
        return
    
    root = tk.Tk()
    app = MemViewApp(root)
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    try:
        if platform.system() == "Darwin":
            pass
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()