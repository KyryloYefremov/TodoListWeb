from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task-manager.db"
# Initialise the app with the extension
db.init_app(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.String)


# with app.app_context():
#     db.create_all()

# Add new tasks
t1 = Task(
    name="Go to supermarket",
    date="07/11/2023"
)
t2 = Task(
    name="Clean room",
    date="08/11/2023"
)
t3 = Task(
    name="Finish the project",
    date="10/11/2023"
)

# with app.app_context():
#     db.session.add(t1)
    # db.session.add(t2)
    # db.session.add(t3)
    # db.session.commit()


@app.route("/")
def home():
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return render_template("index.html", all_tasks=tasks)


@app.route("/future-tasks/")
def get_future_tasks():
    return render_template("future_tasks.html")


@app.route("/projects/")
def get_projects():
    return render_template("projects.html")


if __name__ == '__main__':
    app.run(debug=True)

