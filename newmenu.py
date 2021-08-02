from ttkthemes import themed_tk as tk
from tkinter import *

root = tk.ThemedTk()
root.get_themes()
root.set_theme('breeze')

root.mainloop()
print(1)