from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLotRequest(_message.Message):
    __slots__ = ("lot_id", "site")
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    lot_id: int
    site: str
    def __init__(self, lot_id: _Optional[int] = ..., site: _Optional[str] = ...) -> None: ...

class GetLotResponse(_message.Message):
    __slots__ = ("lot",)
    LOT_FIELD_NUMBER: _ClassVar[int]
    lot: _containers.RepeatedCompositeFieldContainer[Lot]
    def __init__(self, lot: _Optional[_Iterable[_Union[Lot, _Mapping]]] = ...) -> None: ...

class GetSaleHistoryRequest(_message.Message):
    __slots__ = ("lot_id", "site")
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    lot_id: int
    site: str
    def __init__(self, lot_id: _Optional[int] = ..., site: _Optional[str] = ...) -> None: ...

class GetSaleHistoryResponse(_message.Message):
    __slots__ = ("lot",)
    LOT_FIELD_NUMBER: _ClassVar[int]
    lot: _containers.RepeatedCompositeFieldContainer[Lot]
    def __init__(self, lot: _Optional[_Iterable[_Union[Lot, _Mapping]]] = ...) -> None: ...

class GetLotByVinOrLotRequest(_message.Message):
    __slots__ = ("vin_or_lot_id", "site")
    VIN_OR_LOT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    vin_or_lot_id: str
    site: str
    def __init__(self, vin_or_lot_id: _Optional[str] = ..., site: _Optional[str] = ...) -> None: ...

class GetLotByVinOrLotResponse(_message.Message):
    __slots__ = ("lot",)
    LOT_FIELD_NUMBER: _ClassVar[int]
    lot: _containers.RepeatedCompositeFieldContainer[Lot]
    def __init__(self, lot: _Optional[_Iterable[_Union[Lot, _Mapping]]] = ...) -> None: ...

class GetCurrentBidRequest(_message.Message):
    __slots__ = ("lot_id", "site")
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    lot_id: int
    site: str
    def __init__(self, lot_id: _Optional[int] = ..., site: _Optional[str] = ...) -> None: ...

class GetCurrentBidResponse(_message.Message):
    __slots__ = ("current_bid",)
    CURRENT_BID_FIELD_NUMBER: _ClassVar[int]
    current_bid: CurrentBid
    def __init__(self, current_bid: _Optional[_Union[CurrentBid, _Mapping]] = ...) -> None: ...

class CurrentBid(_message.Message):
    __slots__ = ("pre_bid",)
    PRE_BID_FIELD_NUMBER: _ClassVar[int]
    pre_bid: int
    def __init__(self, pre_bid: _Optional[int] = ...) -> None: ...

class Lot(_message.Message):
    __slots__ = ("lot_id", "site", "base_site", "salvage_id", "odometer", "price_new", "price_future", "price_reserve", "current_bid", "auction_date", "cost_priced", "cost_repair", "year", "cylinders", "state", "vehicle_type", "auction_type", "make", "model", "series", "damage_pr", "damage_sec", "keys", "odobrand", "fuel", "drive", "transmission", "color", "status", "title", "vin", "engine", "engine_size", "location", "location_old", "location_id", "country", "document", "document_old", "currency", "seller", "is_buynow", "iaai_360", "copart_exterior_360", "copart_interior_360", "video", "link_img_hd", "link_img_small", "is_offsite", "location_offsite", "link", "body_type", "seller_type", "vehicle_score", "form_get_type", "sale_history", "sale_date", "sale_status", "purchase_price")
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    BASE_SITE_FIELD_NUMBER: _ClassVar[int]
    SALVAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ODOMETER_FIELD_NUMBER: _ClassVar[int]
    PRICE_NEW_FIELD_NUMBER: _ClassVar[int]
    PRICE_FUTURE_FIELD_NUMBER: _ClassVar[int]
    PRICE_RESERVE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BID_FIELD_NUMBER: _ClassVar[int]
    AUCTION_DATE_FIELD_NUMBER: _ClassVar[int]
    COST_PRICED_FIELD_NUMBER: _ClassVar[int]
    COST_REPAIR_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    CYLINDERS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAKE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_PR_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_SEC_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    ODOBRAND_FIELD_NUMBER: _ClassVar[int]
    FUEL_FIELD_NUMBER: _ClassVar[int]
    DRIVE_FIELD_NUMBER: _ClassVar[int]
    TRANSMISSION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    VIN_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_SIZE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_OLD_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_OLD_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    IS_BUYNOW_FIELD_NUMBER: _ClassVar[int]
    IAAI_360_FIELD_NUMBER: _ClassVar[int]
    COPART_EXTERIOR_360_FIELD_NUMBER: _ClassVar[int]
    COPART_INTERIOR_360_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    LINK_IMG_HD_FIELD_NUMBER: _ClassVar[int]
    LINK_IMG_SMALL_FIELD_NUMBER: _ClassVar[int]
    IS_OFFSITE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_OFFSITE_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    BODY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SELLER_TYPE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_SCORE_FIELD_NUMBER: _ClassVar[int]
    FORM_GET_TYPE_FIELD_NUMBER: _ClassVar[int]
    SALE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    SALE_DATE_FIELD_NUMBER: _ClassVar[int]
    SALE_STATUS_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_PRICE_FIELD_NUMBER: _ClassVar[int]
    lot_id: int
    site: int
    base_site: str
    salvage_id: int
    odometer: int
    price_new: int
    price_future: int
    price_reserve: int
    current_bid: int
    auction_date: str
    cost_priced: int
    cost_repair: int
    year: int
    cylinders: int
    state: str
    vehicle_type: str
    auction_type: str
    make: str
    model: str
    series: str
    damage_pr: str
    damage_sec: str
    keys: str
    odobrand: str
    fuel: str
    drive: str
    transmission: str
    color: str
    status: str
    title: str
    vin: str
    engine: str
    engine_size: float
    location: str
    location_old: str
    location_id: int
    country: str
    document: str
    document_old: str
    currency: str
    seller: str
    is_buynow: bool
    iaai_360: str
    copart_exterior_360: _containers.RepeatedScalarFieldContainer[str]
    copart_interior_360: str
    video: str
    link_img_hd: _containers.RepeatedScalarFieldContainer[str]
    link_img_small: _containers.RepeatedScalarFieldContainer[str]
    is_offsite: bool
    location_offsite: str
    link: str
    body_type: str
    seller_type: str
    vehicle_score: str
    form_get_type: str
    sale_history: _containers.RepeatedCompositeFieldContainer[SaleHistory]
    sale_date: str
    sale_status: str
    purchase_price: int
    def __init__(self, lot_id: _Optional[int] = ..., site: _Optional[int] = ..., base_site: _Optional[str] = ..., salvage_id: _Optional[int] = ..., odometer: _Optional[int] = ..., price_new: _Optional[int] = ..., price_future: _Optional[int] = ..., price_reserve: _Optional[int] = ..., current_bid: _Optional[int] = ..., auction_date: _Optional[str] = ..., cost_priced: _Optional[int] = ..., cost_repair: _Optional[int] = ..., year: _Optional[int] = ..., cylinders: _Optional[int] = ..., state: _Optional[str] = ..., vehicle_type: _Optional[str] = ..., auction_type: _Optional[str] = ..., make: _Optional[str] = ..., model: _Optional[str] = ..., series: _Optional[str] = ..., damage_pr: _Optional[str] = ..., damage_sec: _Optional[str] = ..., keys: _Optional[str] = ..., odobrand: _Optional[str] = ..., fuel: _Optional[str] = ..., drive: _Optional[str] = ..., transmission: _Optional[str] = ..., color: _Optional[str] = ..., status: _Optional[str] = ..., title: _Optional[str] = ..., vin: _Optional[str] = ..., engine: _Optional[str] = ..., engine_size: _Optional[float] = ..., location: _Optional[str] = ..., location_old: _Optional[str] = ..., location_id: _Optional[int] = ..., country: _Optional[str] = ..., document: _Optional[str] = ..., document_old: _Optional[str] = ..., currency: _Optional[str] = ..., seller: _Optional[str] = ..., is_buynow: bool = ..., iaai_360: _Optional[str] = ..., copart_exterior_360: _Optional[_Iterable[str]] = ..., copart_interior_360: _Optional[str] = ..., video: _Optional[str] = ..., link_img_hd: _Optional[_Iterable[str]] = ..., link_img_small: _Optional[_Iterable[str]] = ..., is_offsite: bool = ..., location_offsite: _Optional[str] = ..., link: _Optional[str] = ..., body_type: _Optional[str] = ..., seller_type: _Optional[str] = ..., vehicle_score: _Optional[str] = ..., form_get_type: _Optional[str] = ..., sale_history: _Optional[_Iterable[_Union[SaleHistory, _Mapping]]] = ..., sale_date: _Optional[str] = ..., sale_status: _Optional[str] = ..., purchase_price: _Optional[int] = ...) -> None: ...

class SaleHistory(_message.Message):
    __slots__ = ("lot_id", "site", "base_site", "vin", "sale_status", "sale_date", "purchase_price", "is_buynow", "buyer_state", "buyer_country", "vehicle_type")
    LOT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    BASE_SITE_FIELD_NUMBER: _ClassVar[int]
    VIN_FIELD_NUMBER: _ClassVar[int]
    SALE_STATUS_FIELD_NUMBER: _ClassVar[int]
    SALE_DATE_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_PRICE_FIELD_NUMBER: _ClassVar[int]
    IS_BUYNOW_FIELD_NUMBER: _ClassVar[int]
    BUYER_STATE_FIELD_NUMBER: _ClassVar[int]
    BUYER_COUNTRY_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    lot_id: int
    site: int
    base_site: str
    vin: str
    sale_status: str
    sale_date: str
    purchase_price: int
    is_buynow: bool
    buyer_state: str
    buyer_country: str
    vehicle_type: str
    def __init__(self, lot_id: _Optional[int] = ..., site: _Optional[int] = ..., base_site: _Optional[str] = ..., vin: _Optional[str] = ..., sale_status: _Optional[str] = ..., sale_date: _Optional[str] = ..., purchase_price: _Optional[int] = ..., is_buynow: bool = ..., buyer_state: _Optional[str] = ..., buyer_country: _Optional[str] = ..., vehicle_type: _Optional[str] = ...) -> None: ...
