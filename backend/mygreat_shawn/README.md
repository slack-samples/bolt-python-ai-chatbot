# Chronosphere Slackbot Knowledge Repository

This project is a Slackbot-powered knowledge system using **FastAPI** and **SQLite** to centralize, organize, and preserve critical team information for migration, monitoring, conversions, and best practices—making knowledge discoverable beyond Slack message scrolling.

***

## Features

- **Query Conversion Database**  
  Store, retrieve, and search conversions (e.g., Graphite → PromQL) with full explanations and provenance.
  
- **Guidance Management**  
  Document and update team guidance—like query standards, usage policies, and migration SOPs—ensuring everyone has access to the latest recommendations.
  
- **Standardizations Tracker**  
  Track and announce processes or query patterns the team should standardize on, with status review and links to related guidance.
  
- **Message Response Repository**  
  Save and search solutions to frequently encountered migration errors or technical issues directly from Slack channel history.
  
- **Tagging and Search**  
  Group knowledge with flexible tags and search APIs for fast Slack-triggered lookups.

## Tech Stack

- **Backend:** FastAPI (async RESTful API)
- **Database:** SQLite (SQLAlchemy ORM)
- **Bot Framework:** slack-bolt for Python (Socket Mode compatible; easily connects with Slack event API)
- **Deploy:** Local development or Docker for hosted environments

***

## Getting Started

### Prerequisites

- Python 3.10+
- Slack workspace with App integration privileges
- SQLite (or Docker)
- `slack-bolt` Python library
- FastAPI, SQLAlchemy packages (`pip install fastapi[all] sqlalchemy slack_bolt`)

### Setup

1. **Clone the repo and install dependencies:**

    ```bash
    git clone <YOUR-REPO-URL>
    cd chronosphere-slackbot
    pip install -r requirements.txt
    ```

2. **Configure Slack:**
    - Go to [Slack API](https://api.slack.com/apps)
    - Create an App
    - Add OAuth scopes: `chat:write`, `app_mentions:read`, `commands`
    - Install the App to your workspace and grab the tokens
    - Set environment variables:
      ```
      SLACK_BOT_TOKEN=xoxb-***
      SLACK_SIGNING_SECRET=***
      ```

3. **Run the FastAPI backend:**

    ```bash
    uvicorn main:app --reload
    # Default at http://localhost:8000
    ```

4. **Start the Slackbot listener (example):**

    ```bash
    python slackbot_handler.py
    ```

    *Slackbot listens for events and hits the FastAPI API as needed.*

***

## API Reference

### Query Conversions

- `POST /conversions/` - Add conversion (Graphite → PromQL)
- `GET /conversions/` - List conversions (filter by customer, etc.)
- `GET /conversions/search/?query=` - Search by asset_title or explanation

### Guidance

- `POST /guidance/` - Add/update a guidance item
- `GET /guidance/` - List/filter by customer
- `GET /guidance/search/?title=` - Search by title

### Message Responses

- `POST /responses/` - Add response to team issue/frequent problem
- `GET /responses/` - List by issue_topic or customer
- `GET /responses/search/?tag=` - Search by tag/keywords

### Standardizations

- `POST /standardizations/` - Add/track a team standard/process
- `GET /standardizations/` - List by status
- `GET /standardizations/search/?query=` - Search by item

### Tags

- `POST /tags/` - Add a new tag
- `GET /tags/` - List all tags

*Each table links knowledge to customer, asset, and topic for deep search and provenance.*

***

## Slackbot Integration

- **Slash Commands**: Set `/convert`, `/guidance`, `/issue` to hit API endpoints.
- **App Mentions**: Slackbot listens and responds using FastAPI queries.
- **Webhook Events**: Connect Slack events to backend endpoints for dynamic updates and lookups.
- **Socket Mode**: Recommended for local dev and private endpoints.

*See `slackbot_handler.py` for examples of listening and processing Slack events.*

***

## Extending and Scaling

- Add PATCH/PUT/DELETE endpoints for item updates/removal.
- Enhance search with full-text or semantic (AI) lookups.
- Abstract database for future migration to PostgreSQL.
- Integrate notifications, feedback, and analytics for team learning.

***

## Contribution & License

- Fork, PR, and issue reports welcome!
- License: MIT / Chronosphere internal, as applicable.

***

## Acknowledgements

Built for the 2025 Chronosphere Team Hackathon.  
Inspired by best practices in observability, monitoring, migration, and collaboration automation.[1][6]

***

*For questions, look for `#slackbot-repo` in Slack or contact the project maintainers.*

[1](https://github.com/Ricardo-VP/slack-bot-fastapi)
[2](https://fastapi.tiangolo.com/project-generation/)
[3](https://www.val.town/x/chuphucben/slackBotExample/code/README.md)
[4](https://docs.ai.science/en/readthedoc_fix/How_To/Slack%20Bot/readme.html)
[5](https://thepythoncode.com/article/build-rag-chatbot-fastapi-openai-streamlit)
[6](https://ducky.ai/blog/build-semantic-search-for-slack)
[7](https://ai-sdk.dev/cookbook/guides/slackbot)
[8](https://www.youtube.com/watch?v=6P2L6azlLEI&vl=en)