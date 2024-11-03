# Функциональная оболоска перечня машин
# Нужена чтобы было проще работать со списком машин.

class CarManager:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self, index):
        if 0 <= index < len(self.cars):
            del self.cars[index]

    def update_car(self, index, car):
        if 0 <= index < len(self.cars):
            self.cars[index] = car

    def get_cars(self):
        return self.cars

    def search_cars(self, filters):
        return [car for car in self.cars if all(getattr(car, key) == value for key, value in filters.items() if value)]