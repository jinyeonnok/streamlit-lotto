# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:07:42 2024

@author: Rogio
"""



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import joblib
from sklearn.utils.class_weight import compute_class_weight
from keras.optimizers import Adamax
import numpy as np




기초통계 = '../통계자료/기초통계.xlsx'


전체기록 = pd.read_excel(기초통계, sheet_name= 'Sheet1', index_col= 0)
# 전체기록 = 전체기록.drop(columns = '보너스')
# 전체기록.index = 전체기록.index.str.replace('회차', '').astype(int)



#%%
# 특정 번호를 추출하는 함수
def analyze_number(df, draw_number, number):
    
    '''
    df = 전체기록
    draw_number = 1136
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
result = analyze_number(전체기록, 1144, 21)
print(result)

#%%
기록 = []
for i in range(len(전체기록),0,-1):
    
    for j in range(1,46):
        # 번호 = 전체기록.loc[i][j]
        번호 = j
        # print(번호)
        result = analyze_number(전체기록, i, 번호)

        기록.append(pd.DataFrame([result]))



기록 = pd.concat(기록)

#%%
기록.columns
독립변수 = pd.DataFrame(기록[['연속 출현 횟수', '연속 미출현 횟수', '최근 100회차 출현 횟수','최근 4회차 출현 횟수']]).reset_index(drop = True)

종속변수 = pd.DataFrame(기록['출현 여부']).reset_index(drop = True)
#%%




# 독립 변수와 종속 변수 분리
X = 기록[['연속 출현 횟수', '연속 미출현 횟수', '최근 100회차 출현 횟수', '최근 4회차 출현 횟수']]

# '연속 미출현 횟수' 제곱하여 영향력 증가
X['연속 미출현 횟수'] = X['연속 미출현 횟수'] * 2

y = 기록['출현 여부']

# 데이터 전처리: 훈련, 검증, 테스트 세트로 분할
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=2)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=2)

# X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=2)
# 스케일링
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
# X_test = scaler.transform(X_test)

# ANN 모델 정의
model = keras.Sequential([
    layers.Dense(16, activation='tanh', input_shape=(X_train.shape[1],)),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# model = keras.Sequential([
#     layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),  # 입력층
#     layers.BatchNormalization(),  # 배치 정규화
#     layers.Dropout(0.3),  # 드롭아웃
#     layers.Dense(32, activation='relu'),  # 첫 번째 은닉층
#     layers.BatchNormalization(),  # 배치 정규화
#     layers.Dropout(0.3),  # 드롭아웃
#     layers.Dense(16, activation='relu'),  # 두 번째 은닉층
#     layers.Dense(1, activation='sigmoid')  # 출력층
# ])

# 모델 컴파일
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.compile(optimizer=Adamax(lr=0.002), loss='binary_crossentropy', metrics=['accuracy'])


# 클래스 가중치 계산
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)

class_weights_dict = {
    0: class_weights[0],  # 0 클래스의 가중치
    1: class_weights[1]   # 1 클래스의 가중치
}



# 모델 학습# 모델 학습
model.fit(X_train, y_train, epochs=100, batch_size=8, validation_data=(X_val, y_val), verbose=1, class_weight=class_weights_dict)


# 모델 평가
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {accuracy:.4f}")


# 모델 및 스케일러 저장
model.save('ann_model.h5')
joblib.dump(scaler, 'scaler.save')  # 스케일러 저장
print("모델과 스케일러가 각각 'ann_model.h5'와 'scaler.save'로 저장되었습니다.")

#%%
# 예측

model = keras.models.load_model('ann_model.h5')
scaler = joblib.load('scaler.save')

predictions = model.predict(X_test)
predictions = (predictions > 0.5).astype(int)  # 확률을 0 또는 1로 변환
print("Predictions:", predictions.flatten())

#%%


# 저장된 모델과 스케일러 불러오기
model = keras.models.load_model('ann_model.h5')
scaler = joblib.load('scaler.save')
i = 0
for i in range(0,1000):
    sample = X_train[i].reshape(1, -1)  # 2차원 배열 형태로 변환
    # print(sample)
    prediction = model.predict(sample,verbose=0)
    # print(prediction)
    prediction_class = (prediction > 0.5).astype(int)  # 확률을 0 또는 1로 변환
    
    print("Predicted Class:", prediction_class.flatten()[0])










