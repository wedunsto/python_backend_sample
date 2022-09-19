"""
Application will start on http://localhost:8080
Application has two endpoints:
    Add a blog post: POST at /blog/post
    Get a blog post by id: GET at /blog/post/{id}
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

blogs = [
    {
    "id": 0,
    "author": "Peter Parker",
    "title": "Title Example",
    "text": "This is sample text for a blog post!"
    }
]

comments = {0:[{"author": "Bruce Wayne", "text": "This is sample text for a comment!"}]}

def _find_next_blog_id():
    return max(blog["id"] for blog in blogs) + 1

@app.route("/blog/post", methods = ['POST'])
def add_blog():
    if request.is_json:
        blog = request.get_json()
        blog["id"] = _find_next_blog_id()
        blogs.append(blog)
        return blog, 201
    return {"error": "Request must be JSON"}, 415

@app.route("/blog/post", methods = ['GET'])
def get_blogs():
    return jsonify(blogs)

@app.route('/blog/post/<int:id>', methods = ['GET'])
def get_blog(id):
    blog_id = id
    return jsonify(blogs[blog_id])

@app.route('/blog/post/<int:id>/comment', methods = ['POST'])
def add_comment(id):
    if request.is_json:
        comment = request.get_json()
        if id in comments.keys():
            comments[id].append(comment)
            return comment, 201
        comments[id] = [comment]
        return comment, 201
    return {"error": "Request must be JSON"}, 415

@app.route('/blog/post/<int:id>/comment', methods = ['GET'])
def get_comment(id):
    blog_id = id
    return jsonify(comments[blog_id])

app.run(host="localhost", port=8080, debug=True)