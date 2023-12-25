from init_program import db
from sqlalchemy.orm import relationship


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.String)
    # create FK
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    # create reference btw tables
    project = relationship(argument="Project", back_populates="tasks")


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tasks = relationship(argument="Task", back_populates="project")
