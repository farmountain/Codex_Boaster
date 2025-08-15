"""High level adapters wrapping tool invocations via the LocalHub."""
from __future__ import annotations

from typing import Any, Dict, List

from .hub import LocalHub

_hub = LocalHub()


def repo(action: str, path: str, message: str = "") -> Dict[str, Any]:
    return _hub.call("repo", {"action": action, "path": path, "message": message})


def lint(targets: List[str]) -> Dict[str, Any]:
    return _hub.call("lint", {"targets": targets})


def test(path: str = ".") -> Dict[str, Any]:
    return _hub.call("test", {"path": path})


def build(path: str = ".") -> Dict[str, Any]:
    return _hub.call("build", {"path": path})


def docs(path: str = ".") -> Dict[str, Any]:
    return _hub.call("docs", {"path": path})


def pr(title: str, body: str = "") -> Dict[str, Any]:
    return _hub.call("pr", {"title": title, "body": body})


def deploy(env: str) -> Dict[str, Any]:
    return _hub.call("deploy", {"env": env})


def eval(suite: str) -> Dict[str, Any]:
    return _hub.call("eval", {"suite": suite})


__all__ = ["repo", "lint", "test", "build", "docs", "pr", "deploy", "eval"]
