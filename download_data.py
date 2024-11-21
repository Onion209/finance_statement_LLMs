import os
import shutil
import kagglehub
import pandas as pd
# Download latest version
path = kagglehub.dataset_download("rish59/financial-statements-of-major-companies2009-2023")
# print("Files in the directory:", os.listdir(path))
# Specify the correct CSV file path
file_path = os.path.join(path, "Financial Statements.csv")
# Copy the file to a new location
destination_path = "/home/minhlahanhne/finance_statement_LLMs/Financial Statements.csv"
shutil.copy(file_path, destination_path)

# Read the CSV file
df = pd.read_csv(file_path)
print(df.info())