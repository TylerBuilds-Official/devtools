"""Templated content for .gitignore files"""


PYTHON: str = """\
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
dist/
*.egg-info/
*.egg

# Virtual environments
.venv/
venv/
env/
ENV/

# Testing / coverage
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local

# Logs
*.log
logs/
"""
