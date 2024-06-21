# Run this from the root of the repository so that 
# Docker uses the root as its build context.

FROM python:3.12-slim-bookworm AS requirements-stage

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# `usr/src/app` directory is the root of our application.
WORKDIR /usr/src/app

# Install Python environment
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# Copy the app files and files commonly used by all apps
COPY chainlit-chat/ chainlit-chat/
RUN mv chainlit-chat/public chainlit-chat/config.toml ./

FROM requirements-stage AS app-stage

ENV LISTEN_PORT 8000
EXPOSE 8000

# Run the application as a Python module from `usr/src/app`
CMD ["python", "-m", "chainlit", "run", "chainlit-chat/app.py"] 