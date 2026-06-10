import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# إعداد الـ Client بحيث يقرأ الـ Key من السيرفر علطول
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class AgentRequest(BaseModel):
    prompt: str
    method: str

# 1. Router Pattern
def router_logic(user_input):
    if user_input.lower().startswith("math:"):
        prompt = f"You are a math teacher. Solve clearly: {user_input}"
    elif user_input.lower().startswith("translate:"):
        text = user_input.split("translate:", 1)[1].strip()
        prompt = f"You are a translator. Translate this to Arabic: {text}"
    else:
        prompt = f"You are a creative writer. Answer: {user_input}"
    
    resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return resp.text

# 2. Parallelization Method
async def ask_parallel(role, instruction):
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=instruction,
        config={'system_instruction': f"You are a helpful {role}."}
    )
    return response.text

async def parallel_logic(user_request):
    tasks = [
        ask_parallel("Researcher", f"List 5 key beginner topics for: {user_request}"),
        ask_parallel("Curator", f"Suggest 3 free online resources for: {user_request}"),
        ask_parallel("Planner", f"Make a 3-day study plan for: {user_request}"),
    ]
    results = await asyncio.gather(*tasks)
    roles = ["Researcher", "Curator", "Planner"]
    return "\n\n".join([f"--- {r} ---\n{o}" for r, o in zip(roles, results)])

# 3. Orchestrator-Worker Pattern
async def orchestrator(task):
    config = types.GenerateContentConfig(
        system_instruction="Break this task into exactly 3 subtasks. Write each subtask on a separate line. Do not include numbers, bullet points, or markdown asterisks."
    )
    response = await client.aio.models.generate_content(model="gemini-2.0-flash", contents=task, config=config)
    steps = response.text.split("\n")
    return [s.strip(" .* ") for s in steps if s.strip()][:3]

async def worker(subtask):
    response = await client.aio.models.generate_content(model="gemini-2.5-flash", contents=f"Do this subtask in 3–4 sentences: {subtask}")
    return response.text

async def synthesizer(results: list):
    joined = "\n\n".join(results)
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Combine these into a single short comprehensive guide:\n{joined}",
        config=types.GenerateContentConfig(temperature=0.4)
    )
    return response.text

async def orchestrator_logic(task):
    subtasks = await orchestrator(task)
    results = await asyncio.gather(*(worker(s) for s in subtasks))
    final = await synthesizer(results)
    return final

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        return {"error": "GEMINI_API_KEY is missing in Space Variables!"}
    
    try:
        if request.method == "router":
            result = router_logic(request.prompt)
            return {"agent_response": result}
        elif request.method == "parallel":
            result = await parallel_logic(request.prompt)
            return {"agent_response": result}
        elif request.method == "orchestrator":
            result = await orchestrator_logic(request.prompt)
            return {"agent_response": result}
        else:
            return {"error": "Method not found!"}
    except Exception as e:
        return {"error": str(e)}
