import unittest
from llms_free import generate_cookies, save_cookies, load_cookies

class TestLLMSFree(unittest.TestCase):

    def test_generate_cookies(self):
        # Test that cookies are generated for each URL
        for url in URLS.values():
            cookies = generate_cookies(url)
            self.assertIsNotNone(cookies)

    def test_save_and_load_cookies(self):
        # Test that cookies can be saved and loaded for each URL
        for model, url in URLS.items():
            cookies = generate_cookies(url)
            save_cookies(model, cookies)
            loaded_cookies = load_cookies(model)
            self.assertEqual(cookies, loaded_cookies)

if __name__ == '__main__':
    unittest.main()


#init test
#python -m unittest test_llms_free.py
test1 = TestLLMSFree()
test1.test_generate_cookies()
test1.test_save_and_load_cookies()
print("test ok")