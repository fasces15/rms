import unittest
from src.data_loader import DataLoader
from config import DATA_PATH

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        df = DataLoader.load_data(DATA_PATH)
        self.assertIsNotNone(df)
        self.assertEqual(len(df.columns), 9)  # 예상되는 열의 수
        self.assertGreater(len(df), 0)  # 데이터가 비어있지 않은지 확인

if __name__ == '__main__':
    unittest.main()