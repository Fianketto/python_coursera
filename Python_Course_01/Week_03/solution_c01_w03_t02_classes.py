import csv

CAR = "car"
TRUCK = "truck"
SPEC_MACHINE = "spec_machine"
VALID_CAR_TYPES = [CAR, TRUCK, SPEC_MACHINE]


class CarBase:
    def __init__(self, brand: str, photo_file_name: str, carrying: float):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
        self.car_type = None

    @staticmethod
    def parse_list(row: list) -> list:
        try:
            car_type = row[0]
            car_brand = row[1]
            car_photo_file_name = row[3]
            car_carrying = float(row[5])
            photo_file_name_parts = car_photo_file_name.split(".")
            file_name, file_ext = photo_file_name_parts[0], photo_file_name_parts[-1]
            parsed_row = [car_type, car_brand, car_photo_file_name, car_carrying]
            assert car_brand and car_photo_file_name.count(".") == 1 and file_name and file_ext and car_carrying
            if car_type == CAR:
                car_passenger_seats_count = int(row[2])
                parsed_row.append(car_passenger_seats_count)
                assert row[2] and not row[4] and not row[6]
            elif car_type == TRUCK:
                car_body_whl = row[4]
                parsed_row.append(car_body_whl)
                assert not row[2] and not row[6]

            elif car_type == SPEC_MACHINE:
                car_extra = row[6]
                parsed_row.append(car_extra)
                assert row[6] and not row[2] and not row[4]
            if car_type in VALID_CAR_TYPES:
                return parsed_row
            return []
        except BaseException:
            pass
        return []

    def get_photo_file_ext(self) -> str:
        file_ext = "." + self.photo_file_name.split(".")[-1]
        return file_ext


class Car(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carrying: float, passenger_seats_count: int):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = CAR
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carrying: float, body_whl: str):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = TRUCK
        self.body_whl = body_whl
        self.body_length, self.body_width, self.body_height = self.parse_body_whl()
        self.volume = self.body_length * self.body_width * self.body_height

    def parse_body_whl(self) -> tuple:
        try:
            l, w, h = tuple(map(float, self.body_whl.split("x")))
        except BaseException:
            l = w = h = 0.0
        return l, w, h

    def get_body_volume(self) -> float:
        return self.volume


class SpecMachine(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carrying: float, extra: str):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = SPEC_MACHINE
        self.extra = extra


def get_valid_row_list(csv_filename: str) -> list:
    row_list = []
    with open(csv_filename, encoding="utf-8") as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            parsed_row = CarBase.parse_list(row)
            if parsed_row:
                row_list.append(parsed_row)
    return row_list


def get_car_list(csv_filename: str) -> list:
    row_list = get_valid_row_list(csv_filename)
    #print(row_list)
    car_list = []
    for row in row_list:
        car = make_new_car(row)
        car_list.append(car)
    return car_list


def make_new_car(row):
    new_car = None
    if row[0] == CAR:
        new_car = Car(*row[1:])
    elif row[0] == TRUCK:
        new_car = Truck(*row[1:])
    elif row[0] == SPEC_MACHINE:
        new_car = SpecMachine(*row[1:])
    return new_car


if 0:
    my_car_list = get_car_list("cars.csv")
    for car in my_car_list:
        print(car.brand)
        print(car.get_photo_file_ext())
        print(car.carrying, type(car.carrying))
        if isinstance(car, Truck):
            print(car.volume)
            print(car.get_body_volume())
        if isinstance(car, Car):
            print(car.passenger_seats_count, type(car.passenger_seats_count))
        print("\n")
