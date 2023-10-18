from flask import Flask, url_for, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/today-tasks/")
def get_today_tasks():
    return render_template("today_tasks.html")


@app.route("/future-tasks/")
def get_future_tasks():
    return render_template("future_tasks.html")


@app.route("/projects/")
def get_projects():
    return render_template("projects.html")


if __name__ == '__main__':
    app.run(debug=True)

