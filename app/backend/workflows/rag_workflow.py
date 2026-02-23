import logging
from typing import Any, List

from langgraph.graph import END, START, StateGraph
from schemas.chat import ChatResponse
from schemas.state import State
from workflows.components.response_synthesiser import ResponseSynthesiserComponent
from workflows.components.source_retrieval import SourceRetrievalComponent

logger = logging.getLogger(__name__)


class RAGWorkflow:
    """
    The RAG workflow uses a stateful directed graph, which allows for easier customisability.
    """

    def __init__(
        self,
        *args: Any,
        # Insert any components here
        source_retrieval: SourceRetrievalComponent,
        response_synthesiser: ResponseSynthesiserComponent,
        **kwargs: Any,
    ):
        self.source_retrieval = source_retrieval
        self.response_synthesiser = response_synthesiser

    def build_graph(self):
        # Instantiate graph here
        graph_builder = StateGraph(State)

        # Include nodes
        graph_builder.add_node("retrieve_sources", self.source_retrieval.retrieve)
        graph_builder.add_node(
            "synthesise_response", self.response_synthesiser.synthesize
        )

        # Include Edges
        graph_builder.add_edge(START, "retrieve_sources")
        graph_builder.add_edge("retrieve_sources", "synthesise_response")
        graph_builder.add_edge("synthesise_response", END)

        # Compile and save graph
        self.graph = graph_builder.compile()

    async def run_pipeline(
        self, state: dict, conversation_history: List[ChatResponse]
    ) -> ChatResponse:
        # Update state with conversation history and invoke graph
        state["conversation_history"] = [
            history.model_dump() for history in conversation_history
        ]
        new_state = await self.graph.ainvoke(state)

        # Create response object and insert
        response = ChatResponse.model_validate(new_state)
        try:
            await response.insert()
        except Exception as exc:
            logger.exception(f"Failed to save chat response to database: {exc}")

        logger.info(response)
        return response
