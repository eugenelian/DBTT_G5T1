import logging

from langchain.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from prompts.prompt_manager import JinjaPromptManager
from schemas.state import State

logger = logging.getLogger(__name__)


class ResponseSynthesiserComponent:
    """
    The response synthesizer component synthesizes a response based on user query, conversation history and content from retrieved sources.
    """

    SYNTHESIZE_RESPONSE_PROMPT = "response_synthesis.yaml"

    def __init__(
        self,
        llm_client: ChatOpenAI | ChatGroq,
        prompt_manager: JinjaPromptManager,
        prompt_filename: str | None = None,
    ):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager

        # Shadow the class defaults on the instance (copy to avoid shared mutation)
        self.prompt_filename = prompt_filename or type(self).SYNTHESIZE_RESPONSE_PROMPT

        # Extract out template and mandatory args
        template, mandatory_args = self.prompt_manager.load_prompt(self.prompt_filename)
        self.prompt_template: ChatPromptTemplate = template
        self.mandatory_args: list[str] = mandatory_args

    async def synthesize(self, state: State):
        """
        Synthesizes a response based on the user query, conversation history and content from retrieved sources.

        Args:
            state: State that contains information about "user_query"

        Returns:
            state: Updated state containing the "content" and "usage"
        """
        try:
            # Craft prompt including user query, content from retrieved sources and conversation history.
            # TODO: Add logic for conversation history
            args: dict = {
                "user_query": state.user_query,
                "sources": (
                    "\n".join(
                        [
                            f"**Source {i+1}:** {source["page_content"].replace("\n", "\\n")}"
                            for i, source in enumerate(state.sources)
                        ]
                    )
                    if len(state.sources) != 0
                    else None
                ),
                "conversation history": None,
            }
            filtered_args = {k: v for k, v in args.items() if v is not None}
            self.prompt_manager.validate_inputs(
                filtered_args.keys(), self.mandatory_args
            )
            prompt = self.prompt_template.format_messages(**filtered_args)
            response: AIMessage = await self.llm_client.ainvoke(prompt)
            return {
                "content": response.content,
                "response_metadata": response.response_metadata,
            }

        except Exception as exc:
            logger.exception("Exception occurred: %s", exc)
            return {"content": exc, "response_metadata": {}}
