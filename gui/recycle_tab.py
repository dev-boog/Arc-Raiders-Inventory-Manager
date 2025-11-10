import tkinter as tk
from tkinter import ttk
from gui.helpers import sort_treeview
from item_index import safe_to_recycle

class RecycleTab:
    def __init__(self, parent):
        self.parent = parent
        self.recycle_items = safe_to_recycle
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_items)
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.parent)
        frame.pack(pady=10, fill=tk.X, padx=10)
        ttk.Label(frame, text="Items Safe to Recycle", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(frame, text="Search:", font=('Arial', 9)).pack(side=tk.LEFT, padx=20)
        ttk.Entry(frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        self.count_label = ttk.Label(self.parent, text="Items: 0 | Total Value: $0", font=('Arial', 10))
        self.count_label.pack(pady=5)

        tree_frame = ttk.Frame(self.parent)
        tree_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=10)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Category", "Weight", "Value"), show="headings", yscrollcommand=vsb.set)
        vsb.config(command=self.tree.yview)

        headings = [("Name", 250), ("Category", 200), ("Weight", 120), ("Value", 120)]
        for col, width in headings:
            self.tree.heading(col, text=col, command=lambda c=col: sort_treeview(self.tree, c, False))
            self.tree.column(col, width=width)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.display_items(self.recycle_items)

    def display_items(self, items):
        self.tree.delete(*self.tree.get_children())
        total_value = 0
        for item in items:
            value = item.get("value", 0)
            total_value += value
            self.tree.insert("", tk.END, values=(
                item.get("name", ""),
                item.get("category", ""),
                f"{item.get('weight', 0):.2f}",
                f"${value:,}"
            ))
        self.count_label.config(text=f"Items: {len(items)} | Total Value: ${total_value:,}")

    def filter_items(self, *args):
        query = self.search_var.get().lower()
        if not query:
            self.display_items(self.recycle_items)
        else:
            filtered = [i for i in self.recycle_items if query in i.get("name", "").lower()]
            self.display_items(filtered)
