# https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html

# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://odepj:8piJSuhIb.CMTL$O@oege.ie.hva.nl/zodepj')


df = pd.read_sql("SELECT * FROM test", con=engine)

df.head()






