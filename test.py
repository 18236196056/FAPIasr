import os

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import time
from datetime import datetime
import uvicorn
from pony.orm import *
from database.mysqldb import *
from fileDeal.asrCall import *
app = FastAPI()
@app.post("/file_upload")
async def file_upload(file: UploadFile = File(...)):
    start = time.time()
    try:
        #保存上传的音频到本地文件
        res = await file.read()
        with open(f"./video/{file.filename}", "wb") as f:
            f.write(res)
            #f 这个文件是"message": "'_io.BufferedWriter' object has no attribute 'file'",
        #****************  调接口对音频进行识别
        resfile = client.asr(get_file_content(f"./video/{file.filename}"), 'wav', 16000, {
            'dev_pid': 1537,
        })
        # print(resfile)  # {'corpus_no': '6988818717101064966', 'err_msg': 'success.', 'err_no': 0, 'result': ['北京科技馆。'], 'sn': '621839036111627211160'}
        videoText = resfile.get("result")[0]
        print(videoText)
        if len(videoText)!=0:
            # 向mysql表中填充数据
            print(11)
            # db.generate_mapping(create_tables=True)
            with db_session:
                VdText(textstr=videoText,lentext=str(len(videoText)))
                commit()
                print("插入数据成功")
        else:
            print("识别文字为空")

        return {"message": "success", 'time': time.time() - start, 'filename': file.content_type}
    except Exception as e:
        return {"message": str(e), 'time': time.time() - start, 'filename': file.filename}

# class Item(BaseModel):
#     name:str
#     password:str
#     comment:str
#用户注册
startMin = time.localtime(time.time()).tm_min
# print(startMin)
@app.post('/userRegister')
# async def Uploaduser(item:Item):
async def Uploaduser(name:str=Form(...),password:str=Form(...),comment:str=Form(...)):
    # startMin = time.localtime(time.time()).tm_min
    try:
            # for a in range(0,20):
            #     os.system('cls')
            #     time.sleep(1)
        endMin =datetime.now().minute
        lessMin = endMin - startMin
        print(startMin,endMin,lessMin)   #操作超时提醒
        if int(lessMin) >2:
            print("操作超时，请重新登录")
            return "Error:超时"
        else:
            with db_session:
                existUser = select(user for user in UserBase if name in user.user_name)[:]
                # print(existUser)
                if len(existUser):
                    return '{"Error": "该用户已存在，请更改用户名"}'
                else:
                    UserBase(user_name=name,pass_word=password,notes=comment)
                    return "插入mysql成功"
                commit()
    except Exception as e:
        return {"Error":str(e)}
# 登录：验证用户输入的的信息是否在mysql中
@app.post('/UserLogin')
async def findUser(name:str=Form(...),password:str=Form(...),comment:str=Form(...)):
    try:
        with db_session:
            userExisted = select(user for user in UserBase if name==user.user_name)
            # print(userExisted[:1])
            for user in userExisted:
                if len(userExisted):
                    # pass
                    if password == user.pass_word:
                        return "合法用户，可跳转到'file_upload'接口进行语音识别"
                    else:
                        return "密码输入有误，请重新输入"
                else:
                    return "该用户不存在，请先注册"
            commit()
    except Exception as e:
        return {"error:",str(e)}
