# my_html/tab3.py

from page3 import draw_lotto_numbers
import streamlit as st



# 색상 지정 함수
def get_color(number):
    number = int(number)
    if 1 <= number <= 10:
        return "#f9c74f"  # 노란색
    elif 11 <= number <= 20:
        return "#007bff"  # 파란색
    elif 21 <= number <= 30:
        return "#dc3545"  # 빨간색
    elif 31 <= number <= 40:
        return "#6c757d"  # 회색
    elif 41 <= number <= 45:
        return "#28a745"  # 녹색
    else:
        return "#000000"  # 기본 색상

def display_lotto_numbers(numbers):
    lotto_balls_html = '<div class="lotto-container">'
    for value in numbers.values():
        color = get_color(value)
        lotto_balls_html += f'<div class="lotto-ball" style="background-color: {color}; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin: 5px; color: white; font-weight: bold;">{value}</div>'
    lotto_balls_html += '</div>'
    st.markdown(lotto_balls_html, unsafe_allow_html=True)



def draw_number(n = 1):

    for n in range(0,n):
        draw_numbers = draw_lotto_numbers.draw_lotto_numbers(draw_lotto_numbers.최근회차)
        # display_lotto_numbers(draw_numbers.iloc[0])
        
        display_lotto_numbers(draw_numbers.iloc[0].to_dict())