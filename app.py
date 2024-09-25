from flask import Flask, jsonify, render_template
from pathlib import Path
import csv
import statistics
import matplotlib.pyplot as plt


app = Flask(__name__)

class HackerNews:
    def __init__(self, id, title, url, num_points, num_comments, author, created_at):
        self.id = id
        self.title = title
        self.url = url
        self.num_points = num_points
        self.num_comments = num_comments
        self.author = author
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'num_points': self.num_points,
            'num_comments': self.num_comments,
            'author': self.author,
            'created_at': self.created_at
        }

def all_hacker_news(file_path):
    
    news_list = []
    points_list = []

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Extract fields
                id = int(row.get('id', '0'))
                title = row.get('title', '')
                url = row.get('url', '')
                num_points = int(row.get('num_points', '0'))
                num_comments = int(row.get('num_comments', '0'))
                author = row.get('author', '')
                created_at = row.get('created_at', '')

                # Create HackerNews object
                post = HackerNews(id, title, url, num_points, num_comments, author, created_at)
                news_list.append(post)

                # Add num_points to the list
                points_list.append(num_points)
            
            except ValueError:
                continue

    return news_list, points_list

file_path = Path('./data/hacker_news.csv')
news_list, points_list = all_hacker_news(file_path)

def get_points_stats():
    
    mean_value = statistics.mean(points_list)
    median_value = statistics.median(points_list)
    mode_value = statistics.mode(points_list)
    std_value = statistics.stdev(points_list)
    
    return {
            'values': points_list,
            'mean': mean_value,
            'median': median_value,
            'mode': mode_value,
            'std': std_value
        }
    
def display_graph():
    
    # Get stats from the function
    stats = get_points_stats()
    
    # Plotting with Matplotlib
    # Create a figure with two subplots: one for stats and one for histogram
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    # Bar plot for mean, median, mode, std
    axs[0].bar(['Mean', 'Median', 'Mode', 'Std'], [stats['mean'], stats['median'], stats['mode'], stats['std']], color=['blue', 'green', 'red', 'purple'])
    axs[0].set_title('Statistical Summary')
    axs[0].set_ylabel('Value')
    
    # Histogram for the points list
    axs[1].hist(stats['values'], bins=5, color='skyblue', edgecolor='black')
    axs[1].set_title('Distribution of Points')
    axs[1].set_xlabel('Points')
    axs[1].set_ylabel('Frequency')
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    
def get_top_ten_most_comments(hacker_news):
    sorted_comments = sorted(hacker_news, key=lambda x: x.num_comments, reverse=True)
    top_ten = sorted_comments[:10]
    return top_ten

top_ten_comments = get_top_ten_most_comments(news_list)
top_ten_dicts_comments = [post.to_dict() for post in top_ten_comments]

def get_top_ten_most_points(hacker_news):
    sorted_points = sorted(hacker_news, key=lambda x: x.num_points, reverse=True)
    top_ten = sorted_points[:10]
    return top_ten

top_ten_points = get_top_ten_most_points(news_list)
top_ten_dicts_points = [post.to_dict() for post in top_ten_points]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1.0/points-stats', methods=['GET'])
def points_stats():
    result = get_points_stats()
    return jsonify(result)

@app.route('/api/v1.0/top-ten-comments', methods=['GET'])
def news_list_comments():
    return jsonify(top_ten_dicts_comments)

@app.route('/api/v1.0/top-ten-points', methods=['GET'])
def news_list_points():
    display_graph()
    return jsonify(top_ten_dicts_points)

if __name__ == '__main__':
    app.run(debug=False)