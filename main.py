import pandas as pd
from mimesis import Locale, Generic
from generation_of_person import PersonProvider
from generation_of_cards import CardProvider
from generation_of_train import TrainProvider

exsit_type_of_train = {
    "Стандарт" : ["1С", "1Р", "1В", "2Р", "2Е", "3Э", "3Э", "3Э", "2Э", "1Б", "1Л", "1А", "1И"],
    "Сапсан" : ["1Р", "1Р", "2С", "2С", "2С", "2С", "2С", "2С", "2С", "2С", "2С", "2С"], 
    "Стриж" : ["1Р", "1Е", "1Р", "2С", "2С", "2С", "2С", "2С", "2С"]
}
sale_for_tickets = {
    "Сапсан": {
      "1Р" : 2000,
      "1В" : 1600,
      "1С" : 2400,
      "2С" : 1000,
      "2В" : 1200,
      "2Е" : 0 
    },
    "Стриж" : {
      "1Е" : 3000,
      "1Р" : 1400,
      "2С" : 800
    },
    
    "Стандарт" : {
      "1С": 600, 
      "1Р": 700,
      "1В": 800,
      "2Р": 900,
      "2Е": 400,
      "3Э": 500,
      "2Э": 1200,
      "1Б": 2000,
      "1Л": 2200,
      "1А": 2400,
      "1И": 2400
    }
}
if __name__ == "__main__":
    used_train = set()
    cnt_of_passengers = 0

    names = []
    passports = []
    seats = []
    trips = []
    cards = []
    arrived_times = []
    departure_times = []
    costs = []
    count_of_tickets = 75000

    generic = Generic(locale=Locale.RU)
    generic.add_providers(PersonProvider, CardProvider, TrainProvider)
    while cnt_of_passengers <= count_of_tickets:
        train, rand_symbol_trip = generic.generation_trains.create_random_number_trip()
        trip = str(train).zfill(3) + rand_symbol_trip
        while trip in used_train:
            train, rand_symbol_trip = generic.generation_trains.create_random_number_trip()
        used_train.add(trip)
        train_type, distance, intervals = generic.generation_trains.create_trip(train)
        for k in range(len(intervals)):
            if cnt_of_passengers >= count_of_tickets:
                break
            start = intervals[k][0]
            finish = intervals[k][1]
            if k % 2 == 0:
                number_of_train = str(train).zfill(3) + rand_symbol_trip
            else:
                number_of_train = trip = str(train + 1).zfill(3) + rand_symbol_trip
            for i in range(len(exsit_type_of_train[train_type])):
                car = exsit_type_of_train[train_type][i]
                if car[0] == '1':
                    for seat in range(1, 21):
                        names.append(generic.generation_names.create_names())
                        passports.append(generic.generation_names.create_passport_data())
                        trips.append(number_of_train)
                        costs.append(distance * sale_for_tickets[train_type][car] // 100)
                        cards.append(generic.generation_cards.create_cards())
                        seats.append(str(i + 1) + "-" + str(seat))
                        departure_times.append(start)
                        arrived_times.append(finish)
                    cnt_of_passengers += 20
                elif car[0] == '2':
                    for seat in range(1, 37):
                        names.append(generic.generation_names.create_names())
                        passports.append(generic.generation_names.create_passport_data())
                        trips.append(number_of_train)
                        costs.append(distance * sale_for_tickets[train_type][car] // 100)
                        cards.append(generic.generation_cards.create_cards())
                        seats.append(str(i + 1) + "-" + str(seat))
                        departure_times.append(start)
                        arrived_times.append(finish)
                    cnt_of_passengers += 36
                elif car[0] == '3':
                    for seat in range(1, 57):
                        names.append(generic.generation_names.create_names())
                        passports.append(generic.generation_names.create_passport_data())
                        trips.append(number_of_train)
                        costs.append(distance * sale_for_tickets[train_type][car] // 100)
                        cards.append(generic.generation_cards.create_cards())
                        seats.append(str(i + 1) + "-" + str(seat))
                        departure_times.append(start)
                        arrived_times.append(finish)
                    cnt_of_passengers += 56
    print("End generation")
    df = pd.DataFrame.from_dict({
        "ФИО" : names,
        "Паспорт" : passports,
        "Рейс" : trips,
        "Место" : seats,
        "Время отъезда" : departure_times,
        "Время приезда" : arrived_times,
        "Цена билета" : costs,
        "Карта оплаты" : cards
    })
    df.to_csv('output.csv', index=False)  
    df.to_excel("output.xlsx") 
    print("End write")
