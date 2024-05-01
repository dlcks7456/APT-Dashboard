import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_icon="💲",
    page_title="머니레터 | 잘쓸레터",
)

st.title("🙋‍♂️ 어피티 구독자 대시보드")

st.divider()

# 데이터
df = pd.read_csv('data/data.csv', low_memory=False)
rename_cols = {
    '이메일 주소': 'email',
    '이메일 수신 상태': 'email_status',
    '이름': 'name',
    '구독폼 유입 경로': 'subscribe_path',
    '추천인': 'recommend_by',
    '추가 경로': 'add_path',
    '그룹': 'group',
    '광고성 정보 수신 동의': 'ad_agree_status',
    '구독일': 'subscribe_date',
    '마지막 업데이트일': 'last_update_date',
    '구독 해지 사유': 'why_unsubscribe',
    }
df.rename(columns=rename_cols, inplace=True)

df.subscribe_date = pd.to_datetime(df.subscribe_date)
df['sub_year'] = df.apply(lambda x: x.subscribe_date.year, axis=1)
df['sub_month'] = df.apply(lambda x: x.subscribe_date.month, axis=1)
df['sub_day'] = df.apply(lambda x: x.subscribe_date.day, axis=1)

######


col_1, col_2 = st.columns([3, 7])

# 구독자 수 게이지 차트
current_subscribers = 5000
goal_subscribers = 10000

# 게이지 차트 생성
gauge_chart = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = current_subscribers,
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {
            'range': [None, goal_subscribers], 
            'tickwidth': 1, 
            'tickcolor': "darkblue"
            },
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {
                'range': [0, goal_subscribers*0.5], 
                'color': 'lightgray'
            },
            {
                'range': [goal_subscribers*0.5, goal_subscribers*0.75], 
                'color': 'gray'},
            {'range': [goal_subscribers*0.75, goal_subscribers], 
                'color': 'blue'},
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': goal_subscribers*0.9}
    }
))


with col_1 :
    st.write("#### 이번 달 구독자 수")
    st.plotly_chart(
        gauge_chart, 
        use_container_width=True)
    

### 월별 구독자 차트
now_year = datetime.now().year
now_month = datetime.now().month
counts = df[df.sub_year == 2024]['sub_month'].value_counts().sort_index()
counts.index = [f'{x}월' for x in counts.index]

months = [f'{x}월' for x in range(1,13)]
counts = counts.reindex(months, fill_value=0)

subscribe_bar_chart = px.bar(
    x=counts.index,
    y=counts.values,
    labels={
        'x': f'{now_year}년 구독자',
        'y': '구독자수'
        }
    )

with col_2 :
    st.write('#### 월별 구독자 수')
    st.plotly_chart(subscribe_bar_chart, use_container_width=True)
