from unittest import TestCase
from unittest.mock import Mock, patch, create_autospec

from StokerBrockerDriver import StokerBrockerDriver


class AutoTradingSystemTest(TestCase):

    # 아래 스펙으로 StokerBrockerDriver 추상클래스 구현해주시면 되겠습니다.
    # ABC 상속 및 @abstractmethod 작성필요

    # login(id, pass) -> Boolean
    # buy(code, price, count) -> Boolean
    # sell(code, price, count) -> Boolean
    # get_price(price) -> int
    def test_추상클래스_구현_확인(self):
        # arrange
        broker = create_autospec(StokerBrockerDriver)
        broker.login.return_value = True
        broker.buy.return_value = True
        broker.sell.return_value = True
        broker.get_price.return_value = 100

        # act


        # assert
        self.assertTrue(broker.login('test_user', 'password'))
        self.assertTrue(broker.buy('AAPL', 150.0, 10))
        self.assertTrue(broker.sell('AAPL', 155.0, 5))
        self.assertEqual(broker.get_price('AAPL'), 100)
