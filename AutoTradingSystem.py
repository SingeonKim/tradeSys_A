class StokerBrockerDriver:
    def __init__(self, broker):
        self.__broker = broker

    def buy_nice_timing(self, stock_name, input_balance):
        prev = 0
        for i in range(3):
            current_price = self.__broker.get_price(stock_name)
            if current_price <= prev:
                return False
            prev = current_price

        self.__broker.buy(stock_name, current_price, input_balance // current_price)
        return True
