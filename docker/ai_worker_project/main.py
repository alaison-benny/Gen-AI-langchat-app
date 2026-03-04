from fastapi import FastAPI
from celery import Celery
from worker import analyze_text
from celery.result import AsyncResult

app = FastAPI()

# 1. Celery സെറ്റപ്പ്: Broker ഉം Backend ഉം ഇവിടെ ഡിഫൈൻ ചെയ്യുന്നു
celery_app = Celery('tasks', 
                    broker='redis://redis:6379/0', 
                    backend='redis://redis:6379/0')

@app.get("/")
def read_root():
    return {"status": "API is running"}

# 2. സെന്റിമെന്റ് അനാലിസിസ് ചെയ്യാൻ ഓർഡർ കൊടുക്കുന്നു
@app.post("/analyze")
def trigger_analysis(text: str):
    task = analyze_text.delay(text) # ജോലി ക്യൂവിലേക്ക് വിടുന്നു
    return {"task_id": task.id, "status": "Processing"}

# 3. ജോലിയുടെ റിസൾട്ട് വന്നെന്ന് നോക്കുന്നു
@app.get("/result/{task_id}")
def get_result(task_id: str):
    # ഇവിടെ നമ്മൾ മുകളിൽ ഉണ്ടാക്കിയ celery_app ഉപയോഗിച്ച് റിസൾട്ട് നോക്കുന്നു
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        return {"status": "Completed", "result": result.result}
    return {"status": "Pending"}
