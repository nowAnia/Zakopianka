from datetime import timedelta

import requests


class Car:
    def __init__(self, speed, licence):
        self.speed = speed
        self.licence = licence

    def run(self, tunnel_id, tunnel_length, enter_time):
        print(f'Car with number of licence: {self.licence} enter the tunnel and drive: {self.speed} at {enter_time}')
        exit_time = enter_time + timedelta(hours=(tunnel_length / self.speed))
        exit_time_text = exit_time.strftime('%Y-%m-%d %H:%M:%S')
        self.__send_enter_car_drive_request(tunnel_id, enter_time)
        self.__send_exit_car_drive_request(tunnel_id, exit_time_text)

    def __send_enter_car_drive_request(self, tunnel_id, enter_time):
        enter_car_url = "http://localhost:5000/enter_car_drives"
        data = f"licence={self.licence}&enter_datetime={enter_time}&tunnel_id={tunnel_id}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(enter_car_url, data=data, headers=headers)
        return response

    def __send_exit_car_drive_request(self, tunnel_id, exit_time_text):
        exit_car_url = "http://localhost:5000/exit_car_drives"
        data = f"licence={self.licence}&exit_datetime={exit_time_text}&tunnel_id={tunnel_id}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.put(exit_car_url, data=data, headers=headers)
        return response
