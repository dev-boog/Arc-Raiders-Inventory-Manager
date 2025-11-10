import tkinter as tk
from gui.gui import InventoryGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()
