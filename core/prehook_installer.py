# core/prehook_installer.py
import os
from pathlib import Path
import shutil

def install_hook():
    """
    Installs the pre-commit hook from scripts/pre-commit.sh into .git/hooks/
    """
    project_root = Path(__file__).parent.parent
    hook_src = project_root / "scripts" / "pre-commit.sh"
    hook_dst = project_root / ".git" / "hooks" / "pre-commit"

    if not hook_src.exists():
        print("❌ pre-commit.sh not found.")
        return

    shutil.copy(hook_src, hook_dst)
    os.chmod(hook_dst, 0o775)

    print(f"✅ Pre-commit hook installed at: {hook_dst}")
