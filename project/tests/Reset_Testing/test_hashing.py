from project.models import User
from werkzeug.security import check_password_hash

def test_security_answer_hashing(self):
        """Test that security answers are properly hashed"""
        test_user = User(username='testuser', email='test@example.com')
        test_answer = 'New York'
        
        #set and verify security answer
        test_user.set_security_answer(test_answer)
        
        #verify answer is hashed
        self.assertNotEqual(test_user.security_answer_hash, test_answer.lower())
        self.assertTrue(test_user.check_security_answer(test_answer))
        
        #verify case insensitivity
        self.assertTrue(test_user.check_security_answer('NEW YORK'))
        
        #verify incorrect answer fails
        self.assertFalse(test_user.check_security_answer('wrong answer'))