# main.py
import streamlit as st
import pandas as pd
from page3.get_data import Lotto_class
from my_html.tab1 import display_current_numbers 
from my_html.tab2 import display_past_records    
from my_html.tab3 import draw_number    


# Lotto_class의 인스턴스 생성
lotto_instance = Lotto_class()

# 전체 기록을 캐시하는 함수
@st.cache_data
def load_all_records():
    최근회차 = lotto_instance.최근회차()
    전체기록 = pd.DataFrame(lotto_instance.download_records(1, 최근회차)).transpose()
    전체기록.index = 전체기록.index.str.replace('회차', '').astype(int)
    return 전체기록

# 전체 기록을 한 번만 불러오기
전체기록 = load_all_records()
최근회차 = lotto_instance.최근회차()

st.title('이번주 당첨번호')
st.title(f'최근 회차 : {최근회차}')


# 탭 추가
tab1, tab2, tab3 = st.tabs(["당첨 번호", "과거 당첨 기록", "AI 로또 추첨기"])

with tab1:
    display_current_numbers(lotto_instance,최근회차, 전체기록)

with tab2:
    display_past_records(lotto_instance, 최근회차)

with tab3:
    
    # 사용자가 몇 개의 번호를 추첨할지 입력할 수 있는 텍스트 입력 필드 추가
    num_draws = st.number_input('몇 개의 추가 번호를 뽑으시겠습니까?', min_value=1, max_value=10, value=3)

    # 생성 버튼 추가
    if st.button('번호 생성'):
        st.write("생성된 번호 :")
        draw_number(최근회차, 전체기록,num_draws)  # 입력받은 숫자를 draw_number 함수에 전달