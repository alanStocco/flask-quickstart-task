import unittest
from app import app

class TestApp(unittest.TestCase):
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Index Page')
        
    def test_show_post(self):
        tester = app.test_client(self)
        response = tester.get('/post/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Post 1')
        
    def test_show_subpath(self):
        tester = app.test_client(self)
        response = tester.get('/path/mysubpath', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Subpath mysubpath')
        
    def test_projects(self):
        tester = app.test_client(self)
        response = tester.get('/projects/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'The project page')
        
    def test_about(self):
        tester = app.test_client(self)
        response = tester.get('/about', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'The about page')
        
if __name__ == '__main__':
    unittest.main()