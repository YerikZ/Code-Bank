
from sqlalchemy import create_engine
import pandas.io.sql as sql
from sqlalchemy import types

# connection
engine = create_engine('postgresql://postgres:{password}@localhost:5432/postgres')

multi = pd.read_sql_query("select * from schema.table_name", con=engine)
