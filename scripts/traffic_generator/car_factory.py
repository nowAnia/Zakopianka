import random
from car import Car

CITY_PREFIXES = ["SK", "KNT", "WE", "SL", "FE", "LI"]


class CarFactory:
    def __init__(self, start_time):
        self.start_time = start_time

    def run(self, tunnel_id, tunnel_length):
        random_licence = random.choice(CITY_PREFIXES) + str(random.randint(1233253, 6547835))
        car_speed = random.randint(40, 120)

        car = Car(speed=car_speed, licence=random_licence)
        car.run(tunnel_id, tunnel_length, self.start_time)
