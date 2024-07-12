from abc import ABC, abstractmethod


class I_StokerBrockerDriver(ABC):
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
    def get_price(self, price) -> int:
        pass
