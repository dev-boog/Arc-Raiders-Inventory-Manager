import tkinter as tk
from tkinter import ttk
from item_index import get_workshop_items
from gui.helpers import sort_treeview

class WorkbenchTab:
    def __init__(self, parent):
        self.parent = parent
        self.workbench_items = get_workshop_items()
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.parent)
        frame.pack(pady=10, fill=tk.X, padx=10)

        ttk.Label(frame, text="Workshop Upgrade Requirements", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        self.workshop_filter = ttk.Combobox(frame, width=25, state='readonly')
        self.workshop_filter['values'] = ['All Workshops', 'Scrappy', 'Gunsmith', 'Gear Bench', 'Medical Lab', 'Refiner', 'Explosives Station', 'Utility Station']
        self.workshop_filter.current(0)
        self.workshop_filter.pack(side=tk.LEFT, padx=5)
        self.workshop_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_workbench())

        self.workbench_total_label = ttk.Label(self.parent, text="Total Value: $0", font=('Arial', 10, 'bold'))
        self.workbench_total_label.pack(pady=5)

        tree_frame = ttk.Frame(self.parent)
        tree_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=10)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Workshop", "Category", "Value", "Quantity", "Total Value"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        headings = [("Name", 200), ("Workshop", 200), ("Category", 150), ("Value", 100), ("Quantity", 80), ("Total Value", 120)]
        for col, width in headings:
            self.tree.heading(col, text=col, command=lambda c=col: sort_treeview(self.tree, c, False))
            self.tree.column(col, width=width)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.display_items(self.workbench_items)

    def display_items(self, items):
        self.tree.delete(*self.tree.get_children())
        total = 0
        for item in items:
            total_value = item.get("total_value", item.get("value", 0))
            total += total_value
            self.tree.insert("", tk.END, values=(
                item.get("name", ""),
                item.get("location", "").replace("Workshop: ", ""),
                item.get("category", ""),
                f"${item.get('value', 0):,}",
                item.get("quantity", "1x"),
                f"${total_value:,}"
            ))
        self.workbench_total_label.config(text=f"Total Value: ${total:,}")

    def filter_workbench(self):
        val = self.workshop_filter.get()
        if val == 'All Workshops':
            self.display_items(self.workbench_items)
        else:
            filtered = [i for i in self.workbench_items if val.lower() in i.get("location", "").lower()]
            self.display_items(filtered)
