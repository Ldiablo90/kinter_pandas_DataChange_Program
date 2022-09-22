import pandas as pd
import os.path as osPath
from datetime import datetime
import msoffcrypto
import io
import LeeFunction as lf

def excelpassok(path, password):
    try:
        decrypted = io.BytesIO()
        with open(path, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(password=password)  # Use password
            file.decrypt(decrypted)
        return pd.read_excel(decrypted, header=1)
    except msoffcrypto.exceptions.InvalidKeyError :
        return pd.DataFrame()
def excelpassnot(path):
    try:
        return pd.read_excel(path, header=1)
    except:
        return pd.DataFrame()

def resultFile(path, password):
    if osPath.isfile(path):
        if password:
            read_data = excelpassok(path, password)
            if not (len(read_data) > 0):return pd.DataFrame(), "비밀번호가 틀립니다."
        else:
            read_data = excelpassnot(path)
            if not (len(read_data) > 0):return pd.DataFrame(), "비밀번호가 걸려있는 파일입니다."
        try:
            onlyShoeBox, onlyRubby = lf.divideList(read_data)
                    
            if len(onlyShoeBox) > 0:
                onlyShoeBox = lf.SixDivideList(onlyShoeBox)
                sortShoeBox = lf.GrassSubmit(onlyShoeBox)
                concatData = pd.concat([sortShoeBox, onlyRubby])
                endData = lf.typeChack(concatData)
                endData = endData.fillna("")
            else:
                typeData = lf.typeChack(onlyRubby)
                endData = typeData.fillna("")
            if osPath.isfile("%s\블랙리스트(슈케이브).xlsx"%(osPath.abspath(""))):
                types = lf.userCheck(endData, "%s\블랙리스트(슈케이브).xlsx"%(osPath.abspath("")))
                orderUser = "유저 확인이 되었습니다." if types else "이상없는 파일입니다."
            else:
                orderUser = "유저파일이 없습니다."
            return endData, orderUser
        except:
            return endData, "잘못된 파일 내용입니다."
    else:
        return pd.DataFrame(), "파일경로를 확인해 주세요."

def validationFile(path, values):
    result = 0
    if osPath.isfile(path):
        read_data = pd.read_excel(path, header=1)
        sumnum = int(read_data["수량"].sum())
        read_data["주문번호"] = read_data["주문번호"].apply(str)
        read_data = read_data[["주문번호", "옵션정보"]].apply(''.join, axis=1).values.tolist()
        values = set(values)
        read_data = set(read_data)
        result_data = read_data - values
        if len(result_data) > 0:
            result = list(result_data)
    return result, sumnum

def saveFile(datas):
    sf = pd.DataFrame(datas)
    sf["상품주문번호"] = sf["상품주문번호"].apply(lambda x: '{:d}'.format(x))
    sf["주문번호"] = sf["주문번호"].apply(lambda x: '{:d}'.format(x))
    amOrpm = "오후" if datetime.now().hour >= 14 else "오전"
    sf.to_excel('%s\스마트스토어_%s_%s.xlsx'%(osPath.abspath(""), amOrpm, datetime.now().date()), index=False)
