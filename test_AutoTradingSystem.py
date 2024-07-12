from unittest import TestCase
from unittest.mock import Mock, patch, create_autospec

from AutoTradingSystem import AutoTradingSystem
from StokerBrockerDriver import StokerBrockerDriver, KiwerDriver, NemoDriver


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
    def test_AutoTradingSystem_자동매수확인_1_True(self):
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

    def test_AutoTradingSystem_자동매수확인_2_False(self):
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


    # StokerBrockerDriver을 가지고 있는 AutoTradingSystem 객체 생성 및
    # -> 아마 자동 매매 구현하신분과 충돌이 날텐데 PR 시 팀장이 해결해보겠씁니다.
    # 자동 매수 구현
    # 요구 사항: 100ms 에 걸쳐 3번 가격 확인
    # 3번에 걸쳐 내린다면 현재가 기준 count 만큼 매수(buy 호출) 및 True 반환
    # 내리지 않았다면 False 반환

    # sell_nice_timing(code, count) -> bool
    def test_AutoTradingSystem_자동매매확인_1_True(self):
        # arrange
        broker = create_autospec(StokerBrockerDriver)
        broker.login.return_value = True
        broker.buy.return_value = True
        broker.sell.return_value = True
        broker.get_price.side_effect = [300, 200, 100]

        ats = AutoTradingSystem(broker)

        # act
        # 자동 매수 성공할 거임
        actual = ats.sell_nice_timing('AAPL', 3)

        # assert
        self.assertTrue(actual)

    def test_AutoTradingSystem_자동매매확인_2_False(self):
        # arrange
        broker = create_autospec(StokerBrockerDriver)
        broker.login.return_value = True
        broker.buy.return_value = True
        broker.sell.return_value = True
        broker.get_price.side_effect = [300, 200, 300]

        ats = AutoTradingSystem(broker)

        # act
        # 자동 매수 실패( 내리지않았음 300 -> 200 -> 300
        actual = ats.sell_nice_timing('AAPL', 3)

        # assert
        self.assertFalse(actual)

    def test_키위드라이버(self):
        # arrange
        self.driver = KiwerDriver()

        self.assertTrue(self.driver.login("user_id", "password"))

        self.assertTrue(self.driver.buy("AAPL", 150.0, 10))

        self.assertTrue(self.driver.sell("AAPL", 155.0, 5))

        price = self.driver.get_price("AAPL")
        self.assertNotEqual(price, -1)
        self.assertGreaterEqual(price, 5000)
        self.assertLessEqual(price, 5899)


    def test_네모드라이버(self):
        # arrange
        self.driver = NemoDriver()

        self.assertTrue(self.driver.login("user_id", "password"))

        self.assertTrue(self.driver.buy("AAPL", 150.0, 10))

        self.assertTrue(self.driver.sell("AAPL", 155.0, 5))

        price = self.driver.get_price("AAPL")
        self.assertNotEqual(price, -1)
        self.assertGreaterEqual(price, 5000)
        self.assertLessEqual(price, 5899)

    def test_드라이버선택(self):
        # arrange
        broker = KiwerDriver()
        ats = AutoTradingSystem(broker)

        # act (네모 드라이버로 변경)
        ats.select_stock_brocker(NemoDriver())

        # assert (네모 드라이버가 맞는지!)
        self.assertIsInstance(ats._AutoTradingSystem__broker, NemoDriver)

    # 사실 private 메소드여야 할 것 같은데
    # 그냥 public으로 할게요
    def test_종목유효성_검사(self):
        # arrange
        broker_not_important = KiwerDriver()
        ats = AutoTradingSystem(broker_not_important)
        wrong_code1 = 'WRONG1'
        wrong_code2 = '123'
        good_code1 = 'A005930'
        good_code2 = 'A005930'

        # act
        actual1 = ats.is_valid_code(wrong_code1)
        actual2 = ats.is_valid_code(wrong_code2)
        actual3 = ats.is_valid_code(good_code1)
        actual4 = ats.is_valid_code(good_code2)

        # assert
        self.assertFalse(actual1)
        self.assertFalse(actual2)
        self.assertTrue(actual3)
        self.assertTrue(actual4)
