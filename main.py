import datetime
import os
import time

from src.AI import prompts
from src import actions
from src.AI.BASE import Gen


if "gemini_api_key" not in os.listdir("src/AI/"):
    with open("src/AI/gemini_api_key", "w", encoding="utf-8") as f:
        f.write(input("[Gemini API Key] "))

ai = Gen()
ai.system_instructions = [
    {"text": prompts.Instructions.first_instruction},
    # {"text": prompts.Instructions.action_instruction},
    {"text": prompts.Instructions.examples}]
ai.import_history_anyway("conversations/history")


msg = None

while True:
    if not msg:
        msg = f"{str(datetime.datetime.now())}\nfrom_user||"+input("[user] ")
    ai.history_add("user", msg)
    result = ai.generate()
    ai.history_add("assistant", result)
    try:
        target = result.split("||")[0]
        if target.lower() == "user":
            print("[assistant] " + result.split("||")[1])
            ai.export_history("conversations/history")
            msg = None

        elif target.lower() == "system":
            title = result.split("||")[1]
            func4exec = result.split("||")[2]
            print(f"[assistant]", title)

            func4exec = func4exec.replace("```python", "")
            func4exec = func4exec.replace("```", "")

            exec(func4exec)
            result = eval("f4exec()")
            msg = f"{str(datetime.datetime.now())}\nfrom_user||{result}"
    except Exception as e:
        print(e)
        msg = 'error||' + str(e)
    time.sleep(3)

