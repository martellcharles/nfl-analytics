from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

@dag(
    default_args={
        'owner': 'charlie',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,   
        'retry_delay': timedelta(minutes=5),
    },
    description='ETL workflow for NFL data',
    schedule_interval='0 0 * * 1,2,5',
    start_date=days_ago(1),
    catchup=False,
    tags=['etl'],
)
def player_etl_workflow():
    import pandas as pd
    @task()
    def extract():
        from sources.dags.extractPlayers import main as extract_main
        print("Extracting data...")
        return extract_main()

    @task()
    def transform(games: pd.DataFrame, teams: pd.DataFrame):
        from sources.dags.transformPlayers import main as transform_main
        print("Transforming data...")
        return transform_main(games, teams)

    @task()
    def load(t_games: pd.DataFrame, t_teams: pd.DataFrame):
        from sources.dags.loadPlayers import main as load_main
        print("Loading data...")
        load_main(t_games, t_teams)
        return "Database upload successful"
    games = extract()
    transformed_games = transform(games)
    load(transformed_games)

player_dag = player_etl_workflow()