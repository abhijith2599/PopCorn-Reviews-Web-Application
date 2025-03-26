from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class  Movies(models.Model):

    M_name = models.CharField(max_length=100)

    M_lang = models.CharField(max_length=100)

    Director = models.CharField(max_length=100)

    Released_date = models.DateField()

    Genre = models.CharField(max_length=100)

    Image = models.ImageField(upload_to='movie_images',null=True,blank=True)

    def __str__(self):

        return self.M_name
    
    def average_rating(self):
        reviews = self.review_set.all()  # Get all related reviews for this movie
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)  # Round to 1 decimal place
        return 0


class Review(models.Model):

    class RatingChoices(models.IntegerChoices):

            ONE = 1, "⭐ 1"
            TWO = 2, "⭐⭐ 2"
            THREE = 3, "⭐⭐⭐ 3"
            FOUR = 4, "⭐⭐⭐⭐ 4"
            FIVE = 5, "⭐⭐⭐⭐⭐ 5"

    comments = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices)
    created_date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movies,on_delete=models.CASCADE)

    class Meta:

        #  unique_together = ('user_id','movie_id')
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'movie_id'], name='unique_user_movie_review')
        ]

    def  __str__(self):

        return f"{self.user_id.username} - {self.movie_id.M_name} - {self.rating} Stars"