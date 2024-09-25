import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load sample dataset
tips = sns.load_dataset("tips")

# Create a seaborn boxplot
sns.boxplot(x="day", y="total_bill", data=tips)

# Show plot
plt.title("Boxplot of Total Bill by Day")
plt.show()