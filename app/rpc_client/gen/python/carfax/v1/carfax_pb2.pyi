from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IsVinExistsRequest(_message.Message):
    __slots__ = ("vin",)
    VIN_FIELD_NUMBER: _ClassVar[int]
    vin: str
    def __init__(self, vin: _Optional[str] = ...) -> None: ...

class IsVinExistsResponse(_message.Message):
    __slots__ = ("is_exists",)
    IS_EXISTS_FIELD_NUMBER: _ClassVar[int]
    is_exists: bool
    def __init__(self, is_exists: bool = ...) -> None: ...

class BuyCarfaxRequest(_message.Message):
    __slots__ = ("source", "vin", "user_external_id", "success_url", "cancel_url")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    VIN_FIELD_NUMBER: _ClassVar[int]
    USER_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_URL_FIELD_NUMBER: _ClassVar[int]
    CANCEL_URL_FIELD_NUMBER: _ClassVar[int]
    source: str
    vin: str
    user_external_id: str
    success_url: str
    cancel_url: str
    def __init__(self, source: _Optional[str] = ..., vin: _Optional[str] = ..., user_external_id: _Optional[str] = ..., success_url: _Optional[str] = ..., cancel_url: _Optional[str] = ...) -> None: ...

class BuyCarfaxResponse(_message.Message):
    __slots__ = ("carfax", "link")
    CARFAX_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    carfax: Carfax
    link: str
    def __init__(self, carfax: _Optional[_Union[Carfax, _Mapping]] = ..., link: _Optional[str] = ...) -> None: ...

class GetAllCarfaxesForUserRequest(_message.Message):
    __slots__ = ("user_external_id", "source")
    USER_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    user_external_id: str
    source: str
    def __init__(self, user_external_id: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...

class GetAllCarfaxesForUserResponse(_message.Message):
    __slots__ = ("carfaxes",)
    CARFAXES_FIELD_NUMBER: _ClassVar[int]
    carfaxes: _containers.RepeatedCompositeFieldContainer[Carfax]
    def __init__(self, carfaxes: _Optional[_Iterable[_Union[Carfax, _Mapping]]] = ...) -> None: ...

class GetCarfaxByVinRequest(_message.Message):
    __slots__ = ("vin", "source", "user_external_id")
    VIN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    USER_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    vin: str
    source: str
    user_external_id: str
    def __init__(self, vin: _Optional[str] = ..., source: _Optional[str] = ..., user_external_id: _Optional[str] = ...) -> None: ...

class GetCarfaxByVinResponse(_message.Message):
    __slots__ = ("carfax",)
    CARFAX_FIELD_NUMBER: _ClassVar[int]
    carfax: Carfax
    def __init__(self, carfax: _Optional[_Union[Carfax, _Mapping]] = ...) -> None: ...

class Carfax(_message.Message):
    __slots__ = ("user_external_id", "source", "link", "is_paid", "vin", "created_at", "id")
    USER_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    IS_PAID_FIELD_NUMBER: _ClassVar[int]
    VIN_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    user_external_id: str
    source: str
    link: str
    is_paid: bool
    vin: str
    created_at: str
    id: str
    def __init__(self, user_external_id: _Optional[str] = ..., source: _Optional[str] = ..., link: _Optional[str] = ..., is_paid: bool = ..., vin: _Optional[str] = ..., created_at: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...
