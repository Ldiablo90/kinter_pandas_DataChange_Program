from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import tkinter_widget as twidget
import naver

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))

def askOpenFilename(lText:StringVar):
    filename = filedialog.askopenfilename(filetypes=[("Excel file","*.xlsx"),("Excel file", "*.xls")])
    lText.set(filename) if len(filename) > 0 else None

def reset(fileName:StringVar, table:Treeview):
    fileName.set("파일을 입력하세요.")
    [table.delete(iid) for iid in table.get_children()]
    
def save(table:Treeview):
    values = [table.item(i)["values"] for i in table.get_children() ]
    iid = table.get_children()[0]
    hdlen = len(table.item(iid)["values"])
    headerName = [table.heading("# %d" % i)["text"] for i in range(1,hdlen+1)]
    datas = [dict(zip(headerName,item)) for item in values]
    naver.saveFile(datas)

def rowDel(table:Treeview):
    selcects = table.selection()
    ques = messagebox.askquestion("저장", "정보를 변경하시겠습니까?")
    if ques == "yes":
        [table.delete(iid) for iid in selcects]

def itemClick(event, table:Treeview):
    iid = table.identify_row(event.y)
    cell = table.identify_column(event.x)
    x, y, w, h = table.bbox(iid, cell)
    index = int(cell.replace("#",""))-1
    vlues = table.item(iid)["values"][index]
    typeEntry = Entry(table, width=8 )
    typeEntry.insert(0,vlues)
    typeEntry.bind('<Return>',lambda x: entryClose(table, typeEntry, iid, cell))
    typeEntry.place(x=x, y=y)
    typeEntry.focus()

def entryClose(table: Treeview, entry: Entry, iid, cell):        
    row = table.item(iid)["values"]
    cell = int(cell.replace("#",""))
    row[cell-1] = entry.get()
    table.item(iid, text="" ,values=row)
    entry.place_forget()

def dataValidation(outmain, filepath, fnOrigin):
    if len(outmain.winfo_children()) > 2:
        if filepath.get() == fnOrigin.get():
            frame = outmain.winfo_children()[-1]
            table = frame.winfo_children()[0]
            values = ["%s%s"%(table.item(i)["values"][1], table.item(i)["values"][20]) for i in table.get_children()]
            validation, orginSum = naver.validationFile(fnOrigin.get(), values)

            editSum = sum([int("%s"%(table.item(i)["values"][21])) for i in table.get_children()])
            
            if validation:
                messagebox.showwarning("오류검사","누락된 데이터\n" + "\n".join(validation) + "\n원본물품수량:{}\n수정한물품수량:{}".format(orginSum, editSum))
            else:
                messagebox.showinfo("오류검사","검색한 데이터와 파일이 일치합니다.\n원본물품수량:{}\n수정한물품수량:{}".format(orginSum, editSum))
        else:
            messagebox.showerror("오류검사","파일선택을 다시해주세요.")
    else:
        messagebox.showerror("오류검사","검사할 데이터가 없습니다.")


def fileSelectBtnFunc(strvar):
    filename = filedialog.askopenfilename(filetypes=[("Excel file","*.xlsx"),("Excel file", "*.xls")])
    strvar.set(filename) if len(filename) > 0 else None

def searchBtnFunc(filepath, outmain, fnOrigin, password):
    datas, users = naver.resultFile(filepath.get(), password)
    if len(datas) > 0:
        headers = datas.columns.tolist()
        values = datas.values.tolist()
        fnOrigin.set(filepath.get())
        twidget.dataTableFrame(outmain, headers, values)
        messagebox.showinfo("Thank you for using it.","%s"%users)
    else:
        messagebox.showwarning("메세지 확인 요망","%s"%users)

def resetBtnFunc(outmain, strvar, password):
    strvar.set("파일을 입력하세요.")
    password.set("")
    outmain.winfo_children()[-1].destroy() if len(outmain.winfo_children()) > 2 else None

def saveBtnFunc(outmain):
    if len(outmain.winfo_children()) > 2:
        frame = outmain.winfo_children()[-1]
        table = frame.winfo_children()[0]
        if table.winfo_class() == "Treeview":
            values = [table.item(i)["values"] for i in table.get_children()]
            iid = table.get_children()[0]
            hdlen = len(table.item(iid)["values"])
            headerName = [table.heading("# %d" % i)["text"] for i in range(1,hdlen+1)]
            datas = [dict(zip(headerName,item)) for item in values]
            naver.saveFile(datas)
    else:
        messagebox.showerror("저장","검색할 데이터가 없습니다.")

def deleteBtnFunc():
    print("deleteBtnFunc")