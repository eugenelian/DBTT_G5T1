import logging
from typing import Any

from langgraph.graph import StateGraph, START, END

from workflows.components.response_synthesiser import ResponseSynthesiserComponent
from schemas.state import State

logger = logging.getLogger(__name__)


class RAGWorkflow():
    """
    The RAG workflow uses a stateful directed graph, which allows for easier customisability.
    """

    def __init__(
        self,
        *args: Any,
        # TODO: Insert any components here
        response_synthesiser: ResponseSynthesiserComponent,
        **kwargs: Any,
    ):
        self.response_synthesiser = response_synthesiser


    def build_graph(self):
        # Instantiate graph here
        graph_builder = StateGraph(State)

        # Include nodes
        graph_builder.add_node("synthesise_response", self.response_synthesiser.synthesize)

        # Include Edges
        graph_builder.add_edge(START, "synthesise_response")
        graph_builder.add_edge("synthesise_response", END)

        # Compile and save graph
        self.graph = graph_builder.compile()


    async def run_pipeline(self, state: State):
        response = await self.graph.ainvoke(state)
        logger.info(response)
        return response
