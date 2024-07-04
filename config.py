import os

# 프로젝트 루트 디렉토리
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 데이터 파일 경로
DATA_PATH = os.path.join(ROOT_DIR, 'data', 'rms_error_log.txt')

# 결과 저장 경로
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')