from abc import ABC, abstractmethod
from random import random

from kiwer_api import KiwerAPI
from nemo_api import NemoAPI


class StokerBrockerDriver(ABC):
    @abstractmethod
    def login(self, id, pwd) -> bool:
        pass

    @abstractmethod
    def buy(self, code, price, count) -> bool:
        pass

    @abstractmethod
    def sell(self, code, price, count) -> bool:
        pass

    @abstractmethod
    def get_price(self, code) -> int:
        pass


class KiwerDriver(StokerBrockerDriver):
    def __init__(self):
        self.api = KiwerAPI()

    def login(self, id, pwd) -> bool:
        try:
            self.api.login(id, pwd)
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def buy(self, code, price, count):
        try:
            self.api.buy(code,count, price)
            return True
        except Exception as e:
            print(f"BUY failed: {e}")
            return False

    def sell(self, code, price, count):
        try:
            self.api.sell(code, count, price)
            return True
        except Exception as e:
            print(f"SELL failed: {e}")
            return False

    def get_price(self, code) -> int:
        return self.api.current_price(code)


class NemoDriver(StokerBrockerDriver):
    def __init__(self):
        self.api = NemoAPI()

    def login(self, id, pwd):
        try:
            self.api.cerification(id, pwd)
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def buy(self, code, price, count):
        try:
            self.api.purchasing_stock(code, price, count)
            return True
        except Exception as e:
            print(f"BUY failed: {e}")
            return False

    def sell(self, code, price, count):
        try:
            self.api.selling_stock(code, price, count)
            return True
        except Exception as e:
            print(f"SELL failed: {e}")
            return False

    def get_price(self, code, minute=0) -> int:
        return self.api.get_market_price(code, minute)
