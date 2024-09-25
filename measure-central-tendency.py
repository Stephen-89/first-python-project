from flask import Flask
from pathlib import Path
import statistics
import pandas as pd

app = Flask(__name__)

file_path = Path('./data/Fortune500.csv')
df = pd.read_csv(file_path)

data = df['REVENUES']

# Mean
mean_value = statistics.mean(data)
# Median
median_value = statistics.median(data)
# Mode
mode_value = statistics.mode(data)
# Std
std_value = statistics.stdev(data)

print(f"Mean: {mean_value}")
print(f"Median: {median_value}")
print(f"Mode: {mode_value}")
print(f"Std: {std_value}")
#print(f"Data: {data}")