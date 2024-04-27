from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
import json

from ..models import BlogPost


class IndexViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(username='testuser', password='secretpassword')

  def test_not_logged_in(self):
    """If user not logged in, expect to be redirected to log in page."""
    response = self.client.get("/")
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, "/accounts/login/?next=/", status_code=302)

  def test_logged_in(self):
    """If user logged in, expect index view to render."""
    self.client.login(username='testuser', password='secretpassword')
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Your Blog")


class DetailViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(
      username='testuser', 
      password='secretpassword'
    )
    self.fake_post = BlogPost.objects.create(
      title="fake post", 
      body="this is fake!", 
      slug="fake_post", 
      author=self.test_user, 
      id="1")

  def test_detail_view(self):
    self.client.login(username='testuser', password='secretpassword')
    response = self.client.get(f'/posts/{self.fake_post.id}/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "cms/detail.html")
    self.assertEqual(response.context['blogpost'], self.fake_post)


class CreateViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(
      username='testuser', 
      password='secretpassword'
    )
    self.client.login(username='testuser', password='secretpassword')

  def test_get_request(self):
    response = self.client.get("/create/")
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "cms/create.html")

  def test_post_valid_form(self):
    data = {
      'title': 'Test Title',
      'body': 'Test Body',
      'status': 'published'
    }
    response = self.client.post("/create/", data)
    self.assertRedirects(response, "/")

  def test_post_invalid_form(self):
    data = {}
    response = self.client.post("/create/", data)
    self.assertEqual(response.status_code, 200)
    form = response.context['form']
    self.assertFalse(form.is_valid())
    self.assertTrue(form.has_error('title', code='required'))
    self.assertTrue(form.has_error('body', code='required'))
    self.assertTrue(form.has_error('status', code='required'))


class UpdateViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(
      username='testuser', 
      password='secretpassword'
    )
    self.fake_post = BlogPost.objects.create(title="fake post", body="this is fake!", slug="fake_post", author=self.test_user, id="1")
    self.client.login(username='testuser', password='secretpassword')

  def test_get_request(self):
    response = self.client.get(f'/update/{self.fake_post.id}/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "cms/update.html")
  
  def test_post_request(self):
    data = {
      "title": "real post", 
      "body": "this is not fake!",
      "status":"published", 
      "author": self.test_user, 
    }
    response = self.client.post(f'/update/{self.fake_post.id}/', data)
    self.assertRedirects(response, "/")

class DeleteViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(
      username='testuser', 
      password='secretpassword'
    )
    self.fake_post = BlogPost.objects.create(title="fake post", body="this is fake!", slug="fake_post", author=self.test_user, id="1")
    self.client.login(username='testuser', password='secretpassword')

  def test_post_request(self):
    response = self.client.post(f"/delete/{self.fake_post.id}/", {'confirm_delete': True})
    self.assertRedirects(response, "/")
    with self.assertRaises(BlogPost.DoesNotExist):
            BlogPost.objects.get(id=self.fake_post.id)

class SignUpViewTests(TestCase):
  def test_get_request(self):
    """On GET request, empty form renders."""
    response = self.client.get("/signup/")
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Sign Up")
    self.assertTemplateUsed(response, "registration/signup.html")
    form = response.context['form']
    self.assertIsInstance(form, UserCreationForm)

  def test_form_submits(self):
    """User is successfully created on form submission."""
    username = 'newuser'
    password = 'ijqs9283bfu'
    response = self.client.post(reverse('signup'), {
      'username': username,
      'password1': password,
      'password2': password,
    })
    self.assertEqual(response.status_code, 302)
    self.assertTrue(User.objects.filter(username=username).exists())

  
  def test_invalid_username(self):
    """If username is invalid, form does not submit and page is re-rendered."""
    username = 'dan!'
    password = 'ijqs9283bfu'
    response = self.client.post(reverse('signup'), {
      'username': username,
      'password1': password,
      'password2': password,
    })
    self.assertNotEqual(response.status_code, 302)
    self.assertFalse(User.objects.filter(username=username).exists())

  
  def test_invalid_password(self):
    """If password is invalid, form does not submit and page is re-rendered."""
    username = 'danmolloy1'
    password = '12345'
    response = self.client.post(reverse('signup'), {
      'username': username,
      'password1': password,
      'password2': password,
    })
    self.assertNotEqual(response.status_code, 302)
    self.assertFalse(User.objects.filter(username=username).exists())

class RestfulApiViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(username='testuser', password='secretpassword')
    self.author_user = User.objects.create_user(username='testuser2', password='secretpassword')
    self.fake_post = BlogPost.objects.create(title="fake post", body="this is fake!", slug="fake_post", author=self.author_user, id="1", status="published")
    self.fake_draft = BlogPost.objects.create(title="fake draft", body="this is a draft!", slug="draft", author=self.author_user, id="2", status="draft")

  def test_valid_user_with_posts(self):
    """Returns all published posts authored by elected user, excluding drafts."""
    response = self.client.get(f'/api/{self.author_user.username}/')
    expected_data = {"posts": [{"id": 1, "title": "fake post", "body": "this is fake!", "slug": "fake_post", "status": "published", "pub_date": self.fake_post.pub_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z', "author_id": 2}]}
    self.assertEqual(response.json(), expected_data)
    self.assertEqual(response.status_code, 200)

  def test_valid_user_without_posts(self):
    response = self.client.get(f'/api/{self.test_user.username}/')
    self.assertEqual(response.json(), {"posts": []})
    self.assertEqual(response.status_code, 200)

  def test_invalid_user(self):
    response = self.client.get(f'/api/foobar/')
    self.assertEqual(response.json(), {"posts": []})
    self.assertEqual(response.status_code, 200)