# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

# 📡 API Overview

| Method | Path                 | Auth required | Description                                        |
| ------ | -------------------- | -------------- | ---------------------------------------------------- |
| GET    | `/`                  | No              | Landing page                                        |
| GET    | `/register`          | No              | Registration page (HTML)                            |
| GET    | `/login`             | No              | Login page (HTML)                                   |
| GET    | `/dashboard`         | No*             | Dashboard page (HTML) \*client-side JS redirects to `/login` if no token is stored |
| GET    | `/health`            | No              | Health check, returns `{"status": "ok"}`             |
| POST   | `/register`          | No              | Register a new user (JSON, `UserCreate` schema)      |
| POST   | `/login`             | No              | Log in with JSON `{username, password}`, returns a JWT + refresh token |
| POST   | `/auth/token`        | No              | OAuth2 form login (used by Swagger's "Authorize" button) |
| POST   | `/calculations`      | Yes (Bearer)    | Create a calculation                                |
| GET    | `/calculations`      | Yes (Bearer)    | List the current user's calculations (Browse)        |
| GET    | `/calculations/{id}` | Yes (Bearer)    | Read a single calculation                            |
| PUT    | `/calculations/{id}` | Yes (Bearer)    | Update a calculation's inputs (recomputes result)     |
| DELETE | `/calculations/{id}` | Yes (Bearer)    | Delete a calculation                                 |

`/register` and `/login` each have two operations at the same path — a `GET` that serves the HTML page and a `POST` that's the JSON API the page's JavaScript calls.

---

# 🔐 Environment Variables

All variables below have working defaults, so the app runs out of the box; override them via a `.env` file or your environment for anything beyond local dev.

| Variable                      | Default (dev)                                              | Purpose                                  |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------------ |
| `DATABASE_URL`                 | `postgresql://postgres:postgres@localhost:5432/fastapi_db`  | SQLAlchemy Postgres connection string    |
| `JWT_SECRET_KEY`                | placeholder string                                          | Signs access tokens                      |
| `JWT_REFRESH_SECRET_KEY`       | placeholder string                                          | Signs refresh tokens                     |
| `ALGORITHM`                    | `HS256`                                                     | JWT signing algorithm                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | `30`                                                        | Access token lifetime                    |
| `REFRESH_TOKEN_EXPIRE_DAYS`    | `7`                                                          | Refresh token lifetime                   |
| `BCRYPT_ROUNDS`                 | `12`                                                        | Password hashing cost factor             |

`docker-compose.yml` already sets these for local development.

---

# 🖥️ Running the Front-End Locally

```bash
docker-compose up
```

Then visit:

- [http://localhost:8000/](http://localhost:8000/) — landing page
- [http://localhost:8000/register](http://localhost:8000/register) — create an account
- [http://localhost:8000/login](http://localhost:8000/login) — log in (stores the JWT in `localStorage`)
- [http://localhost:8000/dashboard](http://localhost:8000/dashboard) — authenticated dashboard (create/list/delete calculations)

Interactive API docs are available at [`/docs`](http://localhost:8000/docs) or [`/redoc`](http://localhost:8000/redoc). To exercise protected endpoints from Swagger, click **Authorize** and log in against `/auth/token`.

---

# 🧪 Running Playwright E2E Tests Locally

1. Install dependencies and the Playwright browser binary:

```bash
pip install -r requirements.txt
playwright install chromium
```

2. Start Postgres:

```bash
docker-compose up -d db
```

3. Run the E2E suite (spins up its own `uvicorn` subprocess automatically via the `fastapi_server` fixture — no need to run the app separately):

```bash
pytest tests/e2e/test_auth_pages.py -v
```

Or run the full test suite (unit + integration + e2e):

```bash
pytest
```

Useful flags: `pytest --run-slow` (also run `@pytest.mark.slow` tests), `pytest --preserve-db` (keep the test database after the run).

---

# ⚙️ CI/CD

![CI/CD](https://github.com/HackAndQuack/Project-IS218-Module-13/actions/workflows/ci-cd.yml/badge.svg)

GitHub Actions (`.github/workflows/ci-cd.yml`) runs two jobs:

- **`test`** — runs on every push and pull request against `main`. Spins up a `postgres:17` service container, installs dependencies and Playwright's Chromium browser, and runs the full `pytest` suite (including the Playwright E2E tests).
- **`build-and-push`** — runs only on pushes to `main` or version tags (never on pull requests), after `test` passes. Builds the Docker image and pushes it to Docker Hub.

Before `build-and-push` can succeed, add two **repository secrets** (Settings → Secrets and variables → Actions → New repository secret):

- `DOCKERHUB_USERNAME` — your Docker Hub username.
- `DOCKERHUB_TOKEN` — a Docker Hub **access token** (Account Settings → Security → Access Tokens), not your account password.

---

# 🐳 Docker Hub

Image: [`hackandquack/project-is218-module-13`](https://hub.docker.com/r/hackandquack/project-is218-module-13)

```bash
docker pull hackandquack/project-is218-module-13:latest
docker run -p 8000:8000 --env-file .env hackandquack/project-is218-module-13:latest
```
