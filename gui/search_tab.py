import tkinter as tk
from tkinter import ttk, messagebox
from gui.helpers import sort_treeview, copy_to_clipboard
from item_index import search_item

class SearchTab:
    def __init__(self, parent):
        self.parent = parent
        self.query_var = tk.StringVar()
        self.query_var.trace('w', self.on_search_change)

        self.setup_ui()
        self.results = []

    def setup_ui(self):
        frame = ttk.Frame(self.parent)
        frame.pack(pady=10, fill=tk.X, padx=10)

        ttk.Label(frame, text="Item Name:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(frame, textvariable=self.query_var, width=40, font=('Arial', 10))
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.focus()
        
        ttk.Button(frame, text="Search", command=self.lookup).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=5)

        self.category_filter = ttk.Combobox(self.parent, width=20, state='readonly')
        self.category_filter['values'] = ['All', 'ARC', 'Medical', 'Residential', 'Security','Industrial', 'Nature', 'Trinket', 'Recyclable']
        self.category_filter.current(0)
        self.category_filter.pack(padx=10, pady=5, anchor=tk.W)
        self.category_filter.bind('<<ComboboxSelected>>', lambda e: self.lookup())

        self.results_label = ttk.Label(self.parent, text="Results: 0", font=('Arial', 9, 'italic'))
        self.results_label.pack(pady=5)

        tree_frame = ttk.Frame(self.parent)
        tree_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=10)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Location", "Category", "Value", "Quantity", "Total Value"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        headings = [("Name", 200), ("Location", 250), ("Category", 180), ("Value", 100), ("Quantity", 80), ("Total Value", 120)]
        for col, width in headings:
            self.tree.heading(col, text=col, command=lambda c=col: sort_treeview(self.tree, c, False))
            self.tree.column(col, width=width)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def on_search_change(self, *args):
        query = self.query_var.get()
        if len(query) >= 2:
            self.lookup()

    def clear_search(self):
        self.query_var.set("")
        self.tree.delete(*self.tree.get_children())
        self.results_label.config(text="Results: 0")

    def lookup(self):
        query = self.query_var.get()
        category = self.category_filter.get()
        self.results = search_item(query)
        if category != 'All':
            self.results = [i for i in self.results if category.lower() in i.get("category", "").lower()]
        self.tree.delete(*self.tree.get_children())
        if self.results:
            for item in self.results:
                total_val = item.get("total_value", item.get("value", 0))
                self.tree.insert("", tk.END, values=(
                    item.get("name", ""),
                    item.get("location", ""),
                    item.get("category", ""),
                    f"${item.get('value', 0):,}",
                    item.get("quantity", "-"),
                    f"${total_val:,}" if item.get("quantity") else "-"
                ))
            self.results_label.config(text=f"Results: {len(self.results)}")
        else:
            self.results_label.config(text="Results: 0")
            if query:
                messagebox.showinfo("No Results", f"No items found for '{query}'")

    def show_context_menu(self, event):
        item = self.tree.selection()
        if item:
            menu = tk.Menu(self.parent, tearoff=0)
            menu.add_command(label="Copy Name", command=lambda: copy_to_clipboard(self.parent, self.tree, "name"))
            menu.add_command(label="Copy Value", command=lambda: copy_to_clipboard(self.parent, self.tree, "value"))
            menu.post(event.x_root, event.y_root)
