# core/langgraph_flow.py
from typing import Literal
# core/langgraph_flow.py
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing import Dict
from ollama import Client

def run_review_pipeline(diff: str = "staged"):
    import subprocess

    # Get the Git diff
    if diff == "staged":
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    else:
        result = subprocess.run(["git", "diff", diff], capture_output=True, text=True)

    diff_text = result.stdout.strip()

    if not diff_text:
        print("✅ No changes to review.")
        return

    # Build the LangGraph
    builder = StateGraph()
    builder.set_entry_point("summarize")
    builder.add_node("summarize", summarize_change)
    builder.add_node("critique", critique_change)
    builder.add_node("suggestions", suggest_improvements)

    builder.add_edge("summarize", "critique")
    builder.add_edge("critique", "suggestions")
    builder.set_finish_point("suggestions")

    graph = builder.compile()

    # Run the pipeline
    output = graph.invoke({"diff": diff_text})

    print("\n🧠 Commit Summary:\n", output["summary"])
    print("\n🧪 Critique:\n", output["critique"])
    print("\n💡 Suggestions:\n", output["suggestions"])





ollama = Client(host="http://localhost:11434")  # local LLM

# 1️⃣ Agent: Summarize
def summarize_change(state: Dict) -> Dict:
    diff = state["diff"]
    prompt = f"You are a senior Android developer. Summarize the following code diff:\n\n```diff\n{diff}\n```"
    response = ollama.chat(model='codellama', messages=[{"role": "user", "content": prompt}])
    state["summary"] = response['message']['content']
    return state

# 2️⃣ Agent: Critique
def critique_change(state: Dict) -> Dict:
    diff = state["diff"]
    prompt = f"Critique this commit for potential bugs, poor practices, or risky logic:\n\n```diff\n{diff}\n```"
    response = ollama.chat(model='codellama', messages=[{"role": "user", "content": prompt}])
    state["critique"] = response['message']['content']
    return state

# 3️⃣ Agent: Suggestions
def suggest_improvements(state: Dict) -> Dict:
    diff = state["diff"]
    prompt = f"Suggest clear improvements to this commit:\n\n```diff\n{diff}\n```"
    response = ollama.chat(model='codellama', messages=[{"role": "user", "content": prompt}])
    state["suggestions"] = response['message']['content']
    return state

