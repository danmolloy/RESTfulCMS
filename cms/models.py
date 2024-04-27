from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

class BlogPost(models.Model):
  title = models.CharField(max_length=30)
  body = models.TextField()
  slug = models.SlugField(unique=True)
  status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft')
  pub_date = models.DateTimeField("date published", default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  def save(self, *args, **kwargs):
        # Generate a slug if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)

            # Check if the generated slug is unique
            while BlogPost.objects.filter(slug=self.slug).exists():
                # If not, append a number to make it unique
                self.slug = slugify(self.title) + '-' + str(timezone.now().timestamp())

        super().save(*args, **kwargs)



  def __str__(self) -> str:
        return self.title