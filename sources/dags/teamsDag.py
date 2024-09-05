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
def team_etl_workflow():
    import pandas as pd
    @task()
    def extract():
        from sources.dags.extractTeams import main as extract_main
        print("Extracting data...")
        return extract_main()

    @task()
    def transform(teams: pd.DataFrame):
        from sources.dags.transformTeams import main as transform_main
        print("Transforming data...")
        return transform_main(teams)

    @task()
    def load(transformed_teams: pd.DataFrame):
        from sources.dags.loadTeams import main as load_main
        print("Loading data...")
        load_main(transformed_teams)
        return "Database upload successful"
    teams = extract()
    transformed_teams = transform(teams)
    load(transformed_teams)

team_dag = team_etl_workflow()