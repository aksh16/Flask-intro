from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
	#Ensure that flask was setup correctly
	def test_setup(self):
		tester = app.test_client()
		response = tester.get('/login',content_type = 'html/css')
		self.assertEqual(response.status_code, 200)

	#Ensure that login page loads correctly
	def test_login_redirect(self):
		tester = app.test_client()
		response = tester.get('/login',content_type = 'html/css')
		self.assertTrue(b'Please login' in response.data)

	# Login page behaves correctly with the correct credentials
	def test_login_correct(self):
		tester = app.test_client()
		response = tester.post('/login',
			data = dict(username = "aksh", password = "patel"),
			follow_redirects = True)
		self.assertIn(b'You were just logged in!', response.data)


	# Login page behaves correctly with the incorrect credentials
	def test_login_incorrect(self):
		tester = app.test_client()
		response = tester.post('/login',
			data = dict(username = "adj", password = "uieriur"),
			follow_redirects = True)
		self.assertIn(b'Invalid username or password. Please try again', response.data)

	# Logout page behaves correctly
	def test_logout(self):
		tester = app.test_client()
		tester.post('/login',
		 	data = dict(username = "aksh", password = "patel"),
		 	follow_redirects = True)
		response = tester.get('/logout',follow_redirects = True)
		self.assertIn(b'You were just logged out!', response.data)

	#Ensure main route requires login
	def test_main_requires_login(self):
		tester = app.test_client()
		response = tester.get('/',follow_redirects = True)
		self.assertTrue(b'You need to login first!', response.data)

	#Ensure logout route requires login
	def test_logout_requires_login(self):
		tester = app.test_client()
		response = tester.get('/logout',follow_redirects = True)
		self.assertTrue(b'You need to login first!', response.data)



if __name__ == '__main__':
	unittest.main()
