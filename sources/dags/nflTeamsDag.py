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
        'retry_delay': timedelta(minutes=1),
    },
    description='ETL workflow for NFL team data',
    schedule_interval='0 0 * * 1,2,5',
    start_date=days_ago(1),
    catchup=False,
    tags=['etl'],
)
def nfl_team_etl():
    import pandas as pd
    @task()
    def extract():
        from nfl_stuff.helper_functions.extractTeams import main as extract_main
        print("Extracting data...")
        return extract_main()

    @task()
    def transform():
        from nfl_stuff.helper_functions.transformTeams import main as transform_main
        print("Transforming data...")
        return transform_main()

    @task()
    def load():
        from nfl_stuff.helper_functions.loadTeams import main as load_main
        print("Loading data...")
        load_main()
        return "Database upload successful"
    extract()
    transform()
    load()

team_dag = nfl_team_etl()