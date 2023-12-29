import numpy as np
import pandas as pd

# folder = "./outputs/"

# excel_file = "R:\PROJECTS\PYTHON\WEB_PARSER\outputs\Competitors-rates-06-12-2023-15_03.xlsx"

# rates_file = "./rates.xlsx"
# matches_file = "./matches_table.xlsx"

# df = pd.read_excel(folder + "Competitors-rates-06-12-2023-15_03.xlsx", sheet_name=2)

#print(df)
#print(df.head(10))
#print(df.describe())

#rates_df_old = pd.read_excel(rates_file, "old")
# rates_df_new = pd.read_excel(rates_file, "new")

# rates_lim = rates_df_new.iloc[15:23,0:18]
# print(rates_lim.head(30))
# print(rates_lim.describe())

rates = ["r1", "r2", "r3"]

df = pd.DataFrame(
    {
        "x": [2, 3, 4],
        "y": [3, 1, 7]
    },
    index = rates
)

df["deviation"] = 100 * (1 - df["x"] / df["y"])

print(df)

arr = df["deviation"].to_numpy()

print(arr)

new_arr = np.where(arr>0, ">0", "<=0")

print(new_arr)