from flask import Flask, jsonify, render_template
import csv
from pathlib import Path

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

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                id = int(row.get('id', '0'))
                title = row.get('title', '')
                url = row.get('url', '')
                num_points = int(row.get('num_points', '0'))
                num_comments = int(row.get('num_comments', '0'))
                author = row.get('author', '')
                created_at = row.get('created_at', '')

                post = HackerNews(id, title, url, num_points, num_comments, author, created_at)
                news_list.append(post)
            except ValueError:
                continue

    return news_list

def get_top_ten_most_comments(hacker_news):
    sorted_comments = sorted(hacker_news, key=lambda x: x.num_comments, reverse=True)
    top_ten = sorted_comments[:10]
    return top_ten

def get_top_ten_most_points(hacker_news):
    sorted_points = sorted(hacker_news, key=lambda x: x.num_points, reverse=True)
    top_ten = sorted_points[:10]
    return top_ten

file_path = Path('./data/hacker_news.csv')
news_list = all_hacker_news(file_path)

top_ten_comments = get_top_ten_most_comments(news_list)
top_ten_dicts_comments = [post.to_dict() for post in top_ten_comments]

top_ten_points = get_top_ten_most_points(news_list)
top_ten_dicts_points = [post.to_dict() for post in top_ten_points]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1.0/top-ten-comments', methods=['GET'])
def news_list_comments():
    return jsonify(top_ten_dicts_comments)

@app.route('/api/v1.0/top-ten-points', methods=['GET'])
def news_list_points():
    return jsonify(top_ten_dicts_points)

if __name__ == '__main__':
    app.run(debug=False)