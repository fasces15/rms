import unittest
import pandas as pd
from src.data_preprocessor import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        # 테스트용 데이터 생성
        self.test_data = pd.DataFrame({
            'so_code': ['001', '002'],
            'sms_tag': ['123456', 'TB789012'],
            'network_type': ['1', '2'],
            'formatted_datetime': ['2024.6.17 0:00', '2024.6.17 0:01'],
            'error_code': ['E134', '9999'],
            'report_app_package': ['app1', 'app2'],
            'report_app_ver': ['1.0', '2.0'],
            'node_id': ['N1', 'N2'],
            'firmware_version': ['0.1', '0.2']
        })

    def test_preprocess_data(self):
        live_data, test_data = DataPreprocessor.preprocess_data(self.test_data)
        self.assertEqual(len(live_data), 1)
        self.assertEqual(len(test_data), 1)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(live_data['formatted_datetime']))

    def test_normalize_error_codes(self):
        processed_data = DataPreprocessor.normalize_error_codes(self.test_data)
        self.assertTrue(all(processed_data['error_code'].str.isupper()))

    def test_create_time_features(self):
        processed_data = DataPreprocessor.create_time_features(self.test_data)
        self.assertIn('hour', processed_data.columns)
        self.assertIn('day_of_week', processed_data.columns)

    def test_encode_categorical_features(self):
        processed_data = DataPreprocessor.encode_categorical_features(self.test_data)
        self.assertTrue(pd.api.types.is_numeric_dtype(processed_data['network_type']))

if __name__ == '__main__':
    unittest.main()