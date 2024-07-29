import csv
from .models import Ingredient

def load_ingredients_from_csv(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Row: {row}")  # 각 행을 출력하여 확인
                Ingredient.objects.get_or_create(
                    name=row['name'],
                    item=row['item'],
                    defaults={'code': row['code']}
                )
    except Exception as e:
        print(f"Error: {e}")  # 예외 발생 시 오류 메시지 출력
