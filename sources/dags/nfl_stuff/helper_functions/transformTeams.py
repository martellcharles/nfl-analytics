import pandas as pd
import numpy as np
from databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os

def calculate_averages_per(stat1: pd.Series, stat2: pd.Series, percentage: bool) -> list:
    new_avg = []
    stat1_total = stat1.iloc[0]
    stat2_total = stat2.iloc[0]
    for i in range(1,len(stat1)):
        if stat2_total == 0:
            new_avg.append(0)
        else:
            if percentage:
                new_avg.append(round(stat1_total / stat2_total * 100,2))
            else:
                new_avg.append(round(stat1_total / stat2_total,2))
        stat1_total += stat1.iloc[i]
        stat2_total += stat2.iloc[i]
    return new_avg

def calculate_career_rate(completions: pd.Series, attempts: pd.Series, yards: pd.Series, tds: pd.Series, ints: pd.Series) -> list:
    new_avg = []
    cmp_total = completions.iloc[0]
    att_total = attempts.iloc[0]
    yds_total = yards.iloc[0]
    tds_total = tds.iloc[0]
    ints_total = ints.iloc[0]
    for i in range(1,len(completions)):
        if att_total == 0:
            new_avg.append(0)
        else:
            a = ((cmp_total/att_total) - 0.3) * 5
            b = ((yds_total/att_total) - 3) * 0.25
            c = (tds_total/att_total) * 20
            d = 2.375 - ((ints_total/att_total) * 25)
            rate = round(((a+b+c+d)/6) * 100, 2)
            new_avg.append(rate)
        cmp_total += completions.iloc[i]
        att_total += attempts.iloc[i]
        yds_total += yards.iloc[i]
        tds_total += tds.iloc[i]
        ints_total += ints.iloc[i]
    return new_avg

def calculate_net_yds_att(pass_yds: pd.Series, sack_yds: pd.Series, passing_att: pd.Series, sacks: pd.Series) -> list:
    new_avg = []
    pass_yds_total = pass_yds.iloc[0]
    sack_yds_total = sack_yds.iloc[0]
    att_total = passing_att.iloc[0]
    sack_total = sacks.iloc[0]
    for i in range(1,len(pass_yds)):
        if att_total+sack_total==0:
            new_avg.append(0)
        else:
            net_yds_att = round((pass_yds_total - sack_yds_total)/(att_total + sack_total), 2)
            new_avg.append(net_yds_att)
        pass_yds_total += pass_yds.iloc[i]
        sack_yds_total += sack_yds.iloc[i]
        att_total += passing_att.iloc[i]
        sack_total += sacks.iloc[i]
    return new_avg

def create_team_avg_df(team_stats: pd.DataFrame, season: int) -> None:
    all_team_avgs = pd.DataFrame()
    for team in team_stats['team'].unique():
        df = team_stats.loc[(team_stats['team'] == team) & (df_all_years['szn'] == season), :]
        avgs = pd.DataFrame()
        for col in df.columns:
            if col in ['game_id', 'szn', 'date', 'team']:
                avgs[col] = df[col][1:]
                continue
            if col == 'passing_cmp_prc':
                avgs[col] = calculate_averages_per(stat1=df['passing_cmp'], stat2=df['passing_att'], percentage=True)
            elif col == 'passing_yds_att':
                avgs[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'rushing_yds_att':
                avgs[col] = calculate_averages_per(stat1=df['rushing_yds'], stat2=df['rushing_att'], percentage=False)
            elif col == 'passing_rate':
                avgs[col] = calculate_career_rate(df['passing_cmp'], df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col == 'passing_net_yds_att':
                avgs[col] = calculate_net_yds_att(df['passing_yds'], df['passing_sack_yds_lost'], df['passing_att'], df['passing_sacks'])
            elif col == 'third_down_conv':
                avgs[col] = calculate_averages_per(stat1=df['third_down_conv'], stat2=df['third_down_att'], percentage=True)
            elif col == 'fourth_down_conv':
                avgs[col] = calculate_averages_per(stat1=df['fourth_down_conv'], stat2=df['fourth_down_att'], percentage=True)
            elif col in ['third_down_att', 'fourth_down_att']:
                continue
                # combining conversion and attempts into average conversion rate
            else:
                idx = 1
                total = df[col].iloc[0]
                avg_col = []
                for i in df[col][1:]:
                    new_avg = round(total / idx,2)
                    avg_col.append(new_avg)
                    total += i
                    idx += 1
                avgs[col] = avg_col
        all_team_avgs = pd.concat([all_team_avgs, avgs])
    all_team_avgs.reset_index(drop=True, inplace=True)
    all_team_avgs.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/team_avgs.csv")

def main() -> None:
    season = os.environ.get("NFL_SEASON")
    # connect to database to load team_stats
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        team_stats = pd.read_sql_query(session.query(TeamStats).statement, engine)
    create_team_avg_df(team_stats, season)
    