# DBTT_G5T1

Code Repository for IS215 Digital Business (Technologies and Transformation) G5 Team 1

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Install Dependencies](#install-dependencies)
- [Project Structure](#project-structure)
- [Setting up Environment](#setting-up-environment)
- [Development](#development)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
- [Submission Preparation](#submission-preparation)

## Getting Started <a id="getting-started"></a>

### Prerequisites <a id="prerequisites"></a>

- [Python 3.12 or higher](https://www.python.org/downloads/)
  - Ensure you can run `python --version` from console. On Ubuntu, you might need to run `sudo apt install python-is-python3` to link `python` to `python3`.
- [Git](https://git-scm.com/downloads)
- [PowerShell 7+ (pwsh)](https://github.com/powershell/powershell) — For Windows users only.
  - Ensure you can run `pwsh.exe` from a PowerShell terminal. If this fails, you likely need to upgrade PowerShell.
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
  - [Bump My Version](https://callowayproject.github.io/bump-my-version/tutorials/getting-started/) - Recommended to install if you are already using uv. Otherwise, this is optional.

### Create a Virtual Environment <a id="create-a-virtual-environment"></a>

**uv (Recommended)**

To manage our project dependencies, we are using uv which is an extremely fast Python package and project manager, written in Rust. For more information on how to get started with uv, please visit the [uv documentation](https://docs.astral.sh/uv/).

To create a virtual environment, run the following command:

```bash
uv venv
```

Once you have created a virtual environment, you may activate it.

On Linux or macOS, run the following command:

```bash
source .venv/bin/activate
```

On Windows, run:

```powershell
.venv/Scripts/activate
```

### Install Dependencies <a id="install-dependencies"></a>

```bash
uv sync
```

## Project Structure <a id="project-structure"></a>

For more information on our project structure, please refer to the [Project Structure](./docs/PROJECT_STRUCTURE.md) guide.

## Setting up Environment

1. **Start with template:** Duplicate the `.env.sample` and rename the file as `.env`.

2. **Set up API Keys:** Set up API keys and fill up missing fields in `.env`.

   - **[Groq](https://console.groq.com/docs/quickstart):** Access to main model used in project (SLMs).
   - **[OpenAI](https://developers.openai.com/api/docs/quickstart):** Access to the text embedding features and secondary model used in project (LLMs).
   - **[LangSmith](https://docs.langchain.com/langsmith/create-account-api-key):** Access to monitoring capabilities to analyse orchestration layer.
   - **[MongoDB](https://www.mongodb.com/resources/products/fundamentals/mongodb-connection-string):** Connects the application to a database to store patient details and chat history. Requires setting up a cluster to obtain connection string.

3. **Configure environment:** Default fields in `.env.sample` should run, but fields can be adjusted to support different SLM/LLM/Embedding models, Tracing Project, Database name and Logging Level.

4. **Duplicate environment:** Duplicate the `.env` file and paste it within the `app/backend` directory to run the FastAPI application.

## Development

### Running Locally <a id="running-locally"></a>

**Run Locally**: Start the server:

```bash
make start
```

> [!NOTE]
> If for any reason, you have trouble running the make command, you may try the following commands:
>
> For Linux or macOS users, run:
>
> ```bash
> ./scripts/start.sh
> ```
>
> For Windows users, run:
>
> ```powershell
> ./scripts/start.ps1
> ```

The script will install the dependencies and start the server and client.

### Running with Docker <a id="running-with-docker"></a>

You can also run the application using Docker. Below are the steps on how the application is ran using Docker:

**Run Locally with Docker**: Start the server:

```bash
make start-docker
```

> [!NOTE]
> If for any reason, you have trouble running the make command, you may try the following commands:
>
> For Linux or macOS users, run:
>
> ```bash
> ./scripts/start_docker.sh
> ```
>
> For Windows users, run:
>
> ```powershell
> ./scripts/start_docker.ps1
> ```

To stop the server, run:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down
```

## Submission Preparation <a id="submission-preparation"></a>

1. Running formatting checker prior to committing can be done by running:

> ```bash
> make lint
> ```
>
> This performs all the necessary checks that will be performed in the CI

2. Reduce space by removing all unnecessary files (e.g., .venv, cache files), run:

> ```bash
> git clean -fdx
> ```
>
> This removes all files that are not indicated in the .gitignore
