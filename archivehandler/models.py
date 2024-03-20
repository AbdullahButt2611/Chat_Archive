import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Friend(models.Model):
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    slug = models.SlugField(unique=True, max_length=255)
    
    def __str__(self):
        return self.name + ', Friend of '+ self.user.email
    
    def save(self, *args, **kwargs):
        print('Inside Safe')
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            queryset = Friend.objects.filter(slug=self.slug, user=self.user)
            counter = 1
            if queryset.exists():
                random_suffix = str(uuid.uuid4())[:8]  # Generate a random suffix
                self.slug = f"{original_slug}-{random_suffix}"
        super().save(*args, **kwargs)

    # Defines a metadata class to enforce that within each user's scope, no two Friend objects can have the same slug.
    class Meta:
        unique_together = ('user', 'slug')

class Chat(models.Model):
    start_date = models.CharField(max_length=30)
    end_date = models.CharField(max_length=30)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='chats')
    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self):
        return self.friend.user.first_name + ' Chatted with  '+ self.friend.name + ' from ' + self.start_date + ' to ' + self.end_date
    
    def save(self, *args, **kwargs):
        # Generate a unique slug based on friend's name
        base_slug = slugify(self.friend.name + "-chat")

        # Generate random characters using uuid
        random_chars = str(uuid.uuid4()).replace("-", "")[:6]  # Using the first 6 characters

        # Combine base slug and random characters
        self.slug = f"{base_slug}-{random_chars}"

        super().save(*args, **kwargs)
    
class Message(models.Model):
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=2500)
    is_user = is_user = models.BooleanField(default=False)

    def __str__(self):
        return self.text
