import os
import kagglehub
import pandas as pd
# Download latest version
path = kagglehub.dataset_download("rish59/financial-statements-of-major-companies2009-2023")
# print("Files in the directory:", os.listdir(path))
# Specify the correct CSV file path
file_path = os.path.join(path, "Financial Statements.csv")

# Read the CSV file
df = pd.read_csv(file_path)
# print(df.info())