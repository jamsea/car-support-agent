"""Front desk flow for the car rental support agent.

Four nodes:

    greeting -> card_check -> card_policy
         \\          |            /
          +----- transfer ------+   (transfer_to_human works from every node)
"""

from pipecat.flows import FlowManager, NodeConfig

TRANSFER_LINE = "One moment, I'll transfer you now."

ROLE_MESSAGE = (
    "You are a phone support agent for an Australian car rental company. The caller is "
    "standing at the front desk of one of our stores. Speak Australian English and use "
    "Australian spelling. Your replies are spoken aloud, so keep them to one or two short "
    "sentences, with no emojis, lists or special characters. Stay calm and polite, even if "
    "the caller is upset. If the caller ever asks for a person, a human, a manager or a "
    "transfer, call transfer_to_human straight away and say nothing yourself."
)


async def transfer_to_human(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """Transfer the caller to a human.

    Call this whenever the caller asks to speak to a person, a human, a manager, or asks
    to be transferred. Do not say anything yourself, just call this function.
    """
    return None, create_transfer_node()


async def report_rental_refused(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """Record that the caller is at the front desk and is not being given their rental car."""
    return None, create_card_check_node()


async def record_card_answer(flow_manager: FlowManager, has_card: bool) -> tuple[dict, NodeConfig]:
    """Record whether the caller brought a physical payment card with them.

    Args:
        has_card: True if the caller has a physical card with them, False if they do not.
    """
    flow_manager.state["has_card"] = has_card
    return {"has_card": has_card}, create_card_policy_node(has_card)


def create_greeting_node() -> NodeConfig:
    """Greet the caller and find out what is wrong."""
    return NodeConfig(
        name="greeting",
        role_message=ROLE_MESSAGE,
        task_messages=[
            {
                "role": "developer",
                "content": (
                    "Greet the caller briefly and ask how you can help. When they say they "
                    "are not being given their rental car, call report_rental_refused."
                ),
            }
        ],
        functions=[report_rental_refused],
    )


def create_card_check_node() -> NodeConfig:
    """Ask whether the caller brought a physical card."""
    return NodeConfig(
        name="card_check",
        task_messages=[
            {
                "role": "developer",
                "content": (
                    "Ask the caller if they brought a physical card with them today. Ask "
                    "only that. When they answer, call record_card_answer."
                ),
            }
        ],
        functions=[record_card_answer],
    )


def create_card_policy_node(has_card: bool) -> NodeConfig:
    """Explain the physical card rule."""
    if has_card:
        task = (
            "The caller has a physical card with them. Tell them to show the physical card "
            "to the staff at the front desk so they can get their car."
        )
    else:
        task = (
            "The caller did not bring a physical card. Explain that they need to provide a "
            "physical card to get a rental car, so the desk cannot hand over the car without "
            "one. Answer any follow-up questions about this briefly."
        )
    return NodeConfig(
        name="card_policy",
        task_messages=[{"role": "developer", "content": task}],
        functions=[],
    )


def create_transfer_node() -> NodeConfig:
    """Say the fixed transfer line, then end the call."""
    return NodeConfig(
        name="transfer",
        task_messages=[
            {"role": "developer", "content": "The caller is being transferred. Say nothing."}
        ],
        functions=[],
        respond_immediately=False,
        pre_actions=[{"type": "end_conversation", "text": TRANSFER_LINE}],
    )
