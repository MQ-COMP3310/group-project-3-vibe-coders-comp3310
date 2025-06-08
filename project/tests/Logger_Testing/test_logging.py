from project.models import ActivityLog
from project.security import log_activity


def test_log_sanitization():
    malicious_input = "user\nDELETE FROM users;--"
    log_activity(1, "test", details=malicious_input)
    log = ActivityLog.query.first()
    assert "\n" not in log.details  #Newlines sanitized
    assert ";" not in log.details  #SQL statements broken
    #attackers may be able to inject malicious content into logs
    #verify special characters are sanitized

def test_no_password_logging():
    log_activity(1, "login", details="password=secret123")
    log = ActivityLog.query.first()
    assert "secret123" not in log.details
    assert "REDACTED" in log.details  #Verify redaction
    #test to see if the logger is accidentally logging passwords/secrets
    #this is to ensure no sensitive data is logged