import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def load_and_preprocess_data(file_path):
    # 데이터 로드 및 전처리
    columns = ['so_code', 'sms_tag', 'network_type', 'formatted_datetime', 'error_code', 'report_app_package', 'report_app_ver', 'node_id', 'firmware_version']
    df = pd.read_csv(file_path, names=columns, sep='\s+')
    df['formatted_datetime'] = pd.to_datetime(df['formatted_datetime'])
    return df

def analyze_data(df):
    # 1. 시간대별 오류 발생 패턴 분석
    hourly_errors = df.groupby(df['formatted_datetime'].dt.hour)['error_code'].count()
    
    # 2. 네트워크 유형별 오류 분포 비교
    network_errors = df.groupby('network_type')['error_code'].value_counts().unstack(fill_value=0)
    
    # 3. 앱 패키지별 가장 빈번한 오류 유형
    app_errors = df.groupby('report_app_package')['error_code'].value_counts().unstack(fill_value=0)
    
    # 4. 지역별(so_code) 오류 발생 빈도 분석
    region_errors = df.groupby('so_code')['error_code'].count().sort_values(ascending=False)
    
    # 5. 펌웨어 버전과 오류 발생 관계
    firmware_errors = df.groupby('firmware_version')['error_code'].value_counts().unstack(fill_value=0)
    
    # 6. 가장 문제가 많은 디바이스 식별 및 분석
    device_errors = df.groupby('sms_tag')['error_code'].count().sort_values(ascending=False).head(10)
    
    # 7. 오류 코드별 심각도 분류 및 분석
    error_severity = df['error_code'].value_counts()
    
    return hourly_errors, network_errors, app_errors, region_errors, firmware_errors, device_errors, error_severity

def create_visualizations(hourly_errors, network_errors, app_errors, region_errors, firmware_errors, device_errors, error_severity):
    # 시간대별 오류 발생 패턴 그래프
    fig_hourly = px.line(x=hourly_errors.index, y=hourly_errors.values, labels={'x': '시간', 'y': '오류 횟수'}, title='시간대별 오류 발생 패턴')
    
    # 네트워크 유형별 오류 분포 파이 차트
    fig_network = px.pie(values=network_errors.sum(), names=network_errors.index, title='네트워크 유형별 오류 분포')
    
    # 앱 패키지별 오류 유형 막대 그래프
    fig_app = px.bar(app_errors.head(), title='상위 5개 앱 패키지별 오류 유형')
    
    # 지역별 오류 발생 빈도 히트맵
    fig_region = px.density_heatmap(region_errors.reset_index(), x='so_code', y='error_code', z='count', title='지역별 오류 발생 빈도')
    
    # 펌웨어 버전별 오류 발생 빈도 테이블
    fig_firmware = go.Figure(data=[go.Table(header=dict(values=['펌웨어 버전', '오류 횟수']),
                                            cells=dict(values=[firmware_errors.index, firmware_errors.sum(axis=1)]))])
    fig_firmware.update_layout(title='펌웨어 버전별 오류 발생 빈도')
    
    # 가장 문제가 많은 디바이스 Top 10 막대 그래프
    fig_device = px.bar(device_errors, title='가장 문제가 많은 디바이스 Top 10')
    
    # 오류 코드별 심각도 도넛 차트
    fig_severity = px.pie(values=error_severity.values, names=error_severity.index, hole=0.4, title='오류 코드별 심각도 분류')
    
    return fig_hourly, fig_network, fig_app, fig_region, fig_firmware, fig_device, fig_severity

def main():
    df = load_and_preprocess_data('rms_error_log.txt')
    hourly_errors, network_errors, app_errors, region_errors, firmware_errors, device_errors, error_severity = analyze_data(df)
    figs = create_visualizations(hourly_errors, network_errors, app_errors, region_errors, firmware_errors, device_errors, error_severity)
    
    # HTML 파일 생성
    with open('analysis_results.html', 'w') as f:
        f.write('''
        <html>
        <head>
            <title>RMS 오류 로그 분석 결과</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>RMS 오류 로그 분석 결과</h1>
        ''')
        
        for i, fig in enumerate(figs):
            f.write(f'<div id="chart{i}"></div>')
            f.write(f'<script>var plotData = {fig.to_json()}; Plotly.newPlot("chart{i}", plotData.data, plotData.layout);</script>')
        
        f.write('</body></html>')

if __name__ == "__main__":
    main()