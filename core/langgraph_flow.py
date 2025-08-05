from langgraph.graph import StateGraph
from typing import TypedDict
import shlex
import subprocess
from ollama import Client

# LLM client
ollama = Client(host="http://localhost:11434")

# 🧠 State schema
class ReviewState(TypedDict, total=False):
    diff: str
    summary: str
    critique: str
    suggestions: str
    security_feedback: str
    architecture_feedback: str
    test_coverage_feedback: str
    ui_feedback: str
    dependency_feedback: str
    performance_feedback: str
    readability_feedback: str

# 🧠 Agent nodes
def summarize_change(state: ReviewState) -> ReviewState:
    print("🧠 Summarizing...")
    diff = state["diff"]

    prompt = (
        "Summarize the purpose of this code diff in 1–3 short bullet points.\n"
        "Avoid repeating variable names or showing the diff itself.\n"
        "Focus on **what changed** and **why**.\n"
        f"```diff\n{diff}\n```"
    )

    response = ollama.chat(model='codellama:7b', messages=[
        {"role": "user", "content": prompt}
    ])

    state["summary"] = response["message"]["content"].strip()
    return state


def critique_change(state: ReviewState) -> ReviewState:
    print("🧪 Critiquing...")
    diff = state["diff"]

    prompt = (
        "Critique this code diff in a few lines.\n"
        "Mention only concrete issues like:\n"
        "- code smells\n"
        "- risky changes\n"
        "- missing error handling\n"
        "Don't restate what the code does. Focus only on problems.\n"
        f"```diff\n{diff}\n```"
    )

    response = ollama.chat(model='codellama:7b', messages=[
        {"role": "user", "content": prompt}
    ])

    state["critique"] = response["message"]["content"].strip()
    return state


def suggest_improvements(state: ReviewState) -> ReviewState:
    print("💡 Suggesting improvements...")
    diff = state["diff"]

    prompt = (
        "Suggest small, high-impact improvements for this code diff.\n"
        "Focus on naming, structure, readability, or maintainability.\n"
        "Avoid vague advice. Use 2–3 concise bullet points.\n"
        f"```diff\n{diff}\n```"
    )

    response = ollama.chat(model='codellama:7b', messages=[
        {"role": "user", "content": prompt}
    ])

    state["suggestions"] = response["message"]["content"].strip()
    return state


def test_coverage_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting coverage improvements...")
    diff = state["diff"]
    if "Test" not in diff and "test" not in diff:
        state["test_coverage_feedback"] = "🛑 Skipped: No test files modified."
        return state

    prompt = (
        "Does this diff contain production logic changes that are not covered by tests?\n"
        "Flag clearly if any functions or cases are missing corresponding test additions.\n"
        "Keep it brief and pointed.\n"
        f"```diff\n{diff}\n```"
    )
    response = ollama.chat(model='codellama:7b', messages=[{"role": "user", "content": prompt}])
    state["test_coverage_feedback"] = response["message"]["content"].strip()
    return state


def ui_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting UI improvements...")
    diff = state["diff"]
    if not any(f in diff for f in [".xml", "@Composable", "Modifier.", "remember"]):
        state["ui_feedback"] = "🛑 Skipped: No Compose or XML UI changes found."
        return state

    prompt = (
        "Review this UI diff (Compose or XML). Flag any issues with:\n"
        "- accessibility\n"
        "- missing preview/composable modifiers\n"
        "- bad UX/state management\n"
        "Respond concisely.\n"
        f"```diff\n{diff}\n```"
    )
    response = ollama.chat(model='codellama:7b', messages=[{"role": "user", "content": prompt}])
    state["ui_feedback"] = response["message"]["content"].strip()
    return state


def security_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting Security improvements...")
    diff = state["diff"]
    prompt = (
        "Scan the following code diff for security issues such as:\n"
        "- hardcoded secrets or credentials\n"
        "- unsafe network calls\n"
        "- missing validation or input sanitization\n\n"
        "Only list clear security risks, if any. Be concise.\n"
        f"```diff\n{diff}\n```"
    )
    response = ollama.chat(model='codellama:7b', messages=[{"role": "user", "content": prompt}])
    state["security_feedback"] = response["message"]["content"].strip()
    return state


def architecture_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting Architecture improvements...")
    diff = state["diff"]
    prompt = (
        "Does this code follow good architecture practices (e.g., MVVM, Clean Architecture)?\n"
        "Flag architectural issues like logic in wrong layer, no separation of concerns, etc.\n"
        "Respond in 2-3 bullet points if needed. Be direct.\n"
        f"```diff\n{diff}\n```"
    )
    response = ollama.chat(model='codellama:7b', messages=[{"role": "user", "content": prompt}])
    state["architecture_feedback"] = response["message"]["content"].strip()
    return state


def dependency_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting Dependency improvements...")
    diff = state["diff"]
    if "implementation" not in diff and "dependency" not in diff:
        state["dependency_feedback"] = "🛑 Skipped: No dependencies updated."
        return state

    prompt = (
        "Analyze any added/updated dependencies in this diff.\n"
        "List concerns like:\n"
        "- use of outdated/unmaintained libs\n"
        "- risky or unnecessary additions\n"
        "Keep it under 3 bullet points.\n"
        f"```diff\n{diff}\n```"
    )
    response = ollama.chat(model='codellama:7b', messages=[{"role": "user", "content": prompt}])
    state["dependency_feedback"] = response["message"]["content"].strip()
    return state


def performance_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting Performance improvements...")
    diff = state["diff"]
    prompt = (
        "Identify any obvious performance issues in this diff.\n"
        "Examples: large allocations in UI thread, repeated computations, unbatched DB writes.\n"
        "Limit to 2-3 lines. Be precise.\n"
        f"```diff\n{diff}\n```"
    )
    response = ollama.chat(model='codellama:7b', messages=[{"role": "user", "content": prompt}])
    state["performance_feedback"] = response["message"]["content"].strip()
    return state


def readability_agent(state: ReviewState) -> ReviewState:
    print("💡 Suggesting Readability improvements...")
    diff = state["diff"]
    prompt = (
            "Evaluate code readability:\n"
            "- Are variable and function names clear?\n"
            "- Is logic unnecessarily complex?\n"
            "- Are there missing comments for non-trivial logic?\n"
            "Summarize in 2–3 lines.\n"
            f"```diff\n{diff}\n```"
        )

    response = ollama.chat(model='codellama:7b', messages=[
            {"role": "user", "content": prompt}
        ])

    state["readability_feedback"] = response["message"]["content"].strip()
    return state



# 🎯 Main runner
def run_review_pipeline(diff: str = "staged"):
    if diff == "staged":
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    else:
        diff_args = shlex.split(diff)
        result = subprocess.run(["git", "diff", *diff_args], capture_output=True, text=True)

    diff_text = result.stdout.strip()

    if not diff_text:
        print("✅ No changes to review.")
        return

    print("📄 Diff preview:\n", diff_text[:300])

    # Initial state
    state: ReviewState = {
        "diff": diff_text,
        "summary": "",
        "critique": "",
        "suggestions": ""
    }

    builder = StateGraph(ReviewState)

    # Core review flow
    builder.add_node("summarize", summarize_change)
    builder.add_node("critique", critique_change)
    builder.add_node("suggestions", suggest_improvements)

    # Specialized agents
    builder.add_node("security", security_agent)
    builder.add_node("architecture", architecture_agent)
    builder.add_node("test_coverage", test_coverage_agent)
    builder.add_node("ui", ui_agent)
    builder.add_node("dependency", dependency_agent)
    builder.add_node("performance", performance_agent)
    builder.add_node("readability", readability_agent)

    # Flow structure
    builder.set_entry_point("summarize")
    builder.add_edge("summarize", "critique")
    builder.add_edge("critique", "suggestions")

    # Parallel agent branches
    builder.add_edge("suggestions", "security")
    builder.add_edge("suggestions", "architecture")
    # builder.add_edge("suggestions", "test_coverage")
    # builder.add_edge("suggestions", "ui")
    # builder.add_edge("suggestions", "dependency")
    # builder.add_edge("suggestions", "performance")
    # builder.add_edge("suggestions", "readability")

    # Finish after last agent
    builder.set_finish_point("readability")

    graph = builder.compile()

    # Run pipeline
    final_state = graph.invoke(state)

    # Output results
    print("\n🧠 Summary:\n", final_state.get("summary", ""))
    print("\n🧪 Critique:\n", final_state.get("critique", ""))
    print("\n💡 Suggestions:\n", final_state.get("suggestions", ""))

    print("\n🔐 Security:\n", final_state.get("security_feedback", ""))
    print("\n📐 Architecture:\n", final_state.get("architecture_feedback", ""))
    print("\n🧪 Test Coverage:\n", final_state.get("test_coverage_feedback", ""))
    print("\n🖼️ UI Review:\n", final_state.get("ui_feedback", ""))
    print("\n📦 Dependencies:\n", final_state.get("dependency_feedback", ""))
    print("\n📊 Performance:\n", final_state.get("performance_feedback", ""))
    print("\n🔤 Readability:\n", final_state.get("readability_feedback", ""))

