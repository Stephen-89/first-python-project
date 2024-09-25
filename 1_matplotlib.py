import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Sample data
data = [12, 15, 12, 14, 19, 12, 15, 17, 16, 19, 21, 15, 14, 16, 18, 19, 15, 17, 12, 14]

# Calculate Mean, Median, Mode
mean = np.mean(data)
median = np.median(data)
mode = stats.mode(data)[0][0]

# Plot histogram of the data
plt.hist(data, bins=5, color='lightblue', edgecolor='black')

# Plot mean, median, mode as vertical lines
plt.axvline(mean, color='r', linestyle='--', label=f'Mean: {mean:.2f}')
plt.axvline(median, color='g', linestyle='-', label=f'Median: {median}')
plt.axvline(mode, color='b', linestyle='-.', label=f'Mode: {mode}')

# Adding labels and title
plt.title('Histogram with Mean, Median, Mode')
plt.xlabel('Data Values')
plt.ylabel('Frequency')

# Add legend
plt.legend()

# Show plot
plt.show()