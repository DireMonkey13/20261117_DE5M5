#Imports

import pandas as pd
#from sqlalchemy import create_engine, URL, text
import urllib
import argparse
import time

#Parser

parser=argparse.ArgumentParser()
parser.add_argument("path",help="The path to the folder containing the input files")
args=parser.parse_args()
print("Directory path set to: " + args.path)

#Set variables

filedirectory=args.path
bookfile="03_Library Systembook.csv"
customersfile="03_Library SystemCustomers.csv"


#Functions

def missing_values(row):
    return row.isna().any()

def remove_quotes(value):
    return value.replace('"','')

def date_difference(df,datecol1,datecol2,newcol):
    start = pd.to_datetime(df[datecol1], format="%d/%m/%Y")
    end = pd.to_datetime(df[datecol2], format="%d/%m/%Y")
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

book_start_time = time.perf_counter()

# Load the original CSV
#df_original = pd.read_csv( r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library Systembook.csv")

df_original = pd.read_csv( filedirectory + bookfile )
book_input_rows = len(df_original)

# Create a copy to use for data cleaning

df_clean = df_original.copy()

# Drop rows where all values are null
book_before_blank_drop = len(df_clean)
df_clean=df_clean.dropna(how="all").reset_index(drop=True)
book_blank_rows = book_before_blank_drop - len(df_clean)

#CLEAN DATES - REMOVE QUOTES AND SET INVALID TO NULL
df_clean["Book checkout"] = df_clean["Book checkout"].str.replace('"','',regex=False)
df_clean["Book checkout"] = pd.to_datetime( df_clean["Book checkout"],format="%d/%m/%Y",errors="coerce")
df_clean["Book Returned"] = pd.to_datetime( df_clean["Book Returned"],format="%d/%m/%Y",errors="coerce")

invalid_check = df_clean.apply(missing_values,axis=1)

book_null_rejected = invalid_check.sum()

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
book_negative_rejected = negative_days.sum()
df_invalid = pd.concat( [df_invalid, df_clean[negative_days]], ignore_index=True)
df_clean = df_clean[~negative_days].reset_index(drop=True)

#df_clean.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_Systembook_Cleaned.csv", index=False)
#df_invalid.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_Systembook_Invalid.csv", index=False)

df_clean.to_csv( filedirectory+"Cleaned_"+bookfile, index = False)
df_invalid.to_csv( filedirectory+"Invalid_"+bookfile, index = False)

book_clean_rows = len(df_clean)
book_invalid_rows = len(df_invalid)

book_end_time = time.perf_counter()
book_processing_time = book_end_time - book_start_time

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

customer_start_time = time.perf_counter()

# Load the original CSV
#df_original = pd.read_csv( r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library SystemCustomers.csv")

df_original = pd.read_csv( filedirectory + customersfile )
customer_input_rows = len(df_original)

# Create a copy to use for data cleaning
df_clean = df_original.copy()

# Things to clean:
# Null values

# Output rows with n/a records to the invalid file
customer_before_blank_drop = len(df_clean)
df_clean=df_clean.dropna(how="all").reset_index(drop=True)
customer_blank_rows = customer_before_blank_drop - len(df_clean)

invalid_check = df_clean.apply(missing_values,axis=1)
customer_null_rejected = invalid_check.sum()

df_invalid = df_clean[invalid_check].copy()
df_clean = df_clean[~invalid_check].copy()

df_invalid.reset_index(drop=True,inplace=True)
df_clean.reset_index(drop=True,inplace=True)

#Convert IDs back to integer
df_clean["Customer ID"] = df_clean["Customer ID"].astype(int)

#df_clean.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_SystemCustomers_Cleaned.csv", index=False)
#df_invalid.to_csv(r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library_SystemCustomers_Invalid.csv", index=False)

df_clean.to_csv( filedirectory+"Cleaned_"+customersfile, index = False)
df_invalid.to_csv( filedirectory+"Invalid_"+customersfile, index = False)

customer_clean_rows = len(df_clean)
customer_invalid_rows = len(df_invalid)

customer_end_time = time.perf_counter()
customer_processing_time = customer_end_time - customer_start_time

################################
################################

### OUTPUT METRICS

################################
################################



metrics = pd.DataFrame([
    { 
        "File" : bookfile,
        "Input Rows" : book_input_rows,
        "Cleaned Rows" : book_clean_rows,
        "Invalid Rows" : book_invalid_rows,
        "Blank Rows Dropped" : book_blank_rows,
        "Rejected Null/Invalid" : book_null_rejected,
        "Rejected Negative Days" : book_negative_rejected,
        "Processing Time Seconds": round(book_processing_time,3)
        
    },

    {
        "File" : customersfile,
        "Input Rows" : customer_input_rows,
        "Cleaned Rows" : customer_clean_rows,
        "Invalid Rows" : customer_invalid_rows,
        "Blank Rows Dropped" : customer_blank_rows,
        "Rejected Null/Invalid" : customer_null_rejected,
        "Rejected Negative Days" : 0,
        "Processing Time Seconds": round(customer_processing_time,3)
    }
])

metrics.to_csv( filedirectory + "Processing_Metrics.csv", index=False)

################################
################################

### END OF LINE