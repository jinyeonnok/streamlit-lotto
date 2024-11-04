# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 10:25:34 2024

@author: Rogio
"""



import pandas as pd
import numpy as np
from page3.get_data import Lotto_class
from tensorflow import keras
import joblib



# Lotto_class의 인스턴스 생성
lotto_instance = Lotto_class()

최근회차 = lotto_instance.최근회차()

전체기록 = pd.DataFrame(lotto_instance.download_records(1,최근회차)).transpose()

전체기록.index = 전체기록.index.str.replace('회차', '').astype(int)

model = keras.models.load_model('../model/ann_model.h5')
scaler = joblib.load('../model/scaler.save')

#%%

def analyze_number(df, draw_number, number):
    
    '''
    df = 전체기록
    draw_number = 1144
    number = 21
    '''
    
    
    # 분석할 회차
    current_draw_index = draw_number
    
    # 0. 출현 여부
    appearance = 1 if number in df.loc[draw_number].values else 0
    
    
    # 1. 연속 출현 횟수
    consecutive_count = 0
    for i in range(current_draw_index - 1, 0, -1):  # 0보다 클 때까지
        if number in df.loc[i].values:
            consecutive_count += 1
        else:
            break

    # 2. 연속 미출현 횟수
    consecutive_non_appearance = 0
    for i in range(current_draw_index - 1, 0, -1):  # 0보다 클 때까지
        if number not in df.loc[i].values:
            consecutive_non_appearance += 1
        else:
            break

    # 3. 최근 100회차 출현 횟수
    start_index = draw_number - 1
    end_index = draw_number - 101
    recent_100_count = df.loc[start_index : end_index].isin([number]).sum().sum()
    
    
    # 4. 최근 4회차 출현 횟수
    start_index = draw_number - 1
    end_index = draw_number - 5
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

# 예시: 1143회차의 첫번째 번호인 10을 분석
#%%
def draw_lotto_numbers(최근회차):
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
#%%


if __name__ == '__main__':
    추첨_n회 = []
    # 여러 번 시도하여 결과 출력
    for _ in range(10):  # 10번 반복
        추첨번호 = draw_lotto_numbers(최근회차) 
        print(_+1, 추첨번호.values)
        
        추첨_n회.append(pd.DataFrame(추첨번호)) 

    추첨_n회 = pd.concat(추첨_n회)
    추첨_n회 = 추첨_n회.reset_index(drop = True)
    #%%
    
    from collections import Counter
    
    flat_list = 추첨_n회.values.flatten()

    # 리스트를 카운트하여 각 번호의 빈도수 계산
    
    
    # 빈도수 계산
    frequency = Counter(flat_list)
    
    # 데이터프레임으로 변환
    추첨번호_빈도 = pd.DataFrame(frequency.items(), columns=['번호', '출현 횟수'])
    
    # 데이터프레임 정렬
    추첨번호_빈도 = 추첨번호_빈도.sort_values(by='번호').reset_index(drop=True)
    
    # # 결과 출력
    # print(추첨번호_빈도)


