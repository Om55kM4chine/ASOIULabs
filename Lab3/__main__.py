#TODO: создание web-приложения для блога с помощью Flask. Написанный текст должен сохраняться и выводиться по убыванию даты.
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
posts = []

@app.route('/')
def index():
    ordered_posts = sorted(posts, key=lambda p: p['date'], reverse=True)
    return render_template('index.html', posts=ordered_posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if title and content:
        posts.append({'title': title, 'content': content, 'date': datetime.now()})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)