from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class Country(models.Model):
    name = models.CharField(max_length=25)


class Authors(models.Model):
    fullname = models.CharField(max_length=25)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date_of_birth = models.CharField(default="", max_length=10)
    date_of_death = models.CharField(default="", max_length=10, blank=True)

    def __str__(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Books(models.Model):
    slug = models.SlugField(default="")
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, default="Book")
    img = models.CharField(max_length=35, default='default.jpg')
    description = models.TextField(default="Description is not available")
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    read = models.BooleanField(default=False)
    language = models.CharField(max_length=20, default="English")
    original_language = models.CharField(max_length=20, default="English")
    categories = models.ManyToManyField(Category, blank=True, through="BooksCategories")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Books, self).save(*args, **kwargs)


class BooksCategories(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} - {self.category.name}"


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()


class UserActivity(models.Model):
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=50)
    user_agent = models.TextField()
    browser = models.CharField(max_length=20)
    os = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)  # Assuming your book model is named 'Books'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"


class Score(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('book', 'user')