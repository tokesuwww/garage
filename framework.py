import tkinter as tk
from tkinter import messagebox, ttk

from Tools.scripts.make_ctype import values

from car import Car
from carmanager import CarManager
import random


class App:
    COLORS = ["Красный", "Синий", "Зеленый", "Черный", "Белый", "Серый", "Желтый", "Оранжевый", "Фиолетовый", "Розовый"]

    BRANDS_MODELS = {
        "Audi": ["A4", "Q8", "e-tron", "Q7", "Q5 Sportback"],
        "BMW": ["X5", "3 Series", "5 Series", "X3", "Z4"],
        "Buggati": ["Chiron", "Tourbillon", "Veyron"],
        "Cadillac": ["Eldorado", "DeVille", "Fleetwood", "Catera", "Escalade"],
        "Chevrolet": ["Monza", "Tahoe", "Equinox", "Camaro", "Niva"],
        "Dodge": ["Ram", "Challenger", "Caliber", "Nitro", "Caravan"],
        "Exeed": ["RX", "TXL", "LX", "VX"],
        "Ferrary": ["Maranello", "Fiorano", "Superfast", "Berlinetta", "Testarossa"],
        "Ford": ["Focus", "Fiesta", "Mustang", "Explorer", "F-150"],
        "Honda": ["Civic", "Accord", "CR-V", "Fit", "Pilot"],
        "Hyundai": ["Tucson", "Elantra", "Santa Fe", "Palisade", "Sonata"],
        "Jeep": ["Avenger", "Compass", "Grand Cherokee", "Liberty", "Patriot"],
        "Kia": ["Seltos", "Ceed", "Sportage", "Sorento", "Rio"],
        "Lamborghini": ["Urus", "Huracan", "Aventador", "Gallardo", "Diablo"],
        "Land Rover": ["Defender", "Freelander", "Evoque", "Discovery", "Sport"],
        "Lexus": ["RX350", "GX550", "LX600", "NX200", "IS F"],
        "Mazda": ["Cronos", "Grand Familia", "Millenia", "Revue", "Sentia"],
        "Mitsubishi": ["Eclipse Cross", "ASX", "Pajero Sport", "Outlander", "L200"],
        "Nissan": ["Ariya", "Qashqai", "Murano", "Terrano", "X-Trail"],
        "Porsche": ["Taycan", "Panamera", "Cayman", "Macan", "Boxster"],
        "Renault": ["Kaptur", "Duster", "Arkana", "Latitude", "Symbol"],
        "Subaru": ["Legacy", "Outback", "Forester", "WRX STi", "XV"],
        "Toyota": ["Camry", "Corolla", "RAV4", "Hilux", "Yaris"],
        "Volkswagen": ["Jetta", "Passat", "Golf", "Polo", "Tiguan"]

    }

    def __init__(self, root):
        self.manager = CarManager() # Непосредственно список машин в оболочке
        self.root = root
        self.root.title("Программа")

        # Создание таблицы для отображения машин
        self.tree = ttk.Treeview(root, columns=("brand", "model", "color", "transmission", "engine", "state", "headlights", "doors", "people"), show="headings")

        # Установка заголовков колонок
        self.tree.heading("brand", text="Марка")
        self.tree.heading("model", text="Модель")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("transmission", text="Коробка передач")
        self.tree.heading("engine", text="Двигатель")
        self.tree.heading("state", text="Состояние")
        self.tree.heading("headlights", text="Фары")
        self.tree.heading("doors", text="Двери")
        self.tree.heading("people", text="Люди в машине")

        # Установка ширины колонок
        self.tree.column("brand", width=80)
        self.tree.column("model", width=80)
        self.tree.column("color", width=80)
        self.tree.column("transmission", width=100)
        self.tree.column("engine", width=80)
        self.tree.column("state", width=100)
        self.tree.column("headlights", width=80)
        self.tree.column("doors", width=80)
        self.tree.column("people", width=80)

        # Добавление Treeview в интерфейс
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Настройка заголовков столбцов
        for col in ("brand", "model", "color", "transmission", "engine", "state", "headlights", "doors", "people"):
            self.tree.column(col, anchor="center")

        # Кнопки управления
        button_frame = tk.Frame(root)
        button_frame.pack(pady=0)

        self.add_button = tk.Button(button_frame, text="Добавить", command=self.append_car)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(button_frame, text="Изменить", command=self.upd_car)
        self.update_button.grid(row=0, column=1, padx=5)

        self.remove_button = tk.Button(button_frame, text="Удалить", command=self.pop_car)
        self.remove_button.grid(row=0, column=2, padx=5)

        self.search_button = tk.Button(button_frame, text="Поиск", command=self.open_search)
        self.search_button.grid(row=0, column=3, padx=5)

        # Генерация случайных машин при запуске
        self.generate_random_cars(5)

        # Обновить таблицу машин
        self.upd_cars_table()

    def generate_random_cars(self, count): # Функция для случайного создания машин в списке
        for _ in range(count):
            # Слуйчаный выбор одного из перечня названий списков марок
            brand = random.choice(list(self.BRANDS_MODELS.keys()))

            # Слуйчаный выбор модели из списка моделей марки
            model = random.choice(self.BRANDS_MODELS[brand])

            # Слуйчаный выбор каждого параметра.
            color = random.choice(self.COLORS)
            transmission = random.choice(["Автомат", "Механика"])
            engine = random.choice(["Бензин", "Дизель", "Электро"])
            state = random.choice(["Заведена", "Не заведена"])
            headlights = random.choice(["Включены", "Выключены"])
            doors = random.choice(["Закрытые", "Открытые"])
            people = random.choice(["Есть", "Нет"])

            car = Car(brand, model, color, transmission, engine, state, headlights, doors, people)
            self.manager.add_car(car)

    def upd_cars_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for car in self.manager.get_cars():
            self.tree.insert("", tk.END, values=(car.brand, car.model, car.color, car.transmission, car.engine, car.state, car.headlights, car.doors, car.people))

    def open_search(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Поиск машины")

        tk.Label(search_window, text="Марка:").grid(row=0, column=0)
        brand_combobox = ttk.Combobox(search_window, values=list(self.BRANDS_MODELS.keys()))
        brand_combobox.grid(row=0, column=1)

        tk.Label(search_window, text="Модель:").grid(row=1, column=0)
        model_combobox = ttk.Combobox(search_window)
        model_combobox.grid(row=1, column=1)

        def get_models_by_brand(event):
            brand = brand_combobox.get()
            model_combobox['values'] = self.BRANDS_MODELS.get(brand, [])
            model_combobox.set('')

        brand_combobox.bind("<<ComboboxSelected>>", get_models_by_brand) # добавление списка моделей при открытии выпадающего списка.

        tk.Label(search_window, text="Цвет:").grid(row=2, column=0)
        color_combobox = ttk.Combobox(search_window, values=self.COLORS)
        color_combobox.grid(row=2, column=1)

        tk.Label(search_window, text="Коробка передач:").grid(row=3, column=0)
        transmission_combobox = ttk.Combobox(search_window, values=["Автомат", "Механика"])
        transmission_combobox.grid(row=3, column=1)

        tk.Label(search_window, text="Двигатель:").grid(row=4, column=0)
        engine_combobox = ttk.Combobox(search_window, values=["Бензин", "Дизель", "Электро"])
        engine_combobox.grid(row=4, column=1)

        tk.Label(search_window, text="Состояние:").grid(row=5, column=0)
        state_combobox = ttk.Combobox(search_window, values=["Заведена", "Не заведена"])
        state_combobox.grid(row=5, column=1)

        tk.Label(search_window, text="Фары:").grid(row=6, column=0)
        headlights_combobox = ttk.Combobox(search_window, values=["Включены", "Выключены"])
        headlights_combobox.grid(row=6, column=1)

        tk.Label(search_window, text="Двери:").grid(row=7, column=0)
        doors_combobox = ttk.Combobox(search_window, values=["Закрытые", "Открытые"])
        doors_combobox.grid(row=7, column=1)

        tk.Label(search_window, text="Люди в машине:").grid(row=8, column=0)
        people_combobox = ttk.Combobox(search_window, values=["Есть", "Нет"])
        people_combobox.grid(row=8, column=1)

        def search_cars():
            filters = {
                'brand': brand_combobox.get(),
                'model': model_combobox.get(),
                'color': color_combobox.get(),
                'transmission': transmission_combobox.get(),
                'engine': engine_combobox.get(),
                'state': state_combobox.get(),
                'headlights': headlights_combobox.get(),
                'doors': doors_combobox.get(),
                'people': people_combobox.get()
            }
            filtered_cars = self.manager.search_cars(filters)
            for row in self.tree.get_children():
                self.tree.delete(row)
            for car in filtered_cars:
                self.tree.insert("", tk.END, values=(car.brand, car.model, car.color, car.transmission, car.engine, car.state, car.headlights, car.doors, car.people))
            search_window.destroy()

        search_button = tk.Button(search_window, text="Поиск", command=search_cars)
        search_button.grid(row=9, columnspan=2)

    def append_car(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить машину")

        tk.Label(add_window, text="Марка:").grid(row=0,column=0 )
        brand_combobox = ttk.Combobox(add_window ,values=list(self.BRANDS_MODELS.keys()))
        brand_combobox.grid(row=0,column=1 )

        tk.Label(add_window ,text="Модель:").grid(row=1,column=0 )
        model_combobox = ttk.Combobox(add_window )
        model_combobox.grid(row=1,column=1 )

        def upd_models(event):
            brand = brand_combobox.get()
            model_combobox['values'] = self.BRANDS_MODELS.get(brand ,[])
            model_combobox.set('')

        brand_combobox.bind("<<ComboboxSelected>>" ,upd_models)

        tk.Label(add_window ,text="Цвет:").grid(row=2,column=0 )
        color_combobox = ttk.Combobox(add_window ,values=self.COLORS)
        color_combobox.grid(row=2,column=1 )

        tk.Label(add_window ,text="Коробка передач:").grid(row=3,column=0 )
        transmission_combobox = ttk.Combobox(add_window ,values=["Автомат" ,"Механика"])
        transmission_combobox.grid(row=3,column=1 )

        tk.Label(add_window ,text="Двигатель:").grid(row=4,column=0 )
        engine_combobox = ttk.Combobox(add_window ,values=["Бензин" ,"Дизель" ,"Электро"])
        engine_combobox.grid(row=4,column=1 )

        tk.Label(add_window ,text="Состояние:").grid(row=5,column=0 )
        state_combobox = ttk.Combobox(add_window ,values=["Заведена" ,"Не заведена"])
        state_combobox.grid(row=5,column=1 )

        tk.Label(add_window ,text="Фары:").grid(row=6,column=0 )
        headlights_combobox = ttk.Combobox(add_window ,values=["Включены" ,"Выключены"])
        headlights_combobox.grid(row=6,column=1 )

        tk.Label(add_window ,text="Двери:").grid(row=7,column=0 )
        doors_combobox = ttk.Combobox(add_window ,values=["Закрытые" ,"Открытые"])
        doors_combobox.grid(row=7,column=1 )

        tk.Label(add_window ,text="Люди в машине:").grid(row=8,column=0 )
        people_combobox = ttk.Combobox(add_window ,values=["Есть", "Нет"])
        people_combobox.grid(row=8,column=1 )


        def save_car():
            new_car = Car(
                brand_combobox.get(),
                model_combobox.get(),
                color_combobox.get(),
                transmission_combobox.get(),
                engine_combobox.get(),
                state_combobox.get(),
                headlights_combobox.get(),
                doors_combobox.get(),
                people_combobox.get()
            )
            self.manager.add_car(new_car)
            self.upd_cars_table()
            add_window.destroy()

        save_button = tk.Button(add_window, text="Сохранить", command=save_car)
        save_button.grid(row=9,columnspan=2 )

    def upd_car(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item[0])
            update_window = tk.Toplevel(self.root)
            update_window.title("Изменить машину")

            car = self.manager.get_cars()[index]

            tk.Label(update_window ,text=f"Марка:{car.brand}").grid(row=0,column=0 )


            tk.Label(update_window ,text=f"Модель: {car.model}").grid(row=1,column=0 )




            tk.Label(update_window ,text="Цвет:").grid(row=2,column=0 )
            color_combobox = ttk.Combobox(update_window ,values=self.COLORS)
            color_combobox.set(car.color)
            color_combobox.grid(row=2,column=1 )

            tk.Label(update_window ,text="Коробка передач:").grid(row=3,column=0 )
            transmission_combobox = ttk.Combobox(update_window ,values=["Автомат" ,"Механика"])
            transmission_combobox.set(car.transmission)
            transmission_combobox.grid(row=3,column=1 )

            tk.Label(update_window ,text="Двигатель:").grid(row=4,column=0 )
            engine_combobox = ttk.Combobox(update_window ,values=["Бензин" ,"Дизель" ,"Электро"])
            engine_combobox.set(car.engine)
            engine_combobox.grid(row=4,column=1 )

            tk.Label(update_window ,text="Состояние:").grid(row=5,column=0 )
            state_combobox = ttk.Combobox(update_window ,values=["Заведена" ,"Не заведена"])
            state_combobox.set(car.state)
            state_combobox.grid(row=5,column=1 )

            tk.Label(update_window ,text="Фары:").grid(row=6,column=0 )
            headlights_combobox = ttk.Combobox(update_window ,values=["Включены" ,"Выключены"])
            headlights_combobox.set(car.headlights)
            headlights_combobox.grid(row=6,column=1 )

            tk.Label(update_window ,text="Двери:").grid(row=7,column=0 )
            doors_combobox = ttk.Combobox(update_window ,values=["Закрытые" ,"Открытые"])
            doors_combobox.set(car.doors)
            doors_combobox.grid(row=7,column=1 )

            tk.Label(update_window ,text="Люди в машине:").grid(row=8,column=0 )
            people_combobox = ttk.Combobox(update_window ,values=["Есть", "Нет"])
            people_combobox.set(car.people)
            people_combobox.grid(row=8,column=1 )

            def save_upded_car():
                updated_car = Car(
                    brand_combobox.get(),
                    model_combobox.get(),
                    color_combobox.get(),
                    transmission_combobox.get(),
                    engine_combobox.get(),
                    state_combobox.get(),
                    headlights_combobox.get(),
                    doors_combobox.get(),
                    people_combobox.get()
                )
                self.manager.update_car(index, updated_car)
                self.upd_cars_table()
                update_window.destroy()

            save_button = tk.Button(update_window ,text="Сохранить изменения" ,command=save_upded_car )
            save_button.grid(row=8,columnspan=2 )

    def pop_car(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item[0])
            self.manager.remove_car(index)
            self.upd_cars_table()
        else:
            messagebox.showwarning("Предупреждение" ,"Сначала выберите машину для удаления." )