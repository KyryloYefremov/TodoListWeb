from init_program import app, db
from db_tables import Task, Project
from datetime import datetime, timedelta

TODAY_DATE = datetime.now()
TODAY_DATE_STR = TODAY_DATE.strftime('%d.%m.%Y')


def create_tables():
    with app.app_context():
        db.drop_all()
        db.create_all()


def insert_data():
    # Test projects data
    work_proj = Project(name="Work")
    self_dev_proj = Project(name="Self Development")
    house_work_proj = Project(name="House work")
    long_term_goals_proj = Project(name="Long term goals")
    project_examples = [work_proj, self_dev_proj, house_work_proj, long_term_goals_proj]
    tasks_examples = [
        Task(
            name="Go to supermarket",
            date=TODAY_DATE_STR,
            project=house_work_proj
        ),
        Task(
            name="Clean room",
            date=(TODAY_DATE - timedelta(days=1)).strftime('%d.%m.%Y'),
            project=house_work_proj
        ),
        Task(
            name="Finish the project",
            date=TODAY_DATE_STR,
            project=work_proj
        ),
        Task(
            name="Prepare a project report",
            date=(TODAY_DATE + timedelta(days=30)).strftime('%d.%m.%Y'),
            project=work_proj
        ),
        Task(
            name="Go to gym",
            date=(TODAY_DATE + timedelta(days=2)).strftime('%d.%m.%Y'),
            project=self_dev_proj
        ),
        Task(
            name="Buy subscription for training app",
            date=(TODAY_DATE + timedelta(days=3)).strftime('%d.%m.%Y'),
            project=self_dev_proj
        ),
        Task(
            name="Bring project idea to work",
            date=(TODAY_DATE + timedelta(days=1)).strftime('%d.%m.%Y'),
            project=work_proj
        ),
        Task(
            name="Buy a car",
            date=(TODAY_DATE + timedelta(days=120)).strftime('%d.%m.%Y'),
            project=long_term_goals_proj
        )
    ]

    with app.app_context():
        # Add all test data to database
        for proj in project_examples:
            db.session.add(proj)
        for task in tasks_examples:
            db.session.add(task)

        db.session.commit()



