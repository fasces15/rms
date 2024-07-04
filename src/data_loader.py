import pandas as pd
from config import DATA_PATH

class DataLoader:
    @staticmethod
    def load_data(file_path: str = DATA_PATH) -> pd.DataFrame:
        # 열 이름 정의
        columns = ['so_code', 'sms_tag', 'network_type', 'formatted_datetime', 
                   'error_code', 'report_app_package', 'report_app_ver', 
                   'node_id', 'firmware_version']
        
        # 파일 읽기
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # 첫 번째 줄(헤더) 제거
        lines = lines[1:]
        
        # 데이터 처리
        data = []
        for line in lines:
            fields = line.strip().split()
            if len(fields) > 9:
                # 마지막 두 필드를 합치기
                fields = fields[:-2] + [' '.join(fields[-2:])]
            elif len(fields) < 9:
                # 부족한 필드를 빈 문자열로 채우기
                fields += [''] * (9 - len(fields))
            data.append(fields)
        
        # DataFrame 생성
        df = pd.DataFrame(data, columns=columns)
        
        # node_id와 firmware_version 처리
        df['node_id_temp'] = df['node_id'].str.split().str[0]
        df['firmware_version'] = df['node_id'].str.split().str[1:].str.join(' ')
        df['node_id'] = df['node_id_temp']
        df = df.drop('node_id_temp', axis=1)
        
        # NaN 값을 빈 문자열로 대체
        df = df.fillna('')
        
        return df