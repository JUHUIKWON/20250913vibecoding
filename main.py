import streamlit as st
import pandas as pd
import altair as alt
import os

st.title("MBTI 유형별 비율 상위 국가 Top 10")

# 기본 파일 경로
default_file = "countriesMBTI_16types.csv"

df = None

# 1. 같은 폴더에 파일이 있는지 확인
if os.path.exists(default_file):
    st.info(f"기본 데이터 파일({default_file})을 불러왔습니다.")
    df = pd.read_csv(default_file)
else:
    # 2. 없으면 업로드 요청
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

if df is not None:
    # MBTI 컬럼 목록 정의
    mbti_types = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
                  "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

    # 선택할 MBTI 유형
    selected_type = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

    # 해당 유형 기준으로 Top 10 국가 추출
    top10 = df[["Country", selected_type]].copy()
    top10 = top10.sort_values(by=selected_type, ascending=False).head(10)

    # Altair 그래프
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_type, title="비율", axis=alt.Axis(format="%")),
            y=alt.Y("Country", sort="-x", title="국가"),
            tooltip=["Country", selected_type]
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(top10.reset_index(drop=True))
else:
    st.warning("데이터 파일을 불러오지 못했습니다. CSV 파일을 업로드하세요.")
