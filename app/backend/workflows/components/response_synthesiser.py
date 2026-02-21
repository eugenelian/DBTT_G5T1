import logging

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from langchain.messages import AIMessage

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

    async def synthesize(self, state: State):
        """
        Synthesizes a response based on the user query, conversation history and content from retrieved sources.

        Args:
            state: State that contains information about "user_query"
        
        Returns:
            state: Updated state containing the "content" and "usage"
        """
        try:
            # TODO: Craft prompt including user query, conversation history and content from retrieved sources.
            response: AIMessage = await self.llm_client.ainvoke(state.user_query)
            return {"content": response.content, "usage": response.response_metadata}

        except Exception as exc:
            logger.warning("Exception occurred: %s", exc)
            return {"content": exc, "usage": {}}
