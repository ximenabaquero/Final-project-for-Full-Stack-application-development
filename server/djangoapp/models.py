from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True, default="")

	def __str__(self) -> str:
		return self.name


class CarModel(models.Model):
	SEDAN = "SEDAN"
	SUV = "SUV"
	WAGON = "WAGON"
	COUPE = "COUPE"
	HATCHBACK = "HATCHBACK"
	CONVERTIBLE = "CONVERTIBLE"
	MINIVAN = "MINIVAN"
	TRUCK = "TRUCK"

	CAR_TYPE_CHOICES = [
		(SEDAN, "Sedan"),
		(SUV, "SUV"),
		(WAGON, "Wagon"),
		(COUPE, "Coupe"),
		(HATCHBACK, "Hatchback"),
		(CONVERTIBLE, "Convertible"),
		(MINIVAN, "Minivan"),
		(TRUCK, "Truck"),
	]

	car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES, default=SEDAN)
	year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2023)])

	class Meta:
		unique_together = ("car_make", "name", "year")

	def __str__(self) -> str:
		return f"{self.car_make.name} {self.name} ({self.year})"
