from StokerBrockerDriver import StokerBrockerDriver
import time


class AutoTradingSystem:
    def __init__(self, broker: StokerBrockerDriver):
        self.__broker = broker

    def sell_nice_timing(self, code, count) -> bool:
        if not self.is_valid_code(code):
            raise ValueError("Not valid code")

        res = []
        for _ in range(3):
            res.append(self.__broker.get_price(code))
            # time.sleep(0.1)

        is_downtrend = (res[0] > res[1]) and (res[1] > res[2])
        current_price = res[2]
        if is_downtrend:
            self.__broker.sell(code, current_price, count)

        return is_downtrend

    def buy_nice_timing(self, code, count) -> bool:
        if not self.is_valid_code(code):
            raise ValueError("Not valid code")

        prev = 0
        for i in range(3):
            current_price = self.__broker.get_price(code)
            if current_price <= prev:
                return False
            prev = current_price

        self.__broker.buy(code, current_price, count // current_price)
        return True

    def select_stock_brocker(self, broker):
        self.__broker = broker

    def is_valid_code(self, code: str) -> bool:
        return len(code) == 7 and code[0] in ("A", "B", "C", "K") and code[1:].isdigit()
