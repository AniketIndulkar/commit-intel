# core/langgraph_flow.py
from typing import Literal

def run_review_pipeline(diff: Literal["staged", "HEAD~1", "HEAD"] = "staged"):
    """
    Main entrypoint for the multi-agent commit review pipeline.
    Currently prints the diff — LangGraph logic comes next.
    """
    import subprocess

    if diff == "staged":
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    else:
        result = subprocess.run(["git", "diff", diff], capture_output=True, text=True)

    diff_text = result.stdout

    if not diff_text.strip():
        print("✅ No changes to review.")
        return

    print("🔍 Running commit reviewer on diff:\n")
    print(diff_text[:1000])  # Print preview for now (we'll process it with agents later)
