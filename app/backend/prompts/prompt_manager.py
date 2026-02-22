import os
import threading
from abc import ABC, abstractmethod
from typing import Any

import yaml
from jinja2 import Environment, StrictUndefined
from langchain_core.prompts import ChatPromptTemplate


class PromptManager(ABC):

    @abstractmethod
    def load_prompt(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def load_tools(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class JinjaPromptManager(PromptManager):
    JINJA_PROMPTS_DIR: str = os.path.dirname(os.path.abspath(__file__))
    _prompts_cache: dict[str, ChatPromptTemplate] = {}
    _lock = threading.Lock()

    _env = Environment(
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def load_prompt(self, path: str) -> ChatPromptTemplate:
        """
        Loads a Jinja prompt template from a YAML file in a thread-safe manner, caching compiled templates for reuse.

        Args:
            path (str): The path to the YAML file.

        Returns:
            ChatPromptTemplate: The prompt template.
        """
        if path in self._prompts_cache:
            return self._prompts_cache[
                path
            ]  # Return cached template if available to improve performance

        with (
            self._lock
        ):  # Due to ChatPromptTemplate limitation, we cannot compile concurrently.
            if (
                path in self._prompts_cache
            ):  # Double-check inside lock in case another thread already compiled it
                return self._prompts_cache[path]
            with open(os.path.join(self.JINJA_PROMPTS_DIR, path), "r") as f:
                prompt_template_obj = yaml.safe_load(f)
                prompt_template = ChatPromptTemplate.from_template(
                    template=prompt_template_obj["template"],
                    template_format="jinja2",
                    optional_variables=[
                        var["name"]
                        for var in prompt_template_obj["input_variables"]
                        if not var["is_required"]
                    ],
                )
                self._prompts_cache[path] = prompt_template
                return prompt_template

    def load_tools(self, *args, **kwargs) -> Any:
        pass

    def validate_inputs(self, input_args: set, mandatory_args: set):
        missing = mandatory_args - input_args
        if missing:
            raise ValueError(f"Missing mandatory prompt variables: {missing}")
