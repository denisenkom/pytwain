'''
Created on Aug 17, 2011

@author: Mikhail Denisenko
'''
import twain
import sys
from tkinter import *
from tkinter import messagebox
import traceback

root = Tk()
root.title('scan.py')

if len(sys.argv) != 2:
    messagebox.showerror("Error", "Usage: python scan.py <filename>")
    exit(1)
    
outpath = sys.argv[1]

def scan():
    try:
        result = twain.acquire(outpath,
                               dpi=300,
                               frame=(0, 0, 8.17551, 11.45438), # A4
                               pixel_type='bw',
                               parent_window=root,
                               )
    except:
        messagebox.showerror("Error", traceback.format_exc())
        sys.exit(1)
    else:
        sys.exit(0 if result else 1)


root.after(1, scan)
root.mainloop()
