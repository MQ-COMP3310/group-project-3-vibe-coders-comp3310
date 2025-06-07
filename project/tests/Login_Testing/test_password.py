
def testPasswordHash():
    """
    Test password hashing
    """
    from project import create_app, db
    from project.models import User

    app = create_app()
    app.app_context().push()

    # Create a user with a plaintext password
    user = User(username='testuser', password='plaintextpassword')
    db.session.add(user)
    db.session.commit()

    # Check that the password is hashed
    assert user.password != 'plaintextpassword'
    assert user.check_password('plaintextpassword') is True
    Pass
