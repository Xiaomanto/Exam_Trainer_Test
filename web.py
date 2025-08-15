import json
import time
import gradio as gr
import os

from dotenv import load_dotenv
from gradio.utils import NamedString
from service.examService import ExamService

load_dotenv('./.env.example')
examDir = os.getenv('EXAM_DIR')

es = ExamService()

quesObj = []
isStart = False
now_ques = 0
userAns = []

def get_examList() -> list:
    listExam = os.listdir(examDir)
    return listExam

def set_Exam(examName:str | None) -> None:
    if examName is None or examName == '請選擇':
        raise gr.Error("請先選擇題庫")
    examPath = os.path.join(examDir, examName)
    if not os.path.exists(examPath):
        raise gr.Error("Exam Not Found")
    es.load_exam(examPath)
    gr.Success("Exam Loaded")
    return

def set_ramdom(choice:str) -> None:
    es.set_Ramdom_Ques(choice)
    gr.Success("Ramdom Ques Set")
    return

def next_ques(ans:str):
    global quesObj, now_ques
    quesObj = es.Ramdom
    set_ans(ans)
    now_ques += 1
    obj = quesObj[now_ques]
    # print(len(quesObj or []))
    # print(len(es.userAns or []))
    return (
        obj.ques+"\nA "+obj.optionA+"\nB "+obj.optionB+ "\nC "+obj.optionC+ "\nD "+obj.optionD, 
        "A",
        gr.update(interactive=not now_ques == 0 and isStart),
        gr.update(interactive=not now_ques == len(es.Ramdom or [])-1 and isStart),
        gr.update(interactive=len(es.Ramdom or [])-1 == len(es.userAns or []) and isStart),
        f"<center><h4> 第 {now_ques + 1} 題 </h4></center>"
    )
def get_ques():
    global quesObj,isStart
    quesObj = es.Ramdom
    isStart = True
    obj = quesObj[0]
    return (
        obj.ques+"\nA "+obj.optionA+"\nB "+obj.optionB+ "\nC "+obj.optionC+ "\nD "+obj.optionD, 
        "A",
        gr.update(interactive=not 0 == 0 and isStart),
        gr.update(interactive=not 0 == len(es.Ramdom or [])-1 and isStart),
        gr.update(interactive=len(es.Ramdom or [])-1 == len(es.userAns or []) and isStart),
        f"<center><h4> 第 {0 + 1} 題 </h4></center>"
    )

def back_ques(ans:str):
    global quesObj, now_ques
    quesObj = es.Ramdom
    set_ans(ans)
    now_ques -= 1
    obj = quesObj[now_ques]
    return (
        obj.ques+"\nA "+obj.optionA+"\nB "+obj.optionB+ "\nC "+obj.optionC+ "\nD "+obj.optionD, 
        "A",
        gr.update(interactive=not now_ques == 0 and isStart),
        gr.update(interactive=not now_ques == len(es.Ramdom or [])-1 and isStart),
        gr.update(interactive=len(es.Ramdom or [])-1 == len(es.userAns or []) and isStart),
        f"<center><h4> 第 {now_ques + 1} 題 </h4></center>"
    )

def set_ans(ans:str) -> None:
    es.set_ans(now_ques,ans)
    gr.Success("作答成功")
    return

def reset():
    global isStart,now_ques,userAns
    userAns = es.userAns
    es.reset()
    isStart = False
    now_ques = 0
    gr.Success("Reset 成功")
    return (
        "",
        "A",
        gr.update(interactive=not now_ques == 0 and isStart),
        gr.update(interactive=not now_ques == len(es.Ramdom or [])-1 and isStart),
        gr.update(interactive=len(es.Ramdom or [])-1 == len(es.userAns or []) and isStart),
        f"<center><h4> 未開始 </h4></center>")

def upload_exam(file:NamedString):
    baseName = os.path.basename(file.name)
    with open(file.name,'r') as f:
        data = json.load(f)
    with open(os.path.join(examDir,baseName),'w') as f:
        json.dump(data,f)
    gr.Success("Upload 成功")
    return os.listdir(examDir)

def submit_ans(ans:str):
    set_ans(ans=ans)
    score = es.get_score()
    return f"{score}%",*reset()

with gr.Blocks() as demo:
    gr.Markdown("<center><h2> 題庫練習系統 </h2></center>")
    with gr.Tab():
        with gr.TabItem("題庫管理"):
            file = gr.File(label="上傳題庫", file_types=['.json'])
            sub_file = gr.Button("確認上傳")
        with gr.TabItem("測驗"):
            examSelector = gr.Dropdown(label="請選擇題庫", choices=["請選擇",*get_examList()],interactive=True)
            examSelector.change(set_Exam, inputs=examSelector, outputs=None)
            ramdomSelector = gr.Dropdown(label="隨機出題,題數", choices=['all','25','50'],value='all',interactive=True)
            ramdomSelector.change(set_ramdom, inputs=ramdomSelector, outputs=None)
            start = gr.Button("開始測驗")

            title = gr.Markdown(f"<center><h4> 未開始 </h4></center>")
            ques = gr.TextArea(label="題目",interactive=False,lines=8, max_lines=8)
            ans = gr.Dropdown(label="答案",interactive=True,choices=["A","B","C","D"],value="A")
            with gr.Row():
                prev = gr.Button("上一題",interactive= not now_ques == 0 and isStart)
                next = gr.Button("下一題",interactive= not now_ques == len(es.Ramdom or [])-1 and isStart)
            submit = gr.Button("提交試卷",interactive= len(es.Ramdom or [])-1 == len(es.userAns or []) and isStart)
            score = gr.Textbox(label="得分",interactive=False,value="0%")
    
    @gr.render(None, [submit.click])
    def render_errors():
        gr.Info("顯示錯誤題目中...")
        time.sleep(1)
        global quesObj,userAns
        if quesObj is None:
            raise gr.Error("請先開始測驗")
        errors = [x for x in userAns if x.is_correct == False]
        for item in errors:
            gr.Markdown(f"<center><h4> 第 {item.id + 1} 題 </h4></center>")
            gr.Textbox(label="題目",value=quesObj[item.id].ques,interactive=False)
            gr.Textbox(label="A",value=quesObj[item.id].optionA,interactive=False)
            gr.Textbox(label="B",value=quesObj[item.id].optionB,interactive=False)
            gr.Textbox(label="C",value=quesObj[item.id].optionC,interactive=False)
            gr.Textbox(label="D",value=quesObj[item.id].optionD,interactive=False)
            gr.Textbox(label="答案",value=item.current_ans,interactive=False)
            gr.Textbox(label="解釋",value=quesObj[item.id].description,interactive=False)
        quesObj = []
            

    sub_file.click(upload_exam, inputs=file, outputs=examSelector)
    start.click(get_ques,inputs=None,outputs=[ques,ans,prev,next,submit,title])
    prev.click(back_ques,inputs=[ans],outputs=[ques,ans,prev,next,submit,title])
    next.click(next_ques,inputs=[ans],outputs=[ques,ans,prev,next,submit,title])
    submit.click(submit_ans,inputs=[ans],outputs=[score,ques,ans,prev,next,submit,title])

if __name__ == "__main__":
    demo.launch(debug=True)