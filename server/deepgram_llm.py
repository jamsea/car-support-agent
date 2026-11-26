"""Deepgram-hosted LLMs (phoneLLM mini, Think-Fast) as a Pipecat LLM service.

Deepgram's /v1/think endpoint follows the OpenAI Chat Completions format, so
this is the OpenAI service with three small changes:

- requests go to https://agent.deepgram.com/v1/think
- the Deepgram API key is sent with the "Token" scheme
- only the fields the endpoint accepts are sent; it rejects all others

Docs: https://developers.deepgram.com/docs/llm/request-response-format
"""

from openai import AsyncOpenAI, DefaultAsyncHttpxClient
from openai import NotGiven as OpenAINotGiven
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.utils.types import NotGiven

THINK_PATH = "/v1/think"

# The only top-level fields /v1/think accepts.
ALLOWED_FIELDS = {
    "model",
    "messages",
    "temperature",
    "reasoning_effort",
    "tools",
    "stream",
    "stream_options",
    "mip_opt_out",
}


async def _send_to_think(request):
    # The OpenAI client always posts to .../chat/completions.
    request.url = request.url.copy_with(path=THINK_PATH)


class DeepgramLLMService(OpenAILLMService):
    """LLM service for Deepgram-hosted models, using a Deepgram API key."""

    def __init__(
        self, *, api_key: str, settings: OpenAILLMService.Settings | None = None, **kwargs
    ):
        # Pipecat recommends temperature 0 for phoneLLM mini.
        default_settings = self.Settings(model="phonellm-mini-alpha-2-fp8", temperature=0.0)
        if settings is not None:
            default_settings.apply_update(settings)
        super().__init__(api_key=api_key, settings=default_settings, **kwargs)

    def create_client(self, api_key=None, **kwargs):
        return AsyncOpenAI(
            api_key=api_key,
            base_url="https://agent.deepgram.com/v1",
            default_headers={"Authorization": f"Token {api_key}"},
            http_client=DefaultAsyncHttpxClient(event_hooks={"request": [_send_to_think]}),
        )

    def build_chat_completion_params(self, params_from_context) -> dict:
        params = super().build_chat_completion_params(params_from_context)
        return {
            key: value
            for key, value in params.items()
            if key in ALLOWED_FIELDS
            and value is not None
            and not isinstance(value, (NotGiven, OpenAINotGiven))
        }
