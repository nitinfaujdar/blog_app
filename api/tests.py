from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Post, Comment

class BlogTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title='Test Post', content='Content of the test post', author=self.user)

    def test_create_post(self):
        response = self.client.post('/api/blog/', {'title': 'New Post', 'content': 'New content', 'author': self.user.id})
        self.assertEqual(response.status_code, 201)

    def test_get_posts(self):
        response = self.client.get('/api/blog/')
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        response = self.client.patch(f'/api/blog/', {'blog': self.post.id, 'title': 'Updated Post', 'content': 'Updated content', 'author': self.user.id})
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        response = self.client.delete(f'/api/blog/', {'blog': self.post.id})
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        response = self.client.post(f'/api/comment/', {'post': self.post.id, 'text': 'New comment', 'author': self.user.id})
        self.assertEqual(response.status_code, 201)
