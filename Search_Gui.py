#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pylab import *

import pickle

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog 
from ttk import Frame, Button, Label, Style

from random import randint
from PIL import Image

import q1
import q2
import q3
import q4


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    
        
    def initUI(self):
      
        self.parent.title("HW3")

        self.pack(fill=BOTH, expand=1)

        Button(self, text = "Select File", command = openFile).grid(row=0, column=0, pady=5)
        self.fileName = StringVar()
        Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

        Label(self, text = "Select Mode: ").grid(row=1, column=0, pady=5)

        mode = StringVar(self)
        mode.set("Q1-ColorHistogram")
        om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words")
        om.grid(row=1, column=1, pady=5, sticky=W)

        Button(self, text = "SEARCH", command = lambda: startSearching(self.fileName.get(),mode.get(), self.images)).grid(row=3, column=0, pady=5)

        self.images = []
        for i in range(10):
            self.images.append(Label(self))
            self.images[i].grid(row=i/5+4, column=i%5, pady=50)


 
def openFile ():
    fileName = tkFileDialog.askopenfilename(filetypes=[("Image Files","*.jpg;*.gif")], initialdir = "./dataset")
    app.fileName.set(fileName)

def startSearching (fileName, mode, images):
    if mode=="Q1-ColorHistogram":
        ans = q1.run(fileName)
    elif mode=="Q2-ColorLayout":
        ans = q2.run(fileName)
    elif mode=="Q3-SIFT Visual Words":
        ans = q3.run(fileName)
    elif mode=="Q4-Visual Words using stop words":
        ans = q4.run(fileName)
    else:
        print mode+", mode not found"
        return
    print ans

    for x in xrange(len(images)):
        filename = ImageTk.PhotoImage(Image.open(ans[x]))
        images[x].configure(image=filename)
        images[x].filename = filename

if __name__ == '__main__':
    root = Tk()

    app = Example(root)
    root.geometry("1280x720")
    root.mainloop()

  