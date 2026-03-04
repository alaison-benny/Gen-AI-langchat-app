from celery import Celery
from transformers import pipeline

# 1. Celery സെറ്റപ്പ്: Broker ഉം Backend ഉം Redis ആയി നൽകുന്നു
app = Celery('tasks', 
             broker='redis://redis:6379/0', 
             backend='redis://redis:6379/0')

# 2. AI Model ലോഡ് ചെയ്യുന്നു
print("Loading AI Model...")
model = pipeline("sentiment-analysis")

# 3. AI ടാസ്ക് ഡിഫൈൻ ചെയ്യുന്നു
@app.task
def analyze_text(text):
    # AI ഉപയോഗിച്ച് വാചകം പരിശോധിക്കുന്നു
    result = model(text)
    # റിസൾട്ടിലെ ആദ്യത്തെ ഐറ്റം മാത്രം നൽകുന്നു (ഉദാ: {'label': 'POSITIVE', 'score': 0.99})
    return result[0]
