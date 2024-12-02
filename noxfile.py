"""
This file is used to configure Nox for running lint, format, and test tasks in CI/CD pipelines.
In this project, it runs with uv backend.
"""

import nox

# lint and format sessions with ruff
@nox.session(venv_backend="uv", python=["3.12"], tags=["lint"])
def lint(session):
    session.install("ruff")
    session.run("uv", "run", "ruff", "check")
    session.run("uv", "run", "ruff", "format")
    
# security check
@nox.session(venv_backend="uv", python=["3.12"], tags=["security"])
def security(session):
    session.install("safety", "bandit")
    
    # check for dependencies
    session.run("safety", "check")
    
    # statistic check for security issues
    session.run("bandit", "-r", "src", "-c", "pyproject.toml")
    
# test sessions with pytest
@nox.session(venv_backend="uv", python=["3.12"], tags=["test"])
def test(session):
    session.run("uv", "sync", "--dev")

    if session.posargs:
        test_files = session.posargs
    else:
        test_files = ["tests"]

    session.run(
        "uv",
        "run",
        "pytest",
        "--junitxml=reports/test-results/pytest-results.xml",
        "--cov=src",
        "--cov-report=html:reports/coverage/html",
        "--cov-report=xml:reports/coverage/coverage.xml",
        *test_files,
    )
    
@nox.session(venv_backend="uv", python=["3.11", "3.12"], tags=["integration"])
def integration(session):
    """integration test"""
    session.run("uv", "sync", "--dev")
    
    session.run(
        "pytest",
        "tests/integration",
        "--junitxml=reports/test-results/integration-results.xml",
    )