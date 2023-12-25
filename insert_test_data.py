from init_program import app, db
from db_tables import Task, Project


def create_tables():
    with app.app_context():
        db.create_all()


def insert_data():
    # Add new tasks and projects
    p1 = Project(
        name="Home project"
    )

    p2 = Project(
        name="School project"
    )

    t1 = Task(
        name="Go to supermarket",
        date="07/11/2023",
        project=p1
    )
    t2 = Task(
        name="Clean room",
        date="08/11/2023",
        project=p1
    )
    t3 = Task(
        name="Finish the project",
        date="10/11/2023",
        project=p2
    )

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.commit()



