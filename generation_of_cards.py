import pandas as pd
from pathlib import Path
from mimesis import BaseDataProvider, Gender
from mimesis.locales import Locale
import json

class CardProvider(BaseDataProvider):
    class Meta:
        name = 'generation_cards'
        datafile = 'cards.json'
        datadir = Path(__file__).parent / 'datasets'
        
    def __randomize_card_information(self):
        templates = ""
        with open('datasets/en/random_cards.json') as f:
            templates = json.load(f) 
        cards = self._extract(['cards'])
        bank_num = "" # Номер идентифицируешь банк и платёжную систему
        card_system = self.random.weighted_choice(
            choices = templates["card_system"]
        )
        bank = self.random.weighted_choice(
            choices = templates["bank"]
        )
        try:
            bank_num = self.random.choice([cards[card_system][bank]])
        except:
            pass
        return bank_num

    #Создание 16 цифр банковской карты
    def create_cards(self):
        bank_num = self.__randomize_card_information()
        while bank_num == "":
            bank_num = self.__randomize_card_information()
        card = ""
        bank_num = self.random.choice(list(bank_num.values()))[0]
        card += str(bank_num)
        tail_of_numbers_of_card = str(self.random.randint(1000000000, 9999999999)) # Генерация оставшихся 12 цифр
        card += tail_of_numbers_of_card
        card = card[0:4] + " " + card[4:8] + " " + card[8:12] + " " + card[12:16] # Маска для формат карты
        return card