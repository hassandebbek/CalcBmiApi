#استيراد المكتبات
from fastapi import FastAPI , Query
# pydantic لتحسين الكود
from pydantic import BaseModel
#اعداد CORS للسماح بطلبات من متصفح الويب
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

class BMIOutput(BaseModel):
    bmi: float
    message: str

app = FastAPI()

origins = [
    "https://your-render-app-name.onrender.com",  # السماح من أصل تطبيق Render الخاص بك
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"], #يجب تحديد المجالات المسموح في الانتاج
#    allow_methods=["*"],
#    allow_headers=["*"],
#   )

@app.get("/")
def Hi():
    return {"message": "Marhaba python"}

# سنقوم بتحديد مسار جديد.
@app.get("/calculate_bmi")
def calculate_bmi(
    weight: float = Query(..., gt=20, lt=200, description="الوزن بالكيلوغرام"),
    height: float = Query(..., gt=1, lt=3, description="الطول بالمتر")
):
    bmi = weight / (height ** 2)

    if bmi < 18.5:
        message = "لديك نقص في الوزن، كُل أكثر"
    elif 18.5 <= bmi < 25:
        message = "لديك وزن طبيعي، حافظ عليه"
    elif 25 <= bmi < 30:
        message = "لديك زيادة في الوزن، تمرن أكثر"
    else:
        message = "أنت تعاني من السمنة، قم بمراجعة طبيب"

    return BMIOutput(bmi=bmi,message=message)
    #return {
    #    "bmi": bmi,
    #    "message": message
    #}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) #changed to port 8001