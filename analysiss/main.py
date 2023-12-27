import numpy as np
import pandas as pd

folder = "./outputs/"

excel_file = "R:\PROJECTS\PYTHON\WEB_PARSER\outputs\Competitors-rates-06-12-2023-15_03.xlsx"

rates_file = "./rates.xlsx"
matches_file = "./matches_table.xlsx"

df = pd.read_excel(folder + "Competitors-rates-06-12-2023-15_03.xlsx", sheet_name=2)

#print(df)
#print(df.head(10))
#print(df.describe())

#rates_df_old = pd.read_excel(rates_file, "old")
rates_df_new = pd.read_excel(rates_file, "new")

rates_lim = rates_df_new.iloc[15:23,0:18]
print(rates_lim.head(30))
print(rates_lim.describe())