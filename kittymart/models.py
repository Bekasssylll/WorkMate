"""модель для каждого котенка(цвет,возраст,описание)"""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Kitten(models.Model):
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('brown', 'Brown'),
        ('gray', 'Gray'),
        ('cream', 'Cream'),
        ('other', 'Other'),
    ]

    BREED_CHOICES = [
        ('persian', 'Persian'),
        ('maine_coon', 'Maine Coon'),
        ('siamese', 'Siamese'),
        ('bengal', 'Bengal'),
        ('sphynx', 'Sphynx'),
        ('other', 'Other'),
    ]

    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='other')
    age_in_months = models.PositiveIntegerField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    breed = models.CharField(max_length=20, choices=BREED_CHOICES, default='other')

    def __str__(self):
        return f"{self.get_color_display()} {self.get_breed_display()} kitten, {self.age_in_months} months old"


class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SCORE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    score = models.PositiveIntegerField(choices=SCORE_CHOICES)

    class Meta:
        unique_together = ('kitten', 'user')

    def __str__(self):
        return f"Rating {self.score} by {self.user.username} for {self.kitten}"
