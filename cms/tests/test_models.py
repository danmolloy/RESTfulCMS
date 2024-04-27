from django.test import TestCase
from django.contrib.auth.models import User
from ..models import BlogPost


class BlogPostModelTests(TestCase):
  def setUp(self):
    self.author = User.objects.create(username="brett_stable")

  def test_create_blog_post(self):
    """Ensure blog post is created with expected values."""
    post = BlogPost.objects.create(
      title="Test Post",
      slug="test-post",
      author=self.author,
      body="This is a test post.",
      status="draft",
    )
    self.assertEqual(post.title, "Test Post")
    self.assertEqual(post.slug, "test-post")
    self.assertEqual(post.author, self.author)
    self.assertEqual(post.body, "This is a test post.")
    self.assertEqual(post.status, "draft")