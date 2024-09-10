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
    def clean():
        from nfl_stuff.helper_functions.cleanTeams import main as clean_main
        print("Cleaning data...")
        return clean_main()

    @task()
    def loadBasic():
        from nfl_stuff.helper_functions.loadBasicTeams import main as load_basic
        print("Loading basic data...")
        load_basic()
        return "Database upload 1/2 successful"
    
    @task()
    def transform():
        from nfl_stuff.helper_functions.cleanTeams import main as transform_main
        print("Transforming data...")
        transform_main()
        return "Transformation successful"
    
    @task()
    def loadTransformed():
        from nfl_stuff.helper_functions.loadTransformedTeams import main as load_transformed
        print("Loading transformed data...")
        load_transformed()
        return "Database upload 2/2 successful"
    extract()
    clean()
    loadBasic()
    transform()
    loadTransformed

team_dag = nfl_team_etl()