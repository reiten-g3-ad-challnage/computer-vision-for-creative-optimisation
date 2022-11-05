from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2


class Persistence:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/airflow", echo=True)
        self.dominat_color_schema = "/opt/airflow/dags/scripts/schema/dominant_colors.sql"
        self.edge_schema = "/opt/airflow/dags/scripts/schema/edge.sql"
        self.face_emotions_schema = "/opt/airflow/dags/scripts/schema/face_emotions.sql"
        self.logo_schema = "/opt/airflow/dags/scripts/schema/logo.sql"
        self.object_count_schema = "/opt/airflow/dags/scripts/schema/object_count.sql"
        self.performance_schema = "/opt/airflow/dags/scripts/schema/performance.sql"

    def create_table(self):
        """
        Create tables of each schema
        """
        schemas = [self.dominat_color_schema, self.edge_schema, self.face_emotions_schema, self.logo_schema,
        self.object_count_schema, self.performance_schema]
        try:
            with self.engine.connect() as conn:
                for name in schemas:
                    with open(f'{name}') as file:
                        query = text(file.read())
                        conn.execute(query)
        except Exception as e:
            print(e)

    def insert_data(self, tablename, raw_df, table_schema):
        """convert dataframe to sql data
        Args:
            raw_df: The dataframe
            tablename: The database table name
        """
        table_schema = open(table_schema)
        try:
            with self.engine.connect() as conn:
                raw_df.to_sql(name=tablename, con=conn,if_exists='replace')
        except Exception as e:
            print(f"Failed  ---- {e}") 

