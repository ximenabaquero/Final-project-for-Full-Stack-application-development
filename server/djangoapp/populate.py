import json
import os

from django.conf import settings

from .models import CarMake, CarModel


_BODYTYPE_TO_CHOICE = {
    "sedan": CarModel.SEDAN,
    "suv": CarModel.SUV,
    "wagon": CarModel.WAGON,
    "coupe": CarModel.COUPE,
    "hatchback": CarModel.HATCHBACK,
    "convertible": CarModel.CONVERTIBLE,
    "minivan": CarModel.MINIVAN,
    "truck": CarModel.TRUCK,
}


def initiate():
    data_path = os.path.join(settings.BASE_DIR, "database", "data", "car_records.json")
    if not os.path.exists(data_path):
        print(f"car_records.json not found at: {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    cars = payload.get("cars", [])
    created_makes = 0
    created_models = 0

    for car in cars:
        make_name = (car.get("make") or "").strip()
        model_name = (car.get("model") or "").strip()
        body_type = (car.get("bodyType") or "").strip().lower()
        year = car.get("year")

        if not make_name or not model_name or year is None:
            continue

        car_make, make_created = CarMake.objects.get_or_create(
            name=make_name,
            defaults={"description": ""},
        )
        if make_created:
            created_makes += 1

        model_type = _BODYTYPE_TO_CHOICE.get(body_type, CarModel.SEDAN)

        car_model, model_created = CarModel.objects.get_or_create(
            car_make=car_make,
            name=model_name,
            year=int(year),
            defaults={"type": model_type},
        )
        if model_created:
            created_models += 1

    print(f"Populate complete. New makes: {created_makes}, new models: {created_models}")
