from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxValueValidator, MinValueValidator

# Food model regex
class Food(models.Model):
    category = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex = r'^(Main|Dessert|Drink)$'
        )
    ])
    name = models.CharField(max_length=30, validators=[
        RegexValidator(
            regex = r'^[A-Za-z0-9 ]+$'
        ),
        MinLengthValidator(2)
    ])
    price = models.FloatField(validators=[
        MaxValueValidator(999.99),
        MinValueValidator(0.1)
    ])
    checked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']