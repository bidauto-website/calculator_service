from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetCalculatorWithDataRequest(_message.Message):
    __slots__ = ("price", "auction", "fee_type", "vehicle_type", "destination", "location")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    AUCTION_FIELD_NUMBER: _ClassVar[int]
    FEE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    price: int
    auction: str
    fee_type: str
    vehicle_type: str
    destination: str
    location: str
    def __init__(self, price: _Optional[int] = ..., auction: _Optional[str] = ..., fee_type: _Optional[str] = ..., vehicle_type: _Optional[str] = ..., destination: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class GetCalculatorBatchRequest(_message.Message):
    __slots__ = ("data", "lot_id")
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    data: GetCalculatorWithDataRequest
    lot_id: str
    def __init__(self, data: _Optional[_Union[GetCalculatorWithDataRequest, _Mapping]] = ..., lot_id: _Optional[str] = ...) -> None: ...

class GetCalculatorWithDataBatchRequest(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[GetCalculatorBatchRequest]
    def __init__(self, data: _Optional[_Iterable[_Union[GetCalculatorBatchRequest, _Mapping]]] = ...) -> None: ...

class GetCalculatorWithoutDataRequest(_message.Message):
    __slots__ = ("price", "auction", "lot_id")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    AUCTION_FIELD_NUMBER: _ClassVar[int]
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    price: int
    auction: str
    lot_id: str
    def __init__(self, price: _Optional[int] = ..., auction: _Optional[str] = ..., lot_id: _Optional[str] = ...) -> None: ...

class GetCalculatorWithDataResponse(_message.Message):
    __slots__ = ("data", "message", "success")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: CalculatorOut
    message: str
    success: bool
    def __init__(self, data: _Optional[_Union[CalculatorOut, _Mapping]] = ..., message: _Optional[str] = ..., success: bool = ...) -> None: ...

class GetCalculatorWithoutDataResponse(_message.Message):
    __slots__ = ("data", "message", "success")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: CalculatorOut
    message: str
    success: bool
    def __init__(self, data: _Optional[_Union[CalculatorOut, _Mapping]] = ..., message: _Optional[str] = ..., success: bool = ...) -> None: ...

class CalculatorBatchItem(_message.Message):
    __slots__ = ("calculator", "lot_id")
    CALCULATOR_FIELD_NUMBER: _ClassVar[int]
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    calculator: CalculatorOut
    lot_id: str
    def __init__(self, calculator: _Optional[_Union[CalculatorOut, _Mapping]] = ..., lot_id: _Optional[str] = ...) -> None: ...

class GetCalculatorWithDataBatchResponse(_message.Message):
    __slots__ = ("data", "message", "success")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[CalculatorBatchItem]
    message: str
    success: bool
    def __init__(self, data: _Optional[_Iterable[_Union[CalculatorBatchItem, _Mapping]]] = ..., message: _Optional[str] = ..., success: bool = ...) -> None: ...

class City(_message.Message):
    __slots__ = ("name", "price")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    name: str
    price: int
    def __init__(self, name: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class VATs(_message.Message):
    __slots__ = ("vats", "eu_vats")
    VATS_FIELD_NUMBER: _ClassVar[int]
    EU_VATS_FIELD_NUMBER: _ClassVar[int]
    vats: _containers.RepeatedCompositeFieldContainer[City]
    eu_vats: _containers.RepeatedCompositeFieldContainer[City]
    def __init__(self, vats: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., eu_vats: _Optional[_Iterable[_Union[City, _Mapping]]] = ...) -> None: ...

class SpecialFee(_message.Message):
    __slots__ = ("price", "name")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    price: int
    name: str
    def __init__(self, price: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class AdditionalFeesOut(_message.Message):
    __slots__ = ("summ", "fees", "auction_fee", "internet_fee", "live_fee")
    SUMM_FIELD_NUMBER: _ClassVar[int]
    FEES_FIELD_NUMBER: _ClassVar[int]
    AUCTION_FEE_FIELD_NUMBER: _ClassVar[int]
    INTERNET_FEE_FIELD_NUMBER: _ClassVar[int]
    LIVE_FEE_FIELD_NUMBER: _ClassVar[int]
    summ: int
    fees: _containers.RepeatedCompositeFieldContainer[SpecialFee]
    auction_fee: int
    internet_fee: int
    live_fee: int
    def __init__(self, summ: _Optional[int] = ..., fees: _Optional[_Iterable[_Union[SpecialFee, _Mapping]]] = ..., auction_fee: _Optional[int] = ..., internet_fee: _Optional[int] = ..., live_fee: _Optional[int] = ...) -> None: ...

class BaseCalculator(_message.Message):
    __slots__ = ("broker_fee", "transportation_price", "ocean_ship", "additional", "totals")
    BROKER_FEE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTATION_PRICE_FIELD_NUMBER: _ClassVar[int]
    OCEAN_SHIP_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FIELD_NUMBER: _ClassVar[int]
    TOTALS_FIELD_NUMBER: _ClassVar[int]
    broker_fee: int
    transportation_price: _containers.RepeatedCompositeFieldContainer[City]
    ocean_ship: _containers.RepeatedCompositeFieldContainer[City]
    additional: AdditionalFeesOut
    totals: _containers.RepeatedCompositeFieldContainer[City]
    def __init__(self, broker_fee: _Optional[int] = ..., transportation_price: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., ocean_ship: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., additional: _Optional[_Union[AdditionalFeesOut, _Mapping]] = ..., totals: _Optional[_Iterable[_Union[City, _Mapping]]] = ...) -> None: ...

class DefaultCalculator(_message.Message):
    __slots__ = ("broker_fee", "transportation_price", "ocean_ship", "additional", "totals", "auction_fee", "live_fee", "internet_fee")
    BROKER_FEE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTATION_PRICE_FIELD_NUMBER: _ClassVar[int]
    OCEAN_SHIP_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FIELD_NUMBER: _ClassVar[int]
    TOTALS_FIELD_NUMBER: _ClassVar[int]
    AUCTION_FEE_FIELD_NUMBER: _ClassVar[int]
    LIVE_FEE_FIELD_NUMBER: _ClassVar[int]
    INTERNET_FEE_FIELD_NUMBER: _ClassVar[int]
    broker_fee: int
    transportation_price: _containers.RepeatedCompositeFieldContainer[City]
    ocean_ship: _containers.RepeatedCompositeFieldContainer[City]
    additional: AdditionalFeesOut
    totals: _containers.RepeatedCompositeFieldContainer[City]
    auction_fee: int
    live_fee: int
    internet_fee: int
    def __init__(self, broker_fee: _Optional[int] = ..., transportation_price: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., ocean_ship: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., additional: _Optional[_Union[AdditionalFeesOut, _Mapping]] = ..., totals: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., auction_fee: _Optional[int] = ..., live_fee: _Optional[int] = ..., internet_fee: _Optional[int] = ...) -> None: ...

class EUCalculator(_message.Message):
    __slots__ = ("broker_fee", "transportation_price", "ocean_ship", "additional", "totals", "vats", "custom_agency")
    BROKER_FEE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTATION_PRICE_FIELD_NUMBER: _ClassVar[int]
    OCEAN_SHIP_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FIELD_NUMBER: _ClassVar[int]
    TOTALS_FIELD_NUMBER: _ClassVar[int]
    VATS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_AGENCY_FIELD_NUMBER: _ClassVar[int]
    broker_fee: int
    transportation_price: _containers.RepeatedCompositeFieldContainer[City]
    ocean_ship: _containers.RepeatedCompositeFieldContainer[City]
    additional: AdditionalFeesOut
    totals: _containers.RepeatedCompositeFieldContainer[City]
    vats: VATs
    custom_agency: int
    def __init__(self, broker_fee: _Optional[int] = ..., transportation_price: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., ocean_ship: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., additional: _Optional[_Union[AdditionalFeesOut, _Mapping]] = ..., totals: _Optional[_Iterable[_Union[City, _Mapping]]] = ..., vats: _Optional[_Union[VATs, _Mapping]] = ..., custom_agency: _Optional[int] = ...) -> None: ...

class CalculatorOut(_message.Message):
    __slots__ = ("calculator", "eu_calculator")
    CALCULATOR_FIELD_NUMBER: _ClassVar[int]
    EU_CALCULATOR_FIELD_NUMBER: _ClassVar[int]
    calculator: DefaultCalculator
    eu_calculator: EUCalculator
    def __init__(self, calculator: _Optional[_Union[DefaultCalculator, _Mapping]] = ..., eu_calculator: _Optional[_Union[EUCalculator, _Mapping]] = ...) -> None: ...
