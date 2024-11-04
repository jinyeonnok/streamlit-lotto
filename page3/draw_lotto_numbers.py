#  pate3/draw_lotto_numbers.py


import pandas as pd
import numpy as np
from page3.get_data import Lotto_class
from tensorflow import keras
from keras.layers import LeakyReLU
import joblib
import streamlit as st

# 모델과 스케일러를 불러오는 함수
@st.cache_resource
def load_model_and_scaler():
    model = keras.models.load_model('model/ann_model.h5', custom_objects={'LeakyReLU': LeakyReLU})
    scaler = joblib.load('model/scaler.save')
    return model, scaler

# 모델과 스케일러 불러오기
try:
    model, scaler = load_model_and_scaler()
except Exception as e:
    st.error(f"모델 로드 중 에러 발생: {e}")

def analyze_number(df, draw_number, number) -> dict:
    '''
    df = 전체기록
    draw_number = 1144
    number = 1
    '''
    
    # 분석할 회차
    current_draw_index = draw_number
    
    # 0. 출현 여부
    appearance = 1 if number in df.loc[draw_number].values else 0
    
    # 1. 연속 출현 횟수
    consecutive_count = 0
    for i in range(current_draw_index, 0, -1):  # 0보다 클 때까지
        if number in df.loc[i].values:
            consecutive_count += 1
        else:
            break

    # 2. 연속 미출현 횟수
    consecutive_non_appearance = 0
    for i in range(current_draw_index , 0, -1):  # 0보다 클 때까지
        if number not in df.loc[i].values:
            # print(df.loc[i].values)
            consecutive_non_appearance += 1
        else:
            break

    # 3. 최근 100회차 출현 횟수
    start_index = draw_number 
    end_index = draw_number - 99
    recent_100_count = df.loc[start_index : end_index].isin([number]).sum().sum()
    
    # 4. 최근 4회차 출현 횟수
    start_index = draw_number 
    end_index = draw_number - 3
    recent_4_count = df.loc[start_index : end_index].isin([number]).sum().sum()
    
    return {
        '번호' : number,
        '회차' : draw_number,
        "출현 여부" : appearance,
        "연속 출현 횟수": consecutive_count,
        "연속 미출현 횟수": consecutive_non_appearance,
        "최근 100회차 출현 횟수": recent_100_count,
        "최근 4회차 출현 횟수": recent_4_count,
    }

def draw_lotto_numbers(최근회차, 전체기록, scaler = scaler) -> pd.DataFrame:
    results = []
    for number in range(1, 46):
        record = pd.DataFrame([analyze_number(전체기록, 최근회차, number)])
        
        features = pd.DataFrame(record[['연속 출현 횟수', '연속 미출현 횟수', '최근 100회차 출현 횟수', '최근 4회차 출현 횟수']]).reset_index(drop=True)
        
        features_scaled = scaler.transform(features)
        
        predictions = model.predict(features_scaled, verbose=0)
    
        formatted_predictions = [f"{pred[0]:.4f}" for pred in predictions]
    
        result = pd.DataFrame([{
                                    '번호': number,
                                    '확률': float(formatted_predictions[0])
                                }])
                            
        results.append(result)    
    
    results = pd.concat(results)
    results['확률'] = results['확률'] / results['확률'].sum()
    
    selected_numbers = np.random.choice(results['번호'], size=6, replace=False, p=results['확률'])
    sorted_numbers = np.sort(selected_numbers)
    
    df_numbers = pd.DataFrame([sorted_numbers], columns=[1, 2, 3, 4, 5, 6])

    return df_numbers


# analyze_number(전체기록, 최근회차, 1)
