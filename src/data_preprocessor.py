import pandas as pd
from typing import Tuple

class DataPreprocessor:
    @staticmethod
    def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # 데이터 타입 변환
        df['formatted_datetime'] = pd.to_datetime(df['formatted_datetime'])
        df['network_type'] = df['network_type'].astype(int)
        
        # 결측치 처리
        df = df.dropna()
        
        # 이상치 처리
        df = df[df['error_code'].str.len() < 10]
        
        # 불필요한 공백 제거
        for col in df.select_dtypes(['object']):
            df[col] = df[col].str.strip()
        
        # 테스트 데이터와 라이브 데이터 분리
        live_data = df[~df['sms_tag'].str.startswith('TB')].copy()
        test_data = df[df['sms_tag'].str.startswith('TB')].copy()
        
        return live_data, test_data

    @staticmethod
    def normalize_error_codes(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['error_code'] = df['error_code'].str.upper()
        return df

    @staticmethod
    def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['hour'] = df['formatted_datetime'].dt.hour
        df['day_of_week'] = df['formatted_datetime'].dt.dayofweek
        return df

    @staticmethod
    def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['network_type'] = pd.Categorical(df['network_type']).codes
        return df