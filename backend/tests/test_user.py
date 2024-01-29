import json

from mlcb_services.db_models.models import MlcbUsers

user_payload_path = 'backend/tests/pytest_payload/user.json'


def test_create_user(setup_test_db, db_test_env):  # pylint: disable=W0613
    with open(user_payload_path, 'r') as file:
        user_payload = json.load(file)

    user = MlcbUsers(**user_payload)
    setup_test_db.add(user)
    setup_test_db.commit()

    db_user = setup_test_db.query(MlcbUsers).filter(MlcbUsers.user_name == user_payload['user_name']).first()
    assert db_user is not None
    for key, value in user_payload.items():
        if key == 'role' and hasattr(db_user, key):
            assert getattr(db_user, key).value == value
        else:
            assert getattr(db_user, key) == value
