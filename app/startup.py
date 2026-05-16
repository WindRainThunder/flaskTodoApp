from app.extensions import db
from app.models import User

def clear_test_user_tasks():
    test_user = User.query.filter_by(username="test").first()
    print("testUser")
    print(test_user)

    if test_user:
        for task in test_user.tasks:
            db.session.delete(task)

        db.session.commit()