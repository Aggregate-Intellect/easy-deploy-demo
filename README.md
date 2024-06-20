# easy-deploy-demo
This is a small app built for the
[Build Multi-agent LLM Products](https://maven.com/aggregate-intellect/llm-systems?promoCode=aisc) course. The goal is to demonstrate how
straightforward it is deploying a simple Python web app with
a chat-style interface, providing question-answering powered
by a Large Language Model.

The app uses these major components:
* [Chainlit](https://docs.chainlit.io/) for a chat-style UI built in Python
* the [OpenAI library](https://platform.openai.com/docs/libraries) for LLM chat completions
* [Fly.io](https://fly.io) for deployment

While this demo isn't meant to be an endorsement of any particular tech, we have found this particular stack quite convenient for quick and easy deploys of chat-style LLM apps.


## Pre-requisites
- Python >= 3.8
- [pip](https://packaging.python.org/en/latest/guides/tool-recommendations/)
- An [OpenAI Account](https://platform.openai.com/signup) and [API key](https://platform.openai.com/account/api-keys)
- A [Fly.io](https://fly.io) account


## Step 1: Install

Begin by cloning this git repo. 

Then, in a terminal within the repository root directory, ...

```bash
python -m venv .venv 

source .venv/bin/activate

pip install --upgrade pip

pip install chainlit openai python-dotenv

chainlit hello
```

You should see a test Chainlit app running.

If you got stuck anywhere up to here, see the
[Chainlit installation docs](https://docs.chainlit.io/get-started/installation) for help.


## Step 2: Run the app locally
Since our app will connect to the OpenAI platform we
need to copy the value of our [API key](https://platform.openai.com/account/api-keys) into a file called `.env` in the root of the repository.

Copy the sample `.env` file...
```bash
cp sample.env .env
```
... and then edit `.env` to contain your key.

Once you have done this you can run the demo app:

```bash
chainlit run app.py -w
```

The -w flag makes Chainlit reload after each file change. Any changes you make to `app.py` will be reflected 
immediately in your web browser. This is useful for iterative development, and not used in production.


## Step 3: Prepare to deploy to fly.io

```bash
pip freeze > requirements.txt

brew install flyctl

fly auth signup

fly auth login

fly launch
```

You can accept the `fly launch` defaults or tweak them as you see fit.

Before launching the app, go to your [Fly dashboard](https://fly.io/dashboard/) and add an app secret called `OPENAI_API_KEY` to your newly
created app. Enter the value of your API key.


## Step 4: Deploy to fly.io

```bash
fly deploy
```

At this point Fly builds a docker file for you based on the contents of the
`requirements.txt` file and deploys the app.
This can take a few minutes. After this finishes you should
have the demo app running at a URL on the `fly.dev` domain. Enjoy!

You can now make changes to files on your local machine,
save the changes, run locally (use the `-w` flag to get automatic reload), and redeploy using `fly deploy`.

As an alternative to the fully automated build you can create your own Dockerfile in the root of this repository. Fly will build and run your Dockerfile instead of generating one. This is often a useful thing to do, as you can run your Docker image in many places, including other developer laptops and other deployment environments that run Docker containers.


## Other useful fly.io commands
Since this app uses sockets (a Chainlit requirement), and we don't have a load balancer in front of it, we want only a single instance of the app to be running in each fly.io deployment region. You can do this with the command 
`fly scale count 1 `.

Other useful fly commands:

Tail logs: `fly logs`

Restart the app: `fly apps restart`

Scale instances to 0: `fly scale count 0 `

SSH to console: `fly ssh console`


## Credits
SVG icons are from the [Chainlit Cookbook](https://github.com/Chainlit/cookbook/tree/b3b6f38da1a28c23e4f46ad54bf1e67b32036590/openai-data-analyst).