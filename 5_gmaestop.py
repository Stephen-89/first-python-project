import csv
import statistics
import matplotlib.pyplot as plt

# Define the GameStop class
class GameStop:
    def __init__(self, name, brand, rating, average_rating):
        self.name = name
        self.brand = brand
        self.rating = float(rating)  # Ensure rating is a float
        self.average_rating = float(average_rating)  # Ensure average_rating is a float

    def to_dict(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'rating': self.rating,
            'average_rating': self.average_rating
        }

# Function to load CSV data and create GameStop instances
def load_game_stop_data(csv_file):
    game_stop_data = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_stop = GameStop(
                name=row['name'],
                brand=row['brand'],
                rating=row['rating'],
                average_rating=row['average_rating']
            )
            game_stop_data.append(game_stop)
    return game_stop_data

# Function to calculate statistics for ratings and average ratings
def calculate_statistics(game_stop_data):
    
    ratings = [game_stop.rating for game_stop in game_stop_data]
    average_ratings = [game_stop.average_rating for game_stop in game_stop_data]
    
    # Calculate mean, median, and mode for ratings
    stats = {}
    
    for data, label in zip([ratings, average_ratings], ["rating", "average_rating"]):
        
        try:
            
            stats[label] = {
                'mean': statistics.mean(data),
                'median': statistics.median(data),
                'mode': statistics.mode(data),
                'std_dev': statistics.stdev(data)
            }
            
        except statistics.StatisticsError as e:
            
            # Handle case where no unique mode is found or other statistics errors
            stats[label] = {
                'mean': statistics.mean(data),
                'median': statistics.median(data),
                'mode': 'No unique mode' if 'no mode' in str(e) else str(e),
                'std_dev': 'Insufficient data' if 'variance' in str(e) else str(e)
            }
    
    return stats

# Load GameStop data from CSV file
csv_file = './data/gamestop_product_reviews_dataset_sample.csv'
game_stop_data = load_game_stop_data(csv_file)

# Calculate statistics
stats = calculate_statistics(game_stop_data)

# Print the results
for category, values in stats.items():
    print(f"Statistics for {category}:")
    print(f"  Mean: {values['mean']}")
    print(f"  Median: {values['median']}")
    print(f"  Mode: {values['mode']}")

# Function to plot the statistics
def plot_statistics(stats):
    categories = ['rating', 'average_rating']
    
    for category in categories:
        values = stats[category]
        labels = ['Mean', 'Median', 'Mode']
        means = [values['mean']]
        medians = [values['median']]
        modes = [values['mode']] if isinstance(values['mode'], (int, float)) else [0]  # Handle no unique mode

        # Plotting the data
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(labels, means + medians + modes, color=['blue', 'orange', 'green'])
        ax.set_ylabel('Value')
        ax.set_title(f'Statistics for {category.capitalize()}')
        ax.set_ylim(0, max(means + medians + modes) * 1.1)
        for i, value in enumerate(means + medians + modes):
            ax.text(i, value + 0.05 * max(means + medians + modes), f'{value}', ha='center')

        plt.show()
        
        
# Function to plot the statistics including standard deviation
def plot_statistics(stats):
    
    categories = ['rating', 'average_rating']
    
    for category in categories:
        
        values = stats[category]
        labels = ['Mean', 'Median', 'Standard Deviation']
        
        mean_value = values['mean']
        median_value = values['median']
        std_dev_value = values['std_dev']
        
        # Handling non-numeric values
        std_dev_value = std_dev_value if isinstance(std_dev_value, (int, float)) else 0
        mean_value = mean_value if isinstance(mean_value, (int, float)) else 0
        median_value = median_value if isinstance(median_value, (int, float)) else 0
        
        # Plotting the data
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(labels, [mean_value, median_value, std_dev_value], color=['blue', 'orange', 'green'])
        ax.set_ylabel('Value')
        ax.set_title(f'Statistics for {category.capitalize()}')
        ax.set_ylim(0, max(mean_value, median_value, std_dev_value) * 1.1)
        for i, value in enumerate([mean_value, median_value, std_dev_value]):
            ax.text(i, value + 0.05 * max(mean_value, median_value, std_dev_value), f'{value:.2f}', ha='center')

        plt.show()

plot_statistics(stats)

