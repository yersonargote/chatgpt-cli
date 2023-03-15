import json
import os

import openai
import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

app = typer.Typer(rich_markup_mode="markdown")
console = Console()

systems = {
    "default": """You are an useful, helpful, clever, and very friendly AI assistant.
    - Follow the user's instructions carefully.""",
    "programming": """You are an AI programming assistant.
    - Follow the user's requirements carefully & to the letter.
    - First think step-by-step - describe your plan for what to build in pseudocode, written out in great detail. 
    - Then output the code in a single code block.
    - Minimize any other prose.
    """,
}


def read_conversation(name: str) -> list:
    path = f"{CURR_DIR}/chat"
    dir = f"{path}/{name}.json"
    if os.path.exists(dir):
        with open(dir, "r") as f:
            conversation = json.load(f)
            return conversation
    return []


def save_conversation(name: str, conversation: list):
    path = f"{CURR_DIR}/chat"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"{path}/{name}.json", "w") as f:
        f.write(json.dumps(conversation))


@app.command()
def chat(
    name: str = typer.Argument(
        ...,
        help="Name to load or save a conversation",
    ),
    input: str = typer.Argument(
        ...,
        help="Question for chat",
    ),
    system: str = typer.Argument(
        default="default",
        help="The system message helps set the behavior of the assistant",
    ),
):
    conversation: list = read_conversation(name)

    system = systems[system]
    messages = [{"role": "system", "content": system}]
    messages.extend(conversation)
    messages.append({"role": "user", "content": input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=2048,
    )
    message = response["choices"][0]["message"]["content"]

    md = Markdown(f"**User**: {input}")
    console.print(md)
    md = Markdown(f"**Chat**: {message}")
    console.print(md)

    user = {"role": "user", "content": input}
    assistant = {"role": "assistant", "content": message}
    conversation.append(user)
    conversation.append(assistant)
    save_conversation(name, conversation)
    tokens_used = response["usage"]["total_tokens"]
    md = Markdown(f"**Tokens used**: {tokens_used}")
    console.print(md)


if __name__ == "__main__":
    app()
