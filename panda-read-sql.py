# %%
import pyodbc
import pandas as pd
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'localhost'
database = 'omega_dev'
username = 'admin_all'
password = 'admin_all'
driver_linux = 'ODBC Driver 17 for SQL Server'
cnxn = pyodbc.connect('DRIVER=' + driver_linux + ';SERVER=' + server +
                      ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# Windows "Driver=SQL Server;Server=.;Database=nameOfDatabase;Trusted_Connection=Yes;"
# Linux
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "select * from admin_all.COUNTRY;"
df = pd.read_sql(query, cnxn)
df.head(26)

# %%
