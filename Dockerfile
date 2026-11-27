# Build from the repo root: docker build -f Dockerfile .
# Pipecat Cloud GitHub builds use the repo root as the build context.
FROM dailyco/pipecat-base:latest

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Uncomment if you wish to print a summary of the features available in the base image
# ENV PCC_LOG_FEATURES_SUMMARY=true

# Publish each call's whole conversation (user, bot, and tool calls) to Pipecat Cloud
# when the call ends. Off by default. Needs pipecat-ai 1.13 or later.
ENV PCC_EVAL_CONVERSATIONS=true

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=server/uv.lock,target=uv.lock \
    --mount=type=bind,source=server/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy the application code
COPY ./server/bot.py bot.py
COPY ./server/handlers.py handlers.py
COPY ./server/flow.yaml flow.yaml