import pandas as pd
from collections import Counter
from typing import Tuple, Dict

class ErrorAnalyzer:
    @staticmethod
    def get_most_frequent_errors(df: pd.DataFrame, top_n: int = 5) -> Dict[str, int]:
        return dict(Counter(df['error_code']).most_common(top_n))

    @staticmethod
    def get_top_error_device(df: pd.DataFrame) -> Tuple[str, pd.DataFrame]:
        top_device = df['sms_tag'].value_counts().index[0]
        device_errors = df[df['sms_tag'] == top_device]
        return top_device, device_errors

    @staticmethod
    def analyze_error_trend(df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(df['formatted_datetime'].dt.hour)['error_code'].count()

    @staticmethod
    def analyze_errors_by_network_type(df: pd.DataFrame) -> Dict[int, Dict[str, int]]:
        return {
            network_type: dict(Counter(group['error_code']).most_common(5))
            for network_type, group in df.groupby('network_type')
        }

    @staticmethod
    def analyze_errors_by_app(df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
        return {
            app: dict(Counter(group['error_code']).most_common(5))
            for app, group in df.groupby('report_app_package')
        }

    @staticmethod
    def analyze_errors_by_region(df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
        return {
            region: dict(Counter(group['error_code']).most_common(5))
            for region, group in df.groupby('so_code')
        }