 # -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import  Style
import useEnume
import tkinter_widget as twidget
"스마트스토어_전체주문발주발송관리_20220920_1540.xlsx"
class App(Frame):

    def contentMainButtons(self, filepath, fnOrigin):
        frame = Frame(self, bg=mainbg)
        fileframe = twidget.fileSelectFrame(frame,filepath)
        fileframe.pack(side=LEFT)
        submitframe = twidget.fileSubmitFrame(self, frame, filepath, fnOrigin)
        submitframe.pack(side=RIGHT)
        frame.pack(fill=X)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH) 
        self.configure(bg=mainbg, padx=15)
        header = twidget.headerFrame(self, "DELIVERY SYSTEM")
        header.pack(fill="x", pady=10)
        fileName = StringVar()
        fileName.set("파일을 입력하세요.")
        fnOrigin = StringVar()
        self.contentMainButtons(fileName, fnOrigin)

root = Tk()
ws, hs = root.winfo_screenwidth(), root.winfo_screenheight()
w, h  = 1500, 800
x, y = (ws/2) - (w/2), (hs/2) - (h/2)

mainbg = useEnume.MAIN_BG
mainfg = useEnume.MAIN_FG
selectBg = useEnume.SELECT_BTN

root.configure(bg=mainbg)
root.title("sc_delivery [1.0.5]")
style = Style(root)

style.theme_use("default")
style.configure("Entry", background=mainbg, fieldbackground=mainbg, foreground=mainfg)
style.configure("Treeview", background=mainbg, fieldbackground=mainbg, foreground=mainfg, bordercolor=mainfg)
style.configure("Treeview.Heading", background=mainbg, fieldbackground=mainbg, foreground=mainfg, bordercolor=mainbg)
style.map("Treeview", background=[('selected', selectBg)], foreground=[('selected', mainfg)])
style.map("Treeview.Heading", background=[('selected', selectBg)], foreground=[('selected', mainfg)])
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(False, False)
apps = App(master=root)
apps.mainloop()
os.system("pause")