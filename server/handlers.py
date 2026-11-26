"""The Python behind flow.yaml.

The graph, the prompts and the transitions live in flow.yaml. Only tools that
need code live here.
"""

import asyncio

from pipecat.flows import TRANSITION_IN_YAML, FlowManager, flows_tool_options

# How long the pretend booking system takes to answer.
BOOKING_LOOKUP_SECS = 20


async def record_card_answer(flow_manager: FlowManager, has_card: bool):
    """Record whether the caller brought a physical payment card with them.

    Args:
        has_card: True if the caller has a physical card with them, False if they do not.
    """
    flow_manager.state["has_card"] = has_card
    return {"has_card": has_card}, TRANSITION_IN_YAML


# cancel_on_interruption=False makes this an asynchronous function call: the
# call keeps running while the conversation carries on. That is the "background
# work" WaitReassuranceLLMExtension (see bot.py) speaks up about.
@flows_tool_options(cancel_on_interruption=False)
async def check_booking_hold(flow_manager: FlowManager):
    """Check whether the caller's booking is still being held, and until when.

    Call this when the caller asks if their booking or car is still held or reserved.
    The lookup takes a little while.
    """
    # Stands in for a slow booking system. The answer is made up.
    await asyncio.sleep(BOOKING_LOOKUP_SECS)
    return {"booking_held": True, "held_until": "6 pm today"}, TRANSITION_IN_YAML
