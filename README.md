# ai-fast-demos
Fast AI/ML exploration, prototyping, and demo setup (Work in Progress)

## Table of Contents

1. [Usage](#Usage)
1. [Requirements](#requirements)
1. [Development](#development)
    1. [Installing Dependencies](#installing-dependencies)
    1. [Defining and Running Experiments](#defining-and-running-experiments)
    1. [Front End UI Prototyping](#front-end-ui-prototyping)
    1. [Serving FastApi Locally](#serving-fastapi-locally)
    1. [Testing](#testing)
    1. [Code Formatting](#code-formatting)
1. [Outcomes](#outcomes)
1. [Architecture](#architecture)
1. [Roadmap](#roadmap)

## Usage

>Base prototyping setup for Exploratory Data Analysis, model development experimentation, streamlit UIs, prototyping UIs (LLMs, Image GAN), and inference services for a variety of AI/ML use cases. Not intended for production, just a lower friction env for prototyping and demoing AI/ML projects.

## Requirements

- Python 3.11.10 or higher
- Pip 24.2 or higher
- Poetry 1.8.3 or higher
- AWS (For deployment)

## Development

## Configure .env

To store your api keys in development, create a `.env` file in your root dir.
```
touch .env
```

Then store your api keys there
```
OPENAI_API_KEY=you_know_the_drill
...
```

### Installing Dependencies

From within the root directory:

```
poetry install
```

To create an ipykernel associated with this projects virtual env:
```
poetry run python -m ipykernel install --user --name="da_$(basename $(pwd))" --display-name="da_$(basename $(pwd))"
```

### Defining and Running Experiments

From within the root directory:

```
poetry run jupyter lab
```

**Research Summary**
I like to organize my experiments locally under the `/experiments` dir. I'll typically use this to summarize my findings in a notebook file stored there.

**Exploratory Data Analysis & Model Development**
Then in a subdirectory `/experiments/observations` I run my Exploratory Data Analysis and Model Development Iterations in notebook files stored here.

### Front End UI Prototyping

For development, I'm storing base ui templates in a folder titled `streamlit`. To serve locally, run the following command:
```
poetry run streamlit run ./streamlit/text/chat_app.py
```

**Note**
When it comes time to deploy streamlit, if you use their cloudhosting option, they expect filename and folder structure in a specific way. This workflow is on the roadmap to be defined.

### Serving FastApi Locally

From within the root directory:

```
fastapi dev app/main.py
```


### Testing

From within the root directory:

```
poetry run pytest tests
```

### Code Formatting

For this project I'm using the popular [Python Black Code Formatting](https://github.com/psf/black).

### Outcomes

1. Run Exploratory Data Analysis
1. Run Model Development Experiments
1. Prototype frontend UIs quickly
1. Leverage lightweight model servering api
1. Deploy prototype frontend for sharability
1. Deploy model server api
1. Leverage backend prototyping tools for LLMs integrated with deployable frontend and server
1. Leverage backend prototyping tools for Image Generation integrated with deployable frontend and server

### Architecture

- Streamlit: For rapid front end prototyping
- FastApi: For inference api
- Langflow: For rapid prototyping and cloud hosting option

### Roadmap

- Add experiment tracking with mlflow: [MLFlow Quick Start](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html)
- Streamlit cloud deployment
