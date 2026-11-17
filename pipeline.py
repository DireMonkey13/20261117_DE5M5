#Imports

import pandas as pd

# Load the original CSV
df_original = pd.read_csv( r"C:\Users\Admin\Desktop\20261117_DE5M5\data\03_Library Systembook.csv")

# Create a copy to use for data cleaning
df_clean = df_original.copy()

# Drop rows where all values are null

df_clean=df_clean.dropna(how="all").reset_index(drop=True)

# Output rows with n/a records to the invalid file

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


#if __name__ == "__main__":
    
    # Main capability triggered IF this is run as an executable.

################################
################################

### BOOK

################################
################################

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