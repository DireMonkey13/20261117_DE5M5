#Imports

import pandas as pd
from sqlalchemy import create_engine, URL, text
import urllib



#Functions

def missing_values(row):
    return row.isna().any()

def remove_quotes(value):
    return value.replace('"','')

def date_difference(df,datecol1,datecol2,newcol):
    start = pd.to_datetime(df[datecol1])
    end = pd.to_datetime(df[datecol2])
    difference = end - start
    df[newcol] = difference.dt.days
    return df

#def output_to_sql(dataframe, table_name):
#    dataframe.to_sql(
#        name=table_name,
#        con=engine,
#        schema=dbo,
#        if_exists="append"
#        index=false
#    )

# Setup SQL Connection

#connection_string = (
#    "DRIVER={ODBC Driver 18 for SQL Server};"
#    "SERVER=localhost;"
#    "DATABASE=LibrarySystem;"
#    "Trusted_Connection=yes;"
#    "TrustServerCertificate=yes;"
#)
#connection_url = urllib.parse.quote_plus(connection_string)
#engine = create_engine(
#    f"mssql+pyodbc:///?odbc_connect={connection_url}"
#)

#server = 'localhost'
#database = 'LibrarySystem'
#driver = 'ODBC Driver 17 for SQL Server'

#connection_url= URL.create(
#    "mssql+pyodbc",
#    host=server,
#    database=database,
#    query={
#        "driver": driver,
#        "Trusted_Connection":"yes",
#        "TrustServerCertificate":"yes",
#    },
#)

#engine = create_engine(connection_url)

################################
################################

### BOOK

################################
################################

# Load the original CSV
df_original = pd.read_csv( r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library Systembook.csv")

# Create a copy to use for data cleaning
df_clean = df_original.copy()

# Drop rows where all values are null

df_clean=df_clean.dropna(how="all").reset_index(drop=True)

#CLEAN DATES - REMOVE QUOTES AND SET INVALID TO NULL
df_clean["Book checkout"] = df_clean["Book checkout"].str.replace('"','',regex=False)
df_clean["Book checkout"] = pd.to_datetime( df_clean["Book checkout"],format="%d/%m/%Y",errors="coerce")
df_clean["Book Returned"] = pd.to_datetime( df_clean["Book Returned"],format="%d/%m/%Y",errors="coerce")

invalid_check = df_clean.apply(missing_values,axis=1)

df_invalid = df_clean[invalid_check].copy()
df_clean = df_clean[~invalid_check].copy()

df_invalid.reset_index(drop=True,inplace=True)
df_clean.reset_index(drop=True,inplace=True)

# Replace "2 weeks" with 14

df_clean["Days allowed to borrow"] = (df_clean["Days allowed to borrow"].replace("2 weeks" , 14).astype(int))

#Convert IDs back to integer
df_clean["Id"] = df_clean["Id"].astype(int)
df_clean["Customer ID"] = df_clean["Customer ID"].astype(int)

df_clean = date_difference( df_clean, "Book checkout","Book Returned","Days Borrowed")

# Remove rows with negative days borrowed

negative_days = df_clean["Days Borrowed"] < 0
df_invalid = pd.concat( [df_invalid, df_clean[negative_days]], ignore_index=True)
df_clean = df_clean[~negative_days].reset_index(drop=True)


df_clean.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_Systembook_Cleaned.csv", index=False)
df_invalid.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_Systembook_Invalid.csv", index=False)

#output_to_sql(df_clean,"Systembook")
#output_to_sql(df_invalid,"Systembook_invalid")

#with engine.connect() as connection:
#    result= connection.execute(
#        text("TRUNCATE TABLE[Systembook]")
#    )
#with engine.begin() as sqlconn:
#    sqlconn.execute(text("TRUNCATE TABLE[Systembook_invalid]"))

#df_clean.to_sql(
#    name='Systembook',
#    con=engine,
#    if_exists='append',
#    index=False )

#df_invalid.to_sql(
#    name='Systembook_invalid',
#    con=engine,
#    if_exists='append',
#    index=False )

################################
################################

### CUSTOMERS

################################
################################

# Load the original CSV
df_original = pd.read_csv( r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library SystemCustomers.csv")

# Create a copy to use for data cleaning
df_clean = df_original.copy()

# Things to clean:
# Null values

# Output rows with n/a records to the invalid file

df_clean=df_clean.dropna(how="all").reset_index(drop=True)

invalid_check = df_clean.apply(missing_values,axis=1)

df_invalid = df_clean[invalid_check].copy()
df_clean = df_clean[~invalid_check].copy()

df_invalid.reset_index(drop=True,inplace=True)
df_clean.reset_index(drop=True,inplace=True)

#Convert IDs back to integer
df_clean["Customer ID"] = df_clean["Customer ID"].astype(int)

df_clean.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_SystemCustomers_Cleaned.csv", index=False)
df_invalid.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_SystemCustomers_Invalid.csv", index=False)