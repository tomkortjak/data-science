from sqlalchemy import create_engine
import pandas as pd


# relative path

engine = create_engine('sqlite:///zipcode.db')

df=pd.read_csv('population.csv', sep=',')

df.head()

df.to_sql(name='population',con=engine,if_exists='fail',index=False) 
