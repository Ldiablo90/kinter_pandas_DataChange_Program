 # -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import Treeview
import tkinter_function as tfunc
import useEnume

def headerFrame(parent,title):
    frame = Frame(parent)
    frame.config(bg=mainbg)
    label = Label(frame, text=title)
    label.pack()
    return frame

def fileSelectFrame(parent, filepath):
    frame = LabelFrame(parent, text="파일", bg=mainbg, fg=mainfg)
    Button(frame, text="파일선택", command=lambda: tfunc.fileSelectBtnFunc(filepath), background=mainbg, fg=mainfg, activebackground=selectBg).pack(side=LEFT, padx=5, pady=5)
    Label(frame, textvariable=filepath, wraplength= 800, justify='left', bg=mainbg, fg=mainfg).pack(side=LEFT)
    return frame

def fileSubmitFrame(outmain, parent, filepath, fnOrigin):
    password = StringVar()
    frame = Frame(parent, bg=mainbg)
    Entry(frame, textvariable=password).pack(side=LEFT, padx=5)
    Button(frame, text="오류검사", command=lambda: tfunc.dataValidation(outmain, filepath, fnOrigin), bg=mainbg, fg=mainfg, activebackground=selectBg).pack(side=LEFT,padx=5)
    Button(frame, text="검색", command=lambda: tfunc.searchBtnFunc(filepath, outmain, fnOrigin, password.get()), bg=mainbg, fg=mainfg, activebackground=selectBg).pack(side=LEFT,padx=5)
    Button(frame, text="초기화", command=lambda: tfunc.resetBtnFunc(outmain, filepath, password), bg=mainbg, fg=mainfg, activebackground=selectBg ).pack(side=LEFT,padx=5)
    Button(frame, text="저장", command=lambda:tfunc.saveBtnFunc(outmain), bg=mainbg, fg=mainfg, activebackground=selectBg).pack(side=LEFT,padx=5)
    Button(frame, text="삭제", command=lambda:tfunc.deleteBtnFunc(), bg=mainbg, fg=mainfg, activebackground=selectBg).pack(side=LEFT,padx=5)
    Button(frame, text="종료", command=outmain.quit, bg=mainbg, fg="red", activebackground="white").pack(side=LEFT,padx=5)
    return frame

def dataTableFrame(parent, headers, values):
    parent.winfo_children()[-1].destroy() if len(parent.winfo_children()) > 2 else None
    frame = Frame(parent)
    table = Treeview(frame, columns=headers, show="headings", height=100)
    table.bind("<Double-1>")
    vsb = Scrollbar(frame, orient='vertical', command=table.yview)
    hsb = Scrollbar(frame, orient='horizontal', command=table.xview)
    table.config(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for header in headers:
        table.heading(header, text=header)
        table.column(header, width=60)
    [table.insert("","end", text=1, values=row) for row in values]

    table.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="nse")
    hsb.grid(row=1, column=0, sticky="nsew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.pack(fill=BOTH, pady=15)

mainbg = useEnume.MAIN_BG
mainfg = useEnume.MAIN_FG
selectBg = useEnume.SELECT_BTN
mainfont = useEnume.MAINFONT