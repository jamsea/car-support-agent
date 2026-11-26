"""Cloud services for the eval harness, named by `factory:` in the scenario files.

Everything here is hosted, so no local models are needed:

- judge: OpenAI decides each `eval:` check
- caller_voice: Deepgram Aura-2 speaks the caller's lines (Australian voice)
- transcriber: Deepgram Nova-3 (en-AU) writes down what the bot said
"""

import os

import aiohttp
from pipecat.services.deepgram.stt import DeepgramSegmentedSTTService
from pipecat.services.deepgram.tts import DeepgramHttpTTSService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transcriptions.language import Language


def judge(config):
    return OpenAILLMService(
        api_key=os.environ["OPENAI_API_KEY"],
        settings=OpenAILLMService.Settings(model=config.get("model", "gpt-4.1")),
    )


def caller_voice(config):
    return DeepgramHttpTTSService(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        aiohttp_session=aiohttp.ClientSession(),
        settings=DeepgramHttpTTSService.Settings(voice=config["voice"]),
    )


def transcriber(config):
    return DeepgramSegmentedSTTService(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        aiohttp_session=aiohttp.ClientSession(),
        settings=DeepgramSegmentedSTTService.Settings(
            model=config.get("model", "nova-3-general"),
            language=Language.EN_AU,
        ),
    )
