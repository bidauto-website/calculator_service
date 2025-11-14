from enum import Enum


class FeeTypeEnum(str, Enum):
    CLEAN_TITLE_FEE = 'clean_title_fee'
    NON_CLEAN_TITLE_FEE = 'non_clean_title_fee'
    CRASHED_TOYS_FEE = 'crashed_toys_fee'
    LESS_FEE = 'less_fee'