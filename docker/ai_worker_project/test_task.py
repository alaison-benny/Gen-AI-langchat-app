from worker import analyze_text
import time

# 1. ഒരു വാചകം വിശകലനം ചെയ്യാൻ വർക്കറിലേക്ക് അയക്കുന്നു
print("Sending text to AI Worker...")
job = analyze_text.delay("I am very happy with this AWS setup!")

# 2. റിസൾട്ടിനായി കാത്തുനിൽക്കുന്നു (Asynchronous ആയതുകൊണ്ട് ഉടനെ കിട്ടില്ല)
print(f"Task ID: {job.id}")
print("Waiting for result...")

while not job.ready():
    print("AI is thinking...")
    time.sleep(1)

# 3. റിസൾട്ട് കാണിക്കുന്നു
print(f"Result: {job.result}")
