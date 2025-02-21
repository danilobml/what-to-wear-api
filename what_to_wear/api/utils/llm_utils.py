from abc import ABC, abstractmethod

from what_to_wear.api.models.schemas.mistral_llm_response import MistralLlmResponse
from what_to_wear.api.utils.constants import ModelTypeEnum, NoModelSelectedException, MODEL_PARAMS


class LLMResponseParser(ABC):
    """ Abstract class to obtain a parser for the content of different LLM responses """

    @abstractmethod
    def get_content(self, llm_response: dict) -> str:
        pass


class MistralResponseParser(LLMResponseParser):
    """ Parser implementation for Mistral LLM """
    def get_content(self, llm_response: MistralLlmResponse) -> str:
        return llm_response["choices"][0]["message"]["content"]


class LLMResponseParserFactory:
    """ To obtain specific parser implementation """
    # NOTE - add new parsers when a new model is added:
    _parsers = {
        ModelTypeEnum.MISTRAL: MistralResponseParser
    }

    @classmethod
    def get_parser(cls, model_type: ModelTypeEnum) -> LLMResponseParser:
        if model_type in cls._parsers:
            return cls._parsers[model_type]
        raise NoModelSelectedException(f"No parser available for model: {model_type}")


def get_content_from_llm_response(llm_response, model_type: ModelTypeEnum) -> str:
    """ Gets the relevant (content) part of LLM responses: """
    parser = LLMResponseParserFactory.get_parser(model_type)
    return parser.get_content(llm_response)


def get_model_params(model_type: ModelTypeEnum) -> str:
    """ Returns parameters for selected LLM, to be used in API calls """
    return MODEL_PARAMS.get(model_type)
