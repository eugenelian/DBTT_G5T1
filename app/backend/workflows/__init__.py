from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

# Expose public names without importing submodules at import time.
__all__ = [
    "RAGWorkflow",
]

if TYPE_CHECKING:  # For type checkers only; no runtime side effects
    from .rag_workflow import RAGWorkflow


def __getattr__(name: str):
    if name == "RAGWorkflow":
        return importlib.import_module(".rag_workflow", __name__).RAGWorkflow
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
