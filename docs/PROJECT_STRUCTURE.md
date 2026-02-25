# Project Structure

To get a better sense of our project, here is the project structure:

- [`.github/`](../.github): contains configuration files for GitHub Actions

- [`app/`](../app): contains folders acting as a logical separation between backend and frontend logic.

  - [`backend/`](../app/backend/): contains the backend logic.

    - [`api/`](../app/backend/api/): contains the endpoints for the application.

      - [`routers/`](../app/backend/api/routers/): contains the routers for the endpoints in the application.

    - [`config/`](../app/backend/config/): contains the app states and configurations for prettier modules.

    - [`core/`](../app/backend/core/): contains the core logic, dependencies and configuration for the application.

    - [`database/`](../app/backend/database/): contains the database logic for mongodb and local vector store.

    - [`prepdocslib/`](../app/backend/prepdocslib/): contains the data preparation and ingestion logic to local vector store.

    - [`prompts/`](../app/backend/prompts/): contains the prompt logic.

    - [`schemas/`](../app/backend/schemas/): contains the Pydantic schemas used in the endpoints.

    - [`utils/`](../app/backend/utils/): contains the utility functions or decorators for the backend.

    - [`workflows/`](../app/backend/workflows/): contains the workflow logic.

      - [`components/`](../app/backend/workflows/components/): contains the components logic.

  - [`frontend`](../app/frontend/): contains the frontend logic.

- [`data/`](../data): contains data files for usage with notebook in analysis.

- [`docs/`](../docs): contains documentation for the project.

- [`notebooks/`](../notebooks): contains Jupyter notebooks for experiementation and data analysis.

- [`scripts/`](../scripts): contains scripts for the project.

  - [`load_python_env.*`](../scripts/load_python_env.sh): contains the bash and PowerShell scripts for loading the python environment with uv.

  - [`prepdocs_build.*`](../scripts/prepdocs_build.sh): contains the bash and PowerShell scripts for building the vector store based on the approved_sources.json.

  - [`prepdocs_update.*`](../scripts/prepdocs_update.sh): contains the bash and PowerShell scripts for updating the vector store based on the approved_sources.json (Cost-efficiency).

  - [`start_docker.*`](../scripts/start_docker.sh): contains the bash and PowerShell scripts to build the docker network.

  - [`start.*`](../scripts/start.sh): contains the bash and PowerShell scripts to start the backend server.
