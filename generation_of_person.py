import pandas as pd
from pathlib import Path
from mimesis import BaseDataProvider
from mimesis.locales import Locale

class PersonProvider(BaseDataProvider):
    class Meta:
        name = 'generation_names'
        datafile = 'names.json'
        datadir = Path(__file__).parent / 'datasets'

    #Создание имени, отчества, фамилии
    def create_names(self):
        gender = self.random.randint(0, 1)

        if gender == 0:
            first_name = self.random.choice(self._extract(['male_names']))
            middle_name = self.random.choice(self._extract(['male_patronymics']))
            last_name = self.random.choice(self._extract(['male_surnames']))
        else:
            first_name = self.random.choice(self._extract(['female_names']))
            middle_name = self.random.choice(self._extract(['female_patronymics']))
            last_name = self.random.choice(self._extract(['female_surnames']))
        lfm = [last_name, first_name, middle_name] #Фамилия, Имя, Отчество
        return " ".join(lfm)
    def create_passport_data(self):
        number = self.random.randint(1000, 9999)
        series = self.random.randint(100000, 999999)
        s = str(number) + " " + str(series)
        return s


cdp = PersonProvider(Locale.RU)
cdp.create_names()
