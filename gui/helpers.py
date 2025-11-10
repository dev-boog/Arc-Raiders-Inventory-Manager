import tkinter as tk

def sort_treeview(tree, col, reverse):
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    try:
        l.sort(key=lambda t: float(t[0].replace('$', '').replace(',', '')), reverse=reverse)
    except:
        l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))

def copy_to_clipboard(root, tree, field):
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        root.clipboard_clear()
        if field == "name":
            root.clipboard_append(item['values'][0])
        elif field == "value":
            root.clipboard_append(item['values'][3])
