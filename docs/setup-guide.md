# Setup Guide

This guide explains how to configure and run setup commands via the Terminal Runner.

## Configuration

1. Navigate to the **Configure Environment** page in the frontend.
2. Adjust the runtime versions for Python, Node or Go.
3. Add any required environment variables.
4. Enter your setup commands, one per line.

## Example Commands

```
npm install
pip install -r requirements.txt
pytest
```

Click **Run Setup** to execute these commands. Output is streamed to the browser and stored under `logs/runtime/` with a timestamped log file.

