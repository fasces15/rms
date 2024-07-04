import unittest
import pandas as pd
from src.error_analyzer import ErrorAnalyzer

class TestErrorAnalyzer(unittest.TestCase):
    def setUp(self):
        # 테스트용 데이터 생성
        self.test_data = pd.DataFrame({
            'so_code': ['001', '002', '001', '002'],
            'sms_tag': ['123456', '789012', '345678', '901234'],
            'network_type': [1, 2, 1, 2],
            'formatted_datetime': pd.to_datetime(['2024-06-17 00:00', '2024-06-17 00:01', '2024-06-17 00:02', '2024-06-17 00:03']),
            'error_code': ['E134', 'E999', 'E134', 'E001'],
            'report_app_package': ['app1', 'app2', 'app1', 'app2'],
            'report_app_ver': ['1.0', '2.0', '1.0', '2.0'],
            'node_id': ['N1', 'N2', 'N1', 'N2'],
            'firmware_version': ['0.1', '0.2', '0.1', '0.2']
        })

    def test_get_most_frequent_errors(self):
        result = ErrorAnalyzer.get_most_frequent_errors(self.test_data)
        self.assertEqual(len(result), 3)
        self.assertEqual(result['E134'], 2)

    def test_get_top_error_device(self):
        top_device, device_errors = ErrorAnalyzer.get_top_error_device(self.test_data)
        self.assertIsInstance(top_device, str)
        self.assertEqual(len(device_errors), 2)

    def test_analyze_error_trend(self):
        result = ErrorAnalyzer.analyze_error_trend(self.test_data)
        self.assertEqual(len(result), 1)  # 모든 오류가 같은 시간대에 발생

    def test_analyze_errors_by_network_type(self):
        result = ErrorAnalyzer.analyze_errors_by_network_type(self.test_data)
        self.assertEqual(len(result), 2)  # 두 가지 네트워크 유형

    def test_analyze_errors_by_app(self):
        result = ErrorAnalyzer.analyze_errors_by_app(self.test_data)
        self.assertEqual(len(result), 2)  # 두 가지 앱

    def test_analyze_errors_by_region(self):
        result = ErrorAnalyzer.analyze_errors_by_region(self.test_data)
        self.assertEqual(len(result), 2)  # 두 가지 지역

if __name__ == '__main__':
    unittest.main()