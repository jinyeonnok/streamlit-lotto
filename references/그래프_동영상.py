import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 데이터 생성
data = {
    '회차': ['1143회차', '1142회차', '1141회차', '1140회차', '1139회차', 
            '1138회차', '1137회차', '1136회차', '1135회차', '1134회차'],
    '번호1': [10, 2, 7, 7, 5, 14, 4, 21, 1, 3],
    '번호2': [16, 8, 11, 10, 12, 16, 9, 33, 6, 7],
    '번호3': [17, 28, 12, 22, 15, 19, 12, 35, 13, 9],
    '번호4': [27, 30, 21, 29, 30, 20, 15, 38, 19, 13],
    '번호5': [28, 37, 26, 31, 37, 29, 33, 42, 21, 19],
    '번호6': [36, 41, 35, 38, 40, 34, 45, 44, 33, 24],
    '보너스': [6, 22, 20, 15, 18, 35, 26, 1, 4, 23]
}

# DataFrame 생성 및 회차를 인덱스로 설정
df = pd.DataFrame(data)
df.set_index('회차', inplace=True)


#%%

# 번호 출현 빈도 계산
numbers = np.arange(1, 46)  # 1부터 45까지의 번호
frequency = np.zeros((len(df), len(numbers)))

# 각 회차별 번호 출현 빈도 계산
for i in range(len(df)):
    for j in range(0, 7):  # 번호1~6 및 보너스
        number = df.iloc[i, j]  # 현재 회차의 번호
        frequency[i, number - 1] += 1  # -1로 인덱스 조정

# 누적 빈도 계산
cumulative_frequency = np.cumsum(frequency, axis=0)

# 그래프 설정
fig, ax = plt.subplots(figsize=(12, 6))  # 그래프 크기 조정
bar = ax.bar(numbers, cumulative_frequency[0], color='blue')

# y축 범위 초기 설정
ax.set_ylim(0, np.max(cumulative_frequency) + 1)  # y축 최대값 설정
ax.set_title('Lotto Number Cumulative Frequency Over Time')
ax.set_xlabel('Numbers')
ax.set_ylabel('Cumulative Frequency')

# 애니메이션 업데이트 함수
def update(frame):
    for rect, height in zip(bar, cumulative_frequency[frame]):
        rect.set_height(height)  # 각 바의 높이를 업데이트
    # y축 범위 업데이트
    ax.set_ylim(0, np.max(cumulative_frequency) + 1)  # y축 최대값 동적으로 설정
    ax.set_title(f'Lotto Number Cumulative Frequency - from 1 to 1143')  # 제목 업데이트
    return bar

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=len(df), blit=True, repeat=False, interval=50)  # 500ms마다 업데이트

# 그래프 표시
plt.show()
