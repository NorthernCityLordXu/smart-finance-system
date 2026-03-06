from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
# 1. 从你的 classifier.py 引入刚刚写的预测函数
from classifier import predict_category 

app = FastAPI()

class BillRequest(BaseModel):
    description: str

@app.post("/api/classify")
async def classify_bill(request: BillRequest):
    desc = request.description
    
    # 2. 调用真实的算法大脑！
    real_category = predict_category(desc) 
    
    return {
        "code": 200,
        "description": desc,
        # 3. 返回真实的分类结果
        "category": real_category 
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)