from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Category(models.Model):
    name = models.TextField(verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Company(models.Model):
    cat_id = models.SmallIntegerField(unique=True, verbose_name='ИНН', primary_key=True)
    name = models.TextField(verbose_name='Название компании')
    phone = PhoneNumberField(verbose_name='Контактный номер')
    email = models.EmailField(verbose_name='Email')
    about = models.TextField(verbose_name='О компании')
    category = models.ForeignKey(Category,  on_delete=models.CASCADE, verbose_name='Категория',
                                )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
