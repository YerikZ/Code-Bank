
from sqlalchemy import create_engine
import pandas.io.sql as sql
from sqlalchemy import types

# connection
engine = create_engine('postgresql://postgres:101010@localhost:5432/postgres')

multi = pd.read_sql_query("select * from ct_db.tbl_multibuy_orders_shoes_size", con=engine)
