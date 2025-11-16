from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetCheckoutLinkRequest(_message.Message):
    __slots__ = ("purpose", "purpose_external_id", "success_link", "cancel_link", "user_external_id", "source")
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_LINK_FIELD_NUMBER: _ClassVar[int]
    CANCEL_LINK_FIELD_NUMBER: _ClassVar[int]
    USER_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    purpose: str
    purpose_external_id: str
    success_link: str
    cancel_link: str
    user_external_id: str
    source: str
    def __init__(self, purpose: _Optional[str] = ..., purpose_external_id: _Optional[str] = ..., success_link: _Optional[str] = ..., cancel_link: _Optional[str] = ..., user_external_id: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...

class GetCheckoutLinkResponse(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: str
    def __init__(self, link: _Optional[str] = ...) -> None: ...
