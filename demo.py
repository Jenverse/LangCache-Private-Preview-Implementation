import typer
import os
from dotenv import load_dotenv
from jinja2 import Template
from python_on_whales import docker
from python_on_whales.exceptions import NoSuchImage

app = typer.Typer()

@app.command()
def setup():
    gcp_key = input("Enter your GCP API key: ")
    openai_key = input("Enter your OpenAI API key: ")

    with open(".env.example", 'r') as f:
        template_content = f.read()

    template = Template(template_content)
    rendered_content = template.render(
        GCP_API_KEY=gcp_key,
        OPENAI_API_KEY=openai_key
    )

    with open(".env", 'w') as f:
        f.write(rendered_content)

@app.command()
def show():
    containers = docker.compose.ps()
    for container in containers:
        container_id = container.id[:12] if container.id else "Unknown"
        image = container.config.image if hasattr(container.config, 'image') and container.config.image else "Unknown"
        print(f"{container_id} - {image}")

@app.command()
def build():
    print("Building demo")
    docker.compose.build()

@app.command()
def clean():
    print("Cleaning demo")
    try:
        docker.image.remove("llm-app:latest")
        print("Removed llm-app image")
    except NoSuchImage as e:
        pass

def render_config(template_file="config-template.yaml"):
    load_dotenv()
    openai_key = os.environ.get('OPENAI_API_KEY', '')

    with open(template_file, 'r') as f:
        template_content = f.read()

    template = Template(template_content)
    rendered_content = template.render(OPENAI_API_KEY=openai_key)

    with open("config.yaml", 'w') as f:
        f.write(rendered_content)

@app.command()
def start():
    print("Writing config file")
    render_config()
    print("Starting demo")
    docker.compose.up(
        services=[
            "llm-app"
        ],
        build=True,
        detach=True
    )
    show()

@app.command()
def stop():
    print("Stopping demo")
    docker.compose.down(
        services=[
            "llm-app",
            "cache-db1",
            "ollama",
            "embeddings-api"
        ],
        volumes=True
    )

if __name__ == "__main__":
    app()
