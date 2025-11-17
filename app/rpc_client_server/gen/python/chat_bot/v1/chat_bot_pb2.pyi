from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetModelResponseRequest(_message.Message):
    __slots__ = ("assistant_name", "prompt")
    ASSISTANT_NAME_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    assistant_name: str
    prompt: str
    def __init__(self, assistant_name: _Optional[str] = ..., prompt: _Optional[str] = ...) -> None: ...

class GetModelResponseResponse(_message.Message):
    __slots__ = ("response", "is_json")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    IS_JSON_FIELD_NUMBER: _ClassVar[int]
    response: str
    is_json: bool
    def __init__(self, response: _Optional[str] = ..., is_json: bool = ...) -> None: ...

class GetModelImageResponseRequest(_message.Message):
    __slots__ = ("urls", "assistant_name")
    URLS_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_NAME_FIELD_NUMBER: _ClassVar[int]
    urls: _containers.RepeatedScalarFieldContainer[str]
    assistant_name: str
    def __init__(self, urls: _Optional[_Iterable[str]] = ..., assistant_name: _Optional[str] = ...) -> None: ...

class GetModelImageResponseResponse(_message.Message):
    __slots__ = ("response", "is_json")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    IS_JSON_FIELD_NUMBER: _ClassVar[int]
    response: str
    is_json: bool
    def __init__(self, response: _Optional[str] = ..., is_json: bool = ...) -> None: ...
