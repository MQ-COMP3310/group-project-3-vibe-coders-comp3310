def test_activity_log_access(client, regular_user, admin_user):
    # Non-admin attempt
    client.login(regular_user)
    response = client.get("/activity-log")
    assert response.status_code == 403
    
    # Admin access
    client.login(admin_user)
    response = client.get("/activity-log")
    assert response.status_code == 200

    #this is to test whether non adminds are able to access the logs
    #and verify admin only enforcement 