class CalculatorError(Exception):
    pass

class NotFoundError(CalculatorError):
    """Базовый класс для всех ошибок 'не найдено'"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class LocationNotFoundError(NotFoundError):
    def __init__(self, message="Location not found"):
        super().__init__(message)

class DestinationNotFoundError(NotFoundError):
    def __init__(self, message="Destination not found"):
        super().__init__(message)

class VehicleTypeNotFoundError(NotFoundError):
    def __init__(self, message="Vehicle type not found"):
        super().__init__(message)

class DeliveryPriceNotFoundError(NotFoundError):
    def __init__(self, message="Delivery price not found"):
        super().__init__(message)

class ShippingPriceNotFoundError(NotFoundError):
    def __init__(self, message="Shipping price not found"):
        super().__init__(message)