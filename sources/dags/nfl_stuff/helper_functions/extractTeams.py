"""
This module provides functions for scraping nfl team defensive data to add to database.
"""
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import io

# scrape team defensive data with year specified in the function
def scrape_team_data() -> pd.DataFrame:
    year = 2024
    teams = ['crd', 'atl', 'buf', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'clt', 'kan', 'rai', 'sea', 'tam', 'rav',
            'car', 'jax', 'sdg', 'ram', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'phi', 'pit', 'sfo', 'oti', 'was', 'htx']
    all_teams = pd.DataFrame()
    for team in teams:
        url = "https://www.pro-football-reference.com/teams/" + team + "/" + str(year) + "/gamelog/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        time.sleep(3)
        try:
            string = "gamelog_opp" + str(year)
            table = soup.find("table", {"id": string})
            df = pd.read_html(io.StringIO(str(table)))[0]
        except:
            print(url)
            raise RuntimeError("What the fuck")
        # cleaning data
        col1 = {}
        col2 = {}
        df.drop(columns=("Unnamed: 3_level_0", "Unnamed: 3_level_1"), axis=1, inplace=True)
        df.rename(columns={"Unnamed: 4_level_1": "Result"}, level=1, inplace=True)
        for i in df.columns:
            if "Unnamed:" in i[0]:
                col1[i[0]] = 'Game Info'
            if "Unnamed:" in i[1]:
                col2[i[1]] = 'H/A'
        df.rename(columns=col1, level=0, inplace=True)
        df.rename(columns=col2, level=1, inplace=True)
        df.loc[:, ('Game Info', 'H/A')] = [0 if i == "@" else 1 for i in df['Game Info']['H/A']]
        df.loc[:, ('Game Info', 'OT')] = [int(0) if pd.isnull(i) else int(1) for i in df['Game Info']['OT']]
        df[('Game Info', 'Tm')] = team
        df[('Game Info', 'szn')] = year
        months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 
            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        df.loc[:, ('Game Info', 'Date')] = [str(year+1) + '-' + str(months_dict.get(i.split(" ")[0])) + '-' + i.split(" ")[1] if months_dict.get(i.split(" ")[0])<3 else str(year) + '-' + str(months_dict.get(i.split(" ")[0])) + '-' + i.split(" ")[1] for i in df['Game Info']['Date']]
        all_teams = pd.concat([all_teams, df])
    all_teams.reset_index(drop=True, inplace=True)
    return all_teams

def main() -> pd.DataFrame:
    team_data = scrape_team_data()
    team_data.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/team_data.csv")
