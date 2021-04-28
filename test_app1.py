import unittest
import requests


class test_api_flask(unittest.TestCase):
    API_URL = 'http://127.0.0.1:5000'
    SIGNUP_ROUTE = f'{API_URL}/auth/signup'

    def test_signup(self):
        r = requests.post(test_api_flask.SIGNUP_ROUTE,
                          data={'inputEmail':'TEST_API@gmail.com',
                                'inputPassword':1234,
                                'client_name':'TEST_API'}
                                )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['info'], 'user created!')
        
if __name__=="__main__":
    unittest.main()