from typing import Dict, Optional, Union

from autogen import Agent, AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
import chainlit as cl
import os


load_dotenv()

TASK = "Plot a chart of NVDA, Apple and Tesla stock price change YTD and save it on disk."


async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res


class ChainlitAssistantAgent(AssistantAgent):
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool:
        cl.run_sync(
            cl.Message(
                content=f'*Sending message to "{recipient.name}":*\n\n{message}',
                author="AssistantAgent",
            ).send()
        )
        super(ChainlitAssistantAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


class ChainlitUserProxyAgent(UserProxyAgent):
    def get_human_input(self, prompt: str) -> str:
        if prompt.startswith(
            "Provide feedback to assistant. Press enter to skip and use auto-reply"
        ):
            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="Continue or provide feedback?",
                    actions=[
                        cl.Action(
                            name="continue", value="continue", label="✅ Continue"
                        ),
                        cl.Action(
                            name="feedback",
                            value="feedback",
                            label="💬 Provide feedback",
                        ),
                        cl.Action( 
                            name="exit",
                            value="exit", 
                            label="🔚 Exit Conversation" 
                        ),
                    ],
                )
            )
            if res.get("value") == "continue":
                return ""
            if res.get("value") == "exit":
                return "exit"

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))

        return reply["content"].strip()

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        cl.run_sync(
            cl.Message(
                content=f'*Sending message to "{recipient.name}"*:\n\n{message}',
                author="UserProxyAgent",
            ).send()
        )
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


@cl.on_chat_start
async def on_chat_start():
    api_key = os.getenv("OPENAI_API_KEY")
    config_list = [{
        "model": "gpt-4",
         "api_key": api_key
         }]
    assistant = ChainlitAssistantAgent(
        "assistant", llm_config={"config_list": config_list}
    )
    user_proxy = ChainlitUserProxyAgent(
        "user_proxy",
        code_execution_config={
            "work_dir": "public",
            "use_docker": False,
        },
    )
    await cl.Message(content=f"Starting agents on task: {TASK}...").send()
    await cl.make_async(user_proxy.initiate_chat)(
        assistant,
        message=TASK,
    )
