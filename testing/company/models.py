from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    website = models.URLField()


class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    position = models.CharField(max_length=100)
    department = models.OneToOneField("Department", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Create your models here.
