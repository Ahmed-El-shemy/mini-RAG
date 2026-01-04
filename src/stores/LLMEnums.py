from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):
    SYSTM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereEnums(Enum):
    SYSTM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "COHERE"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"