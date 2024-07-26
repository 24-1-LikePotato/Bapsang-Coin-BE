import csv
from .models import Ingredient

def load_ingredients_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Ingredient.objects.get_or_create(name=row['name'], item=row['item'], code=row['code'])
