from enum import Enum


class AuctionEnum(str, Enum):
    COPART = 'COPART'
    IAAI = 'IAAI'

class SpecificAuctionEnum(str, Enum):
    DEALER = 'DEALER'
    # add manheim for bidauto


