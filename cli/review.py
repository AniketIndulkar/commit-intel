# cli/review.py

import typer
from core.langgraph_flow import run_review_pipeline
from core.jacoco_agent import run_coverage_analysis
from core.prehook_installer import install_hook

app = typer.Typer()

@app.command()
def commit(
    diff: str = typer.Option("HEAD~1", help="Git diff: HEAD~1, HEAD~3..HEAD, etc.")
):
    """
    Run the commit review agent on a commit diff (default: HEAD~1).
    """
    typer.echo(f"🔍 Running LLM commit review on diff: {diff}...")
    run_review_pipeline(diff=diff)

@app.command()
def staged():
    """
    Run the commit review agent on currently staged changes.
    """
    typer.echo("🔍 Running LLM review on staged changes...")
    run_review_pipeline(diff="staged")

@app.command()
def coverage():
    """
    Run the JaCoCo test coverage analysis agent.
    """
    typer.echo("📊 Reviewing test coverage...")
    run_coverage_analysis()

@app.command()
def install_prehook():
    """
    Install the Git pre-commit hook that runs the reviewer.
    """
    install_hook()

if __name__ == "__main__":
    app()
