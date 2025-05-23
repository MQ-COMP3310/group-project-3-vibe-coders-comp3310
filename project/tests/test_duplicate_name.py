def test_register_with_duplicate_username():
    from project import create_app, db
    from project.models import User
    from sqlalchemy.exc import IntegrityError

    app = create_app()

    with app.app_context():
        # Ensure tables are created
        db.create_all()

        # Create a user with a unique username
        user1 = User(username='testuser', password='plaintextpassword')
        db.session.add(user1)
        db.session.commit()

        # Attempt to register another user with the same username
        user2 = User(username='testuser', password='anotherpassword')
        db.session.add(user2)

        try:
            db.session.commit()
            assert False, "Expected IntegrityError due to duplicate username"
        except IntegrityError as e:
            db.session.rollback()  # Always rollback after an IntegrityError
            assert 'UNIQUE constraint' in str(e.orig)  # More precise

  