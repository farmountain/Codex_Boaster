# Setup Guide

This guide explains how to configure and run setup commands via the Terminal Runner.

## Configuration
Available runtime versions are defined by the backend. Typical options include Python 3.11+, Node 18+ and Rust 1.72. Environment variables follow KEY=value format. Saving the form also generates `.env.template.json` with empty values for easy sharing.

1. Navigate to the **Configure Environment** page in the frontend.
2. Adjust the runtime versions for Python, Node or Rust.
3. Add any required environment variables.
4. Enter your setup commands, one per line.

## Example Commands

```
npm install
pip install -r requirements.txt
pytest
```

Click **Run Setup** to execute these commands. Output is streamed to the browser and stored under `logs/runtime/` with a timestamped log file.


## Security

All Terminal Runner endpoints require a valid JWT sent in the `Authorization` header. The token payload must include a `role` field and only users with the `admin` role can execute setup commands. In addition, commands are validated against an allow list of common build tools such as `npm`, `pip`, `pytest`, `python` and `node`. Any command outside this list is rejected.
