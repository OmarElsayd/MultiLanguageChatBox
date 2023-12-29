import json

from rtvt_services.db_models.models import RtvtUsers

user_payload_path = 'backend/tests/pytest_payload/user.json'


def test_create_user(setup_test_db, db_test_env):  # pylint: disable=W0613
    with open(user_payload_path, 'r') as file:
        user_payload = json.load(file)

    user = RtvtUsers(**user_payload)
    setup_test_db.add(user)
    setup_test_db.commit()

    db_user = setup_test_db.query(RtvtUsers).filter(RtvtUsers.user_name == user_payload['user_name']).first()
    assert db_user is not None
    for key, value in user_payload.items():
        if key == 'role' and hasattr(db_user, key):
            assert getattr(db_user, key).value == value
        else:
            assert getattr(db_user, key) == value
