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
    description='ETL workflow for NFL player data',
    schedule_interval='0 0 * * 1,2,5',
    start_date=days_ago(1),
    catchup=False,
    tags=['etl'],
)
def nfl_player_etl():
    @task()
    def extract():
        from nfl_stuff.helper_functions.extractPlayers import main as extract_main
        print("Extracting data...")
        return extract_main()

    @task()
    def clean():
        from nfl_stuff.helper_functions.cleanPlayers import main as clean_main
        print("Cleaning data...")
        return clean_main()

    @task()
    def loadBasic():
        from nfl_stuff.helper_functions import databaseModels
        from nfl_stuff.helper_functions.loadBasicPlayers import main as load_basic
        print("Loading basic data...")
        load_basic()
        return "Database upload successful"
    
    @task()
    def transform():
        from nfl_stuff.helper_functions import databaseModels
        from nfl_stuff.helper_functions.transformPlayers import main as transform_main
        print("Transforming data...")
        transform_main()
        return "Transformation successful"
    
    @task()
    def loadTransformed():
        from nfl_stuff.helper_functions import databaseModels
        from nfl_stuff.helper_functions.loadTransformedPlayers import main as load_transformed
        print("Loading transformed data...")
        load_transformed()
        return "Database upload successful"

    # define tasks
    extract_task = extract()
    clean_task = clean()
    load_basic_task = loadBasic()
    transform_task = transform()
    load_transformed_task = loadTransformed()

    # set the order of tasks
    extract_task >> clean_task >> load_basic_task >> transform_task >> load_transformed_task

player_dag = nfl_player_etl()