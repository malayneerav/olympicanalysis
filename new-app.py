import streamlit as st
import pandas as pd
from streamlit.web.server.server import server_port_is_manually_set
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor,helper

df = pd.read_csv(r"C:\Users\ASUS\Desktop\100daysofML\athlete_events.csv")
region_df = pd.read_csv(r"C:/Users/ASUS/Desktop/100daysofML/noc_regions.csv")


df= preprocessor.preprocess(df,region_df)
st.sidebar.header('Olympic Analysis')
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country Wise Analysis')
)

if user_menu=='Medal Tally':
    st.title("Medal Tally Overall")
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)
    selected_year= st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    st.dataframe(medal_tally)

if user_menu=='Overall Analysis':
    st.sidebar.header('Overall Analysis')
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.header('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)


    nations_overtime=helper.data(df,'region')
    fig = px.line(nations_overtime, x='Year', y='region')
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)

    events_overtime = helper.data(df, 'Event')
    fig = px.line(events_overtime, x='Year', y='Event')
    st.title('Events Over the Years')
    st.plotly_chart(fig)

    athletes_overtime = helper.data(df, 'Name')
    fig = px.line(athletes_overtime, x='Year', y='Name')
    st.title('Athletes Over the Years')
    st.plotly_chart(fig)

    st.title('No. of Events Over time sports-wise')
    fig,ax=plt.subplots(figsize=(20,20))
    y = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(y.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes Sports Wise')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)
if user_menu == 'Country Wise Analysis':
    st.title('Country-Year Wise Medal Tally')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    chosen_country=st.sidebar.selectbox('Select a country for medal tally',country_list)
    country_df = helper.yearwise_medaltally(df, chosen_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig)

    pivot=helper.country_sport_heatmap(df,chosen_country)
    st.title('Country-Sport Wise Medal Tally')
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pivot,annot=True)
    st.pyplot(fig)

    st.title('Top 15 Athletes of a Country')
    top15_df=helper.most_successful_countrywise(df,chosen_country)
    st.table(top15_df)