import tkinter as tk
from tkinter import ttk
from gui.search_tab import SearchTab
from gui.workbench_tab import WorkbenchTab
from gui.recycle_tab import RecycleTab

class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ARC Raiders - EasyInventory")
        self.root.geometry("1280x720")

        style = ttk.Style()
        style.theme_use('clam')  # Restore your theme

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.search_tab_frame = ttk.Frame(self.notebook)
        self.workbench_tab_frame = ttk.Frame(self.notebook)
        self.recycle_tab_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.search_tab_frame, text="🔍 Search Items")
        self.notebook.add(self.workbench_tab_frame, text="🔨 Workbenches")
        self.notebook.add(self.recycle_tab_frame, text="♻️ Safe to Recycle")

        self.search_tab = SearchTab(self.search_tab_frame)
        self.workbench_tab = WorkbenchTab(self.workbench_tab_frame)
        self.recycle_tab = RecycleTab(self.recycle_tab_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()
