from unittest import TestCase
from unittest.mock import Mock, patch, create_autospec

from AutoTradingSystem import AutoTradingSystem
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

    # StokerBrockerDriver을 가지고 있는 AutoTradingSystem 객체 생성 및
    # 자동 매매 구현
    # 요구 사항: 100ms 에 걸쳐 3번 가격 확인
    # 3번에 걸쳐 오른다면 현재가 기준 가능한 개수 만큼 매매 (sell 호출) 및 True 반환
    # 오르지 않았다면 False 반환

    # buy_nice_timing(code, price) -> bool
    def test_AutoTradingSystem_자동매매확인_1_True(self):
        # arrange
        broker = create_autospec(StokerBrockerDriver)
        broker.login.return_value = True
        broker.buy.return_value = True
        broker.sell.return_value = True
        broker.get_price.side_effect = [100, 200, 300]

        ats = AutoTradingSystem(broker)

        # act
        # 자동 매매 성공할 거임
        actual = ats.buy_nice_timing('AAPL', 900)

        # assert
        self.assertTrue(actual)

    def test_AutoTradingSystem_자동매매확인_2_False(self):
        # arrange
        broker = create_autospec(StokerBrockerDriver)
        broker.login.return_value = True
        broker.buy.return_value = True
        broker.sell.return_value = True
        broker.get_price.side_effect = [100, 200, 100]

        ats = AutoTradingSystem(broker)

        # act
        # 자동 매매 실패( 오르지않았음 100 -> 200 -> 100)
        actual = ats.buy_nice_timing('AAPL', 900)

        # assert
        self.assertFalse(actual)
