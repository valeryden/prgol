# Builder stage
FROM python:3.10.13-bookworm as builder
RUN arch

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry==2.0.1

# Set working directory
WORKDIR /app

# Copy poetry toml
COPY pyproject.toml ./

# Install project dependencies (excluding dev dependencies) using Poetry
RUN poetry install --no-root
RUN poetry show streamlit
RUN poetry run streamlit --version

# Runtime stage
FROM python:3.10-slim-bookworm as runtime

# Set environment variables for virtual environment
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy virtual environment from builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Set working directory
WORKDIR /app

# Copy the python script to the container
COPY . /app

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl python3-dev

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs

# Set working directory to frontend and install node packages
WORKDIR /app/frontend

# Ensure the correct ownership of the node_modules directory to avoid permission issues
RUN mkdir -p /app/frontend/node_modules && chown -R root:root /app/frontend/node_modules

# Remove existing node_modules and install npm packages, ensuring a clean state
RUN rm -rf node_modules
COPY frontend/package*.json ./
RUN npm ci && npm install rollup rollup-pluginutils rollup-plugin-svelte

# Run the build process
RUN npm run build

# Change back to the app directory
WORKDIR /app

# Expose port
EXPOSE 8080

# Run App using Python explicitly
CMD ["/app/.venv/bin/streamlit", "run", "src/1.py", "--server.port=8080", "--server.enableCORS=false", "--server.address=0.0.0.0"]
