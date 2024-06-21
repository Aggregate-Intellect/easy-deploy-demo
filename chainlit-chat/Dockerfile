# Run `docker build` within the app directory to use this file.

FROM python:3.12-slim-bookworm AS requirements-stage

# Create a Python virtual environment directory and prepend it to PATH
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# `usr/src/app` directory is the root of our application.
WORKDIR /usr/src/app

# Copy app files and install Python environment
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM requirements-stage AS app-stage

ENV LISTEN_PORT 8000
EXPOSE 8000

# Run the application as a Python module from `usr/src/app`
CMD ["python", "-m", "chainlit", "run", "app.py"] 