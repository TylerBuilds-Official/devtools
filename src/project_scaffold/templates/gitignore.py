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


NODE: str = """\
node_modules/
dist/
build/
.cache/
.parcel-cache/

# IDEs
.vscode/
.idea/

# Env
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
