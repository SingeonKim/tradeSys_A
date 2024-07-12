from StokerBrockerDriver import StokerBrockerDriver
import time


class AutoTradingSystem:
    def __init__(self, broker: StokerBrockerDriver):
        self.__broker = broker

    def sell_nice_timing(self, code, count) -> bool:
        res = []
        for _ in range(3):
            res.append(self.__broker.get_price(code))
            # time.sleep(0.1)

        is_downtrend = (res[0] > res[1]) and (res[1] > res[2])
        if is_downtrend:
            self.__broker.sell(code, res[2], count)

        return is_downtrend