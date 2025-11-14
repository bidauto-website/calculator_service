from pydantic import BaseModel


class City(BaseModel):
    name: str
    price: int

class VATs(BaseModel):
    vats: list[City]
    eu_vats: list[City]

class SpecialFee(BaseModel):
    price: int
    name: str

class AdditionalFeesOut(BaseModel):
    summ: int
    fees: list[SpecialFee]
    auction_fee: int
    internet_fee: int
    live_fee: int

class BaseCalculator(BaseModel):
    broker_fee: int
    transportation_price: list[City]
    ocean_ship: list[City]
    additional: AdditionalFeesOut
    totals: list[City]

class DefaultCalculator(BaseCalculator):
    auction_fee: int
    live_fee: int
    internet_fee: int

class EUCalculator(BaseCalculator):
    totals_without_default: list[City]
    vats: VATs
    custom_agency: int = 0



class CalculatorOut(BaseModel):
    calculator: DefaultCalculator
    eu_calculator: EUCalculator


class Calculator(BaseModel):
    calculator_in_dollars: CalculatorOut
    calculator_in_currency: CalculatorOut
    destinations: list[str]



