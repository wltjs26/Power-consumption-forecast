import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
from google.colab import drive
drive.mount('/content/drive')

# Load data
# Google Drive에서 파일 경로 설정
train_raw = pd.read_csv('/content/drive/MyDrive/train1.csv')
buildinginfo = pd.read_csv('/content/drive/MyDrive/building_info.csv')

# 건물번호를 기준으로 inner join
train = pd.merge(train_raw, buildinginfo, on='건물번호', how='inner')


# 건물번호를 기준으로 inner join
train = pd.merge(train_raw, buildinginfo, on='건물번호', how='inner')

print("============== merging.... ==============")

# 열 이름 바꾸기
train.rename(columns={
    '건물번호': 'building_number',
    '일시': 'datetime',
    '기온(C)': 'temperature_C',
    '강수량(mm)': 'precipitation_mm',
    '풍속(m/s)': 'wind_speed_m_s',
    '습도(%)': 'humidity_percent',
    '일조(hr)': 'sunlight_hours',
    '일사(MJ/m2)': 'solar_radiation_MJ_m2',
    '전력소비량(kWh)': 'power_consumption_kWh',
    '건물유형': 'building_type',
    '연면적(m2)': 'total_area_m2',
    '냉방면적(m2)': 'cooling_area_m2',
    '태양광용량(kW)': 'solar_capacity_kW',
    'ESS저장용량(kWh)': 'ess_storage_capacity_kWh',
    'PCS용량(kW)': 'pcs_capacity_kW'
}, inplace=True)


# 건물 유형을 영어로 매핑할 딕셔너리 생성
building_type_translation = {
    '건물기타': 'Other Building',
    '공공': 'Public',
    '대학교': 'University',
    '데이터센터': 'Data Center',
    '백화점및아울렛': 'Department Store & Outlet',
    '병원': 'Hospital',
    '상용': 'Commercial',
    '아파트': 'Apartment',
    '연구소': 'Research Center',
    '지식산업센터': 'Knowledge Industry Center',
    '할인마트': 'Discount Mart',
    '호텔및리조트': 'Hotel & Resort'
}

# 건물유형 열의 값을 영어로 변환
train['building_type'] = train['building_type'].map(building_type_translation)

train['datetime'] = pd.to_datetime(train['datetime'])


# Add date components
train['week'] = train['datetime'].dt.isocalendar().week
train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['weekday'] = train['datetime'].dt.dayofweek
train['hour'] = train['datetime'].dt.hour

# Ensure numeric columns for correlation
numeric_columns = train.select_dtypes(include=[np.number])
correlation_matrix = numeric_columns.corr()

print(train.head())

def create_holiday_variable(df):
    # 주말 날짜 확인 (토요일 = 5, 일요일 = 6)
    df['weekday'] = df['datetime'].dt.weekday  # 0: 월요일, 6: 일요일
    df['is_weekend'] = df['weekday'].isin([5, 6])  # 주말 여부 확인 (토/일은 True, 평일은 False)

    # 각 building_type별로 주말 소비 패턴 계산
    for building_type in df['building_type'].unique():
        building_data = df[df['building_type'] == building_type]

        if building_type == 'Discount Mart':
            # discount mart: 2주에 한 번 일요일 휴무
            building_data = building_data.sort_values(by='datetime')  # 날짜 순서로 정렬
            building_data['week_num'] = building_data['datetime'].dt.isocalendar().week  # ISO 주 번호 추출
            building_data['holiday'] = 0  # 기본값은 0으로 설정
            
            # 원하는 주 번호에 대해 일요일에만 holiday 설정 (예: 23, 25, 27, 29, 32주)
            holiday_weeks = [23, 25, 27, 29, 32]  # 휴무를 설정할 주 번호
            building_data.loc[(building_data['weekday'] == 6) & (building_data['week_num'].isin(holiday_weeks)), 'holiday'] = 1
            
            # 결과 반영
            df.loc[df['building_type'] == building_type, 'holiday'] = building_data['holiday']
        
        elif building_type == 'Data Center':
            # Data Center는 holiday 값을 모두 0으로 설정
            df.loc[df['building_type'] == building_type, 'holiday'] = 0
            
        else:
            # 다른 building_type: 주말 사용량 패턴에 따라 holiday 설정
            weekend_data = building_data[building_data['is_weekend']]
            weekday_data = building_data[~building_data['is_weekend']]

            weekend_mean = weekend_data['power_consumption_kWh'].mean()
            weekday_mean = weekday_data['power_consumption_kWh'].mean()

            # 주말 사용량이 평일보다 적으면 주말을 holiday로 설정
            holiday_condition = weekend_mean < weekday_mean

            if holiday_condition:
                df.loc[(df['building_type'] == building_type) & (df['is_weekend']), 'holiday'] = 1
            else:
                df.loc[(df['building_type'] == building_type) & (df['is_weekend']), 'holiday'] = 0

    # 평일은 기본적으로 0
    df['holiday'] = df['holiday'].fillna(0)

    return df

# 데이터 전처리 후 holiday 변수 생성
train['datetime'] = pd.to_datetime(train['datetime'])  # datetime 형식으로 변환

# 인덱스 초기화 (building_type이 인덱스일 경우 문제 해결)
train = train.reset_index(drop=True)  # drop=True를 사용하여 기존 인덱스를 제거

train = train.sort_values(by=['building_type', 'datetime'])  # building_type별로 시간 순서 정렬

# holiday 변수 생성
train = train.groupby('building_type', group_keys=False).apply(create_holiday_variable)

# 데이터프레임에서 필요한 열만 선택하여 확인
print(train[['building_type', 'datetime', 'power_consumption_kWh', 'weekday', 'holiday']].head())

# building_type이 'Discount Mart'이고 holiday가 1인 행만 선택하여 확인
print(train[(train['building_type'] == 'Discount Mart') & (train['holiday'] == 1)][['building_type', 'datetime', 'power_consumption_kWh', 'week','weekday','holiday']].head())

# train 데이터프레임을 'processed_train.csv' 파일로 내보내기
train.to_csv('processed_train.csv', index=False)  # index=False로 설정하여 인덱스 없이 저장

