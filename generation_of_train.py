from pathlib import Path
import math
from mimesis import BaseDataProvider
from mimesis.locales import Locale
from datetime import datetime
from datetime import timedelta
    
class TrainProvider(BaseDataProvider):
    class Meta:
        name = 'generation_trains'
        datafile = 'city.json'
        datadir = Path(__file__).parent / 'datasets'

    def _calculate_the_distance(self, start_city, end_city):
        EARTH_RADIUS = 6378 

        latitude1 = start_city["latitude"]
        latitude2 = end_city["latitude"]
        longitude1 = start_city["longitude"]
        longitude2 = end_city["longitude"]

        # Перевести координаты в радианы
        lat1 = math.radians(latitude1)
        lat2 = math.radians(latitude2)
        long1 = math.radians(longitude1)
        long2 = math.radians(longitude2)

        # Косинусы и синусы широт и разницы долгот
        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        # Вычисления длины большого круга
        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cdelta

        ad = math.atan2(y, x)
        dist = ad * EARTH_RADIUS

        return dist

    def _determine_train_speed(self, train_number):
        if 1 <= train_number <= 150:
            return 70  # Скорые поезда (70 км/ч)
        elif 151 <= train_number <= 300:
            return 70  # Скорые поезда сезонного/разового назначения (70 км/ч)
        elif 301 <= train_number <= 450:
            return 60  # Пассажирские круглогодичные поезда (60 км/ч)
        elif 451 <= train_number <= 700:
            return 60  # Пассажирские поезда сезонного/разового назначения (60 км/ч)
        elif 701 <= train_number <= 750:
            return 91  # Скоростные поезда (91 км/ч)
        elif 751 <= train_number <= 788:
            return 161  # Высокоскоростные поезда (161 км/ч)
        else:
            return 404  # Другие номера поездов (например, 0 км/ч)
    # Выбор городов для маршрута
    def _create_path_of_train(self):
        start_city = self.random.choice(self._extract(['cities']))
        end_city = self.random.choice(self._extract(['cities']))
        
        while(start_city["city"] == end_city["city"]):
            end_city = self.random.choice(self._extract(['cities']))
        return start_city, end_city
    # Создание времени отъезда и приезда поезда
    def _create_randome_datetime(self, train_type, distance):
        start_time = 0
        month = 0
        hour = 0
        minute = 0
        end_time = datetime(2024, 1, 1)

        if 151 <= train_type <= 298 or 451 <= train_type <= 598:
            months = [1, 12, 6, 7, 8]
            month = self.random.choice(months)
        else:
            month = self.random.randint(1, 12)
        hour = self.random.randint(0, 23)
        minute = self.random.randint(0, 55)
        start_time = datetime(2024, month, 1, hour, minute)
        time_for_arrived = timedelta(hour = distance // self._determine_train_speed(train_type))
    
        end_time = start_time + time_for_arrived

        return start_time, end_time
    def create_random_number_trip(self):
        exist_group_of_trains = [range(2, 151, 2), range(152, 297, 2), range(302, 450, 2), range(452, 596, 2), range(702, 751, 2), range(752, 788, 2)]
        russian_alphabet = 'АБВГДЕЖЗИКЛМНОПРСТУФХЧШЭЮЯ'

        rand_group = self.random.choice(exist_group_of_trains)
        train = self.random.choice(rand_group)
        rand_symbol_trip = self.random.choice(russian_alphabet)

        return train, rand_symbol_trip

    def create_trip(self, train):
        #Интервалы между отправлением рейсов
        interval_between_trips = 2
    
        # Определяем тип поезда
        train_type = "" 
        if 1 <= train <= 750:
            train_type = 'Стандарт'
        elif 751 <= train <= 770:
            train_type = 'Сапсан'
        elif 771 <= train <= 788:
            train_type = 'Стриж'
        

        start_city, end_city = self._create_path_of_train()
        distance = self._calculate_the_distance(start_city, end_city)
        train_speed_mps = self._determine_train_speed(train)

        # Вычисление времени в пути
        travel_time = distance // train_speed_mps

        end_date = datetime(2024, 12, 31)
        if 151 <= train <= 298 or 451 <= train <= 598:
            months = [1, 12, 6, 7, 8]
            month = self.random.choice(months)
        else:
            month = self.random.randint(1, 12)
        hour = self.random.randint(0, 23)
        minute = self.random.randint(0, 55)
        start_date = datetime(2024, month, 1, hour, minute)
        
        intervals = []
        while start_date <= end_date:
            arrival_time = start_date + timedelta(hours=travel_time)
            
            intervals.append((start_date, arrival_time))
            # Создание строки расписания для маршрута B->A (обратного)
            reverse_departure_time = arrival_time + timedelta(minutes=self.random.randint(30, 180))
            reverse_arrival_time = reverse_departure_time + timedelta(hours=travel_time)
            
            intervals.append((reverse_departure_time, reverse_arrival_time))

            start_date = reverse_arrival_time + timedelta(days=interval_between_trips)

        return train_type, distance, intervals
        
