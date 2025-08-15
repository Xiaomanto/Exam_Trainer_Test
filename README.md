# Exam_Trainer_Test

### 這是一個一個本地化題庫練習系統

## 環境
 - python 3.10.6
 - [UV](https://docs.astral.sh/uv/)

## 部署

### 下載
``` bash
git clone https://github.com/Xiaomanto/Exam_Trainer_Test.git
cd Exam_Trainer_Test
```

### 建制虛擬環境
``` bash
python -m venv venv
# or
uv venv
```

### 安裝
``` bash
pip install -r requirements.txt
# or 
uv add -r requirements.txt
```

### 啟動
``` bash
python web.py
# or
uv run web.py
```

## 上傳自己的題庫
### 格式
題庫檔案必須為json格式，且需符合以下結構
``` json
[
    {
        "ques": "題目",
        "optionA": "選項A",
        "optionB": "選項B",
        "optionC": "選項C",
        "optionD": "選項D",
        "answer": "答案(只能是 A,B,C,D)",
        "description": "每個選項的說明 A:...,B:...,C:...,D:... "
    },
    ...
]
```

### 上傳
將題庫檔案放置於`exam`資料夾中，並於網頁中選擇題庫名稱即可。

## 開啟網站
[點此開啟已部署並啟動的網頁](http://localhost:7860)