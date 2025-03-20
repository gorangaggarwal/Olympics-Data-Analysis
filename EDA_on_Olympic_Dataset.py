import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

def missing_values_analysis(olympics_df):
    na_columns_ = [col for col in olympics_df.columns if olympics_df[col].isnull().sum() > 0]
    n_miss = olympics_df[na_columns_].isnull().sum().sort_values(ascending=True)
    ratio_ = (olympics_df[na_columns_].isnull().sum() / olympics_df.shape[0] * 100).sort_values(ascending=True)
    missing_df = pd.concat([n_miss, np.round(ratio_, 2)], axis=1, keys=['Total Missing Values', 'Ratio'])
    missing_df = pd.DataFrame(missing_df)
    return missing_df

def check_df(olympics_df):
    print("--------------------- Shape --------------------")
    print(olympics_df.shape)
    print("-------------------- Types ---------------------")
    print(olympics_df.dtypes)
    print("----------------- NaN Analysis -----------------")
    print(missing_values_analysis(olympics_df))

    sns.pairplot(olympics)
    plt.figure(figsize=(18, 8))
    sns.set(style='whitegrid', )
    sns.distplot(olympics["Age"], color="purple")
    plt.xlabel("Age of the players", fontsize=14, weight="semibold")
    plt.ylabel("Density", fontsize=15, weight="semibold")
    plt.show()
    sns.set(style='ticks', )
    sns.displot(olympics, x="Age", hue="Sex",
                alpha=0.5,
                binwidth=2,
                height=8, aspect=2)
    plt.xlabel("Age of the players", fontsize=14, weight="semibold")
    plt.ylabel("Density", fontsize=15, weight="semibold")
    plt.figure(figsize=(24, 20))
    sns.set(style="whitegrid", )
    sns.boxplot(data=olympics, x="Age", y="Height")
    plt.xticks(rotation=45, weight="semibold")
    plt.yticks(weight="semibold", fontsize=13)
    plt.xlabel("Age of the players", fontsize=14, weight="semibold")
    plt.ylabel("Height in centimeters", fontsize=15, weight="semibold")
    plt.show()
    medal_players = olympics[olympics["Medal"].notna()]
    medal_players
    fig = px.histogram(medal_players, x="Medal", color="Sex",
                       barmode='group', title='Total medals with respect to gender',
                       color_discrete_map={"M": "RebeccaPurple", "F": "MediumPurple"},
                       template='simple_white', opacity=1
                       )
    fig.show()
    px.histogram(medal_players, x="Team", color="Medal",
                 barmode="group")
    medal_players["Medal_Count"] = medal_players.groupby("Medal")["Medal"].transform('count')
    df = medal_players.query("Medal_Count > 250")
    df.info()
