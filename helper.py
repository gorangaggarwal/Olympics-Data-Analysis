import numpy as np

def medal_tally(olympics_df):

    medal_tally = olympics_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(olympics_df):

    years = olympics_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(olympics_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def fetch_medal_tally(olympics_df, year, country):
    medal_df = olympics_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        X = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        X = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    X['Total'] = X['Gold'] + X['Silver'] + X['Bronze']

    return X

def data_over_time(olympics_df,col):

    nations_over_time = olympics_df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values(['Year'])

    return nations_over_time

def most_successful(olympics_df,sport):

    medal_players = olympics_df[olympics_df["Medal"].notna()]

    if sport != 'Overall':
        medal_players = medal_players[medal_players['Sport'] == sport]

    x = medal_players['Name'].value_counts().reset_index().head(10).merge(olympics_df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)

    return x

def yearwise_medal_tally(olympics_df, country):

    medal_players = olympics_df[olympics_df["Medal"].notna()]
    medal_players = medal_players.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = medal_players[medal_players['region'] == country]

    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(olympics_df,country):

    medal_players = olympics_df[olympics_df["Medal"].notna()]
    medal_players = medal_players.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = medal_players[medal_players['region'] == country]

    return new_df

def most_successful_countrywise(olympics_df,country):

    medal_players = olympics_df[olympics_df["Medal"].notna()]
    medal_players = medal_players[medal_players['region'] == country]

    x = medal_players['Name'].value_counts().reset_index().head(10).merge(olympics_df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)

    return x

def weight_vs_height(olympics_df,sport):

    athlete_df = olympics_df.drop_duplicates(subset=['Name','region'])
    athlete_df["Medal"].fillna('No Medal', inplace=False)

    if sport != 'Overall':
        temp_df = olympics_df[olympics_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(olympics_df):

    athlete_df = olympics_df.drop_duplicates(subset=['Name','region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final