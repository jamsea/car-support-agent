"""The Python behind flow.yaml.

The graph, the prompts and the transitions live in flow.yaml. Only tools that
need code live here.
"""

from pipecat.flows import TRANSITION_IN_YAML, FlowManager


async def record_card_answer(flow_manager: FlowManager, has_card: bool):
    """Record whether the caller brought a physical payment card with them.

    Args:
        has_card: True if the caller has a physical card with them, False if they do not.
    """
    flow_manager.state["has_card"] = has_card
    return {"has_card": has_card}, TRANSITION_IN_YAML
