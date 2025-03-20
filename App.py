import streamlit as st
import pandas as pd
import numpy as np
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import plotly.figure_factory as ff

olympics_df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

olympics_df = preprocessor.preprocess(olympics_df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('C:/Users/PURTI/Desktop/gorang/Project/Olympic Data Analysis/Other-Research-guide-Olympic-games.jpg')
user_menu=st.sidebar.radio('Select an Option',('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))

if user_menu == 'Medal Tally':

    st.sidebar.header('Medal Tally')

    years,country = helper.country_year_list(olympics_df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)

    medal_tally = helper.fetch_medal_tally(olympics_df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s"+ " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s" + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    editions = olympics_df['Year'].unique().shape[0] - 1
    cities = olympics_df['City'].unique().shape[0]
    sports = olympics_df['Sport'].unique().shape[0]
    events = olympics_df['Event'].unique().shape[0]
    athletes = olympics_df['Name'].unique().shape[0]
    nations = olympics_df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(olympics_df,'region')
    nations_over_time.rename(columns={'count': 'No. of Countries'}, inplace=True)
    fig = px.line(nations_over_time,x='Year',y='No. of Countries')
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(olympics_df,'Event')
    events_over_time.rename(columns={'count': 'No. of Events'}, inplace=True)
    fig = px.line(events_over_time,x='Year',y='No. of Events')
    st.title('Events Over the Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(olympics_df,'Name')
    athletes_over_time.rename(columns={'count': 'No. of Athletes'}, inplace=True)
    fig = px.line(athletes_over_time,x='Year',y='No. of Athletes')
    st.title('Athletes Over the Years')
    st.plotly_chart(fig)

    st.title('No. of Events Over Time for Every Sports')
    fig,ax = plt.subplots(figsize=(20,20))
    x = olympics_df.drop_duplicates(['Year','Sport','Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = olympics_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(olympics_df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = np.unique(olympics_df['region'].dropna().values).tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(olympics_df, selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country + "'s " + 'Medal Tally Over the Years')
    st.plotly_chart(fig)

    st.title(selected_country + "'s " + 'Excel in the Following Sports')
    new_df = helper.country_event_heatmap(olympics_df, selected_country)
    fig,ax  = plt.subplots(figsize=(20, 20))
    sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes of ' + selected_country)
    athlete_df = helper.most_successful_countrywise(olympics_df, selected_country)
    st.table(athlete_df)

if user_menu == 'Athlete-wise Analysis':

    athlete_df = olympics_df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Age of Gold Medalist', 'Age of Silver Medalist','Age of Bronze Medalist'], show_hist=False, show_rug=False)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x =[]
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title("Distribution of Age wrt Sports(Silver Medalist)")
    st.plotly_chart(fig)

    sport_list = olympics_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(olympics_df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df,x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'])
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(olympics_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)