[![Python](https://img.shields.io/badge/-Python-black?style=flat&logo=python&logoColor=478CBF)]()
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-black?style=flat&logo=postgresql&logoColor=336791)]()
[![Ollama](https://img.shields.io/badge/-Ollama-black?style=flat&logo=ollama&logoColor=white)]()
[![OpenRouter](https://img.shields.io/badge/-OpenRouter-black?style=flat&logo=openrouter&logoColor=white)]()

<div align="start">
  <img src="./.github/assets/soundwave-logo.png" alt="Soundwave Agent Logo" width="200" height="200"/>
</div>

# Leon

> [!WARNING]
> This project is still in development and undergoing rigorous testing. It will
> be released through a beta (when it's that stable) or through iterations that
> will be available for people to download and fully use. For the beta version,
> we would appreciate if people are willing to test for bugs as it will help
> further refine the project and anything that is broken before a suitable
> release candidate.
>
> This project is also the foundational structure that is created and used for
> Lotus, which is another project within Hikarian forge that goes above and beyond
> with SLMs (Small/Specific Language Models) and training your own agent orchestration
> framework.
>
> Link: [Hikarian-Forge/Lotus](https://github.com/hikarian-forge/lotus)

> Leon, Your digital assistant, on Discord.

Leon is a secure, autonomous AI assistant built for one-on-one use across
multiple social platforms. Starting on Discord and expanding towards
BlueSky, Twitter, UpScrolled, and more. Leon is designed to replace a
specific fragile, "vibecoded" bot with a more principled, production-grade,
assistant that you can trust not to provide malicious users with your
credit card information.

She operates within her own controlled domain, powered by local and
configuration LLMs (via Ollama or OpenRouter, alongside Gemini), and
an entire **STT-LLM-TTS** voice pipeline for real-time voice channel
communication.

## Table of Contents

- [Leon](#leon)
  - [Table of Contents](#table-of-contents)
  - [Architecture \& Features Overview](#architecture--features-overview)
  - [Leon Command Index](#leon-command-index)
  - [Installation](#installation)
    - [Leon Environment Variables](#leon-environment-variables)
  - [Documentation](#documentation)
  - [System Requirements](#system-requirements)
  - [Contact/Socials for Leon](#contactsocials-for-leon)
  - [Contributing](#contributing)

## Architecture & Features Overview

Here are some of the following features that are planned for Leon:

1. **Cross-Platform**: Starts on Discord, with planned support for Bluesky, Twitter,
   UpScrolled, and additional platforms as integrations mature.
2. **Configurable LLM Backend**: Supports local inference via Ollama or cloud models
   through OpenRouter — BYOK supported, your data stays yours.
3. **Voice Pipeline**: Real-time voice interaction using a **STT → LLM → TTS** setup.
   - **STT**: High-accuracy transcription model (TBD).
   - **LLM**: Ollama or OpenRouter-routed models.
   - **TTS**: [Qwen3-TTS-1.7B](https://github.com/QwenLM/Qwen3-TTS) or
     [Kokoro-TTS](https://github.com/thewh1teagle/kokoro-onnx) for expressive,
     human-like audio output.
4. **Persistent Memory & RAG**: PostgreSQL-backed storage with pgvector or Weaviate
   for retrieval-augmented generation across conversations.
5. **Skill System**: A `SKILL.md`-driven capability framework that defines and expands
   what Leon can autonomously execute on your behalf.
6. **Security-First**: Scoped permissions, controlled execution environments, and
   no third-party data exposure — purpose-built to be the opposite of insecure,
   poorly-audited bots.

As for its architecture, the mono repo structure is something I prefer
when making projects of this nature. The architecture is better explained
through the `/docs/arch.README.md` file.

## Leon Command Index

| Command                               | Description                                                              |
|---------------------------------------|--------------------------------------------------------------------------|
| `/ask`                                | Ask Leon anything such as conversational queries, tasks, or instructions |
| `/help`                               | Display available commands and usage guidance                            |
| `/stats`                              | View session statistics and system metrics                               |
| `/system prompt`                      | Set or view the active system prompt                                     |
| `/system context`                     | Manage context window state                                              |
| `/system temperature`                 | Adjust LLM temperature                                                   |
| `/system top-p`                       | Adjust nucleus sampling (top-p)                                          |
| `/system max-completion-tokenization` | Set max completion token limit                                           |
| `/ping`                               | Check Leon's responsiveness and connection status                        |
| `/join`                               | Invite Leon to a voice channel to begin a voice session                  |
| `/leave`                              | Remove Leon from the active voice channel                                |
| `/docs`                               | Access inline documentation                                              |
| `/faq`                                | View frequently asked questions about Leon                               |

## Installation

> [!NOTE]
> You will need to have **Python 3.11+** and **PostgresSQL**
> installed to be able to run this project, or **Docker** if
> intending to use the docker compose file for Postgres. As
> for LLMs, you can use Ollama.
>
> Additionally, if you are testing for a specific feature or
> looking for a specific mechanic to test out, you may need
> to search around to find it, or if it doesn't exist yet
> you may need to further check the documentation details
> to see the status for some of our systems.

To get started with Leon, follow these steps to set up your local
environment:

1. Copy the environment using `git clone`:

```bash
git clone https://github.com/hikues-forge/leon.git .
```

1. Once cloned, install dependencies using your preferred package manager:

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -r requirements.txt

# Using poetry
poetry install

# Using pipenv
pipenv install
```

1. From here, copy the `.env.sample` file into a `.env` file for Leon to use:

> [!WARNING]
> Make sure to add your keys for Openrouter or url for Ollama, if you do
> not provide any key for OpenRouter, it will always default to Ollama and
> and use the default localhost url which is usually `http://localhost:11434/api`.

```bash
cp .env.sample .env 
```

1. After this, if using Docker, set up the docker compose file:

> [!WARNING]
> You can ignore this if you have a local PostgresSQL instance over using
> Docker to set up your instance. If you have both Postgres and Docker, it
> would be best you choose one over the other as you will need to provide a
> proper DATABASE_URL in your environment variables (`.env`).

```bash
docker compose up -d
```

1. Run database migrations after you have provided the DATABASE_URL:

```bash
alembic upgrade head
```

1. Now you should be able to run Leon!

```bash
bash scripts/enable.sh && ./scripts/run.sh
```

### Leon Environment Variables

Leon's behavior is configurable through a `.env` alongside `/system` commands
that you can run through discord (or preferred platform of choice). Here are
the environment variables you **NEED** to have:

| Env                   | Description                                                                        |
|-----------------------|------------------------------------------------------------------------------------|
| `DISCORD_BOT_TOKEN`   | Your Discord bot token                                                             |
| `DATABASE_URL`        | PostgreSQL connection string                                                       |
| `LLM_PROVIDER`        | `ollama`, `openrouter` or `gemini`                                                 |
| `OPENROUTER_API_KEY`  | Required if using OpenRouter                                                       |
| `DEFAULT_MODEL`       | Default model to route completions to, this is heavily dependent on the platform.  |
| `TTS_ENGINE`          | `qwen3` or `kokoro`.                                                               |
| `API_URL`             | The API url to connect to a backend service for Leon.                              |
| `API_ENV`             | This can be either `dev`, `staging` or `prod`                                      |

## Documentation

> [!WARNING]
> A quick disclaimer, I intend to store documentation within a wiki hosted
> usually hosted on my own site. If it's hosted, you can find it at the
> following link:
>
> [Leon Website Link](https://Leon.hikue.dev/)
>
> If it's not hosted, then consider checking out the [docs](/docs/) directory
> for more detail regarding the development status of Backstage, alongside
> some links to socials here and there.

The documentation for Leon is extensively organized into categories
within the `/docs` directory. If you are looking for information regarding
the systems or mechanics of Leon or its internals, your best bet is checking
out `/docs`. Additionally, if you have inquiries about Leon, check out the FAQ page
hosted on our site: [leon.hikue.dev](https://Leon.hikue.dev) or email me!

## System Requirements

> **TODO**: Write proper information about the system requirements for Leo.

## Contact/Socials for Leon

> **TODO**: Write proper information about the contact/socials for Leon.

## Contributing

Contributors are always welcome for Leon. However, we recommend properly reading
through our [CONTRIBUTING.md](/.github/CONTRIBUTING.md) file to get a better understanding of the best
practices and guidelines that you should follow as a contributor.

With that being said, all the best, and to the moon 🚀!
