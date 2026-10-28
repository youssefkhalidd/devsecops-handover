# DevSecOps Handover — Flask Starter

A deliberately small Python Flask application used to demonstrate CI and application-security checks with GitHub Actions.

## What's included

- `app/`: Flask application with home, health, and sample-user endpoints.
- `tests/`: pytest tests.
- `.github/workflows/ci.yml`: runs the tests on pushes and pull requests.
- `.github/workflows/sast.yml`: Semgrep static application security testing.
- `.github/workflows/sca.yml`: dependency auditing with `pip-audit`.
- `.github/workflows/secret-detection.yml`: Gitleaks secret scanning.
- `.github/workflows/dast.yml`: starts the application and runs an OWASP ZAP baseline scan on pushes to `main` or manually.

Each workflow is a separate YAML file so the team can understand and maintain each check independently.

## Run locally

Requires Python 3.12 or compatible.

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and run tests:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

Start the application:

```bash
python -m flask --app app.app run --port 5000
```

Then open `http://127.0.0.1:5000/` or `http://127.0.0.1:5000/health`.

## Create the GitHub repository

1. Create an empty repository named `devsecops-handover` on GitHub.
2. Extract this starter ZIP.
3. From the extracted folder, initialize Git and push the files:

```bash
git init
git add .
git commit -m "Initial Flask app and CI security workflows"
git branch -M main
git remote add origin https://github.com/YOUR-ORG/devsecops-handover.git
git push -u origin main
```

Replace `YOUR-ORG` with your GitHub username or organization.

## Workflow behavior

| Workflow | Runs when | What it does |
|---|---|---|
| CI | Push, pull request, or manual run | Installs dependencies and runs pytest |
| SAST | Push, pull request, or manual run | Scans application code with Semgrep |
| SCA | Push, pull request, or manual run | Audits Python application dependencies |
| Secret Detection | Push, pull request, or manual run | Scans repository history for secrets |
| DAST | Push to `main` or manual run | Starts Flask and runs the ZAP baseline scan |

The ZAP workflow is configured to report findings without failing the workflow (`fail_action: false`) while the team learns the tool. This can be changed later when the team agrees on thresholds and triage procedures.

## Important notes

- These are starter workflows, not a complete production security policy.
- Review action versions and tool output before adopting the workflows in production.
- Do not commit real credentials, tokens, or production data.
- Configure branch protection and required status checks in GitHub repository settings separately; workflow files alone do not enforce merge protection.
- The sample application uses in-memory demo data and is not intended for production.
