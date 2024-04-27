from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


from ..models import BlogPost

class SignUpTemplateTests(TestCase):
  def test_sign_up_template(self):
    response = self.client.get("/signup/")
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'registration/signup.html')
    form = response.context['form']
    self.assertIsInstance(form, UserCreationForm)
    self.assertContains(response, '<h2>Sign Up</h2>')
    self.assertContains(response, '<form method="post">')
    self.assertContains(response, '<button type="submit" class="button-primary">Sign Up</button>')
    self.assertContains(response, "<h2>myCMS</h2>")

class BaseTemplateTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(username='testuser', password='secretpassword')

  def test_base_template_not_logged_in(self):
    response = self.client.get('/signup/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '<h2>myCMS</h2>')
  
  def test_base_template_logged_in(self):
    self.client.login(username='testuser', password='secretpassword')
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '<h2>myCMS</h2>')
    self.assertContains(response, '<p>testuser</p>')
    self.assertContains(response, "Log out")

class IndexTemplateTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(username='testuser', password='secretpassword')
    self.author_user = User.objects.create_user(username='testuser2', password='secretpassword')
    self.fake_post = BlogPost.objects.create(title="fake post", body="this is fake!", slug="fake_post", author=self.author_user, id="1")

  def test_index_template_no_posts(self):
    self.client.login(username='testuser', password='secretpassword')
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '<p>No posts available.</p>')
    self.assertContains(response, '<a class="button-primary" href="create/">Create</a>')
  
  def test_index_template_with_posts(self):
    self.client.login(username='testuser2', password='secretpassword')
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, '<p>No posts available.</p>')
    self.assertContains(response, '<h3>fake post</h3>')
    self.assertContains(response, f'<a class="post-tile" href="/posts/{self.fake_post.id}/">')
    self.assertContains(response, '<a class="button-primary" href="create/">Create</a>')

class DetailTemplateTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(username='testuser', password='secretpassword')
    self.time = timezone.now()

    self.fake_post = BlogPost.objects.create(title="fake post", body="this is fake!", slug="fake_post", author=self.test_user, id="1", pub_date=self.time)

  def test_detail_template(self):
    self.client.login(username='testuser', password='secretpassword')
    response = self.client.get(f'/posts/{self.fake_post.id}/')
    self.assertTemplateUsed(response, "cms/detail.html")
    self.assertContains(response, f'{self.fake_post.title}')
    self.assertContains(response, self.fake_post.body)
    self.assertContains(response, '<input class="button-secondary delete-btn" type="submit" value="Delete">')
    self.assertContains(response, f'<a class="button-primary" href="/update/{self.fake_post.id}">Edit</a>')
    formatted_date = self.time.strftime('%B %d, %Y, %-I:%M ') 
    self.assertContains(response, formatted_date)
