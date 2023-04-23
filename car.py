class Car:
    def __init__(self, **kwargs):
        self.attrs = kwargs
        self.set_characters_attr()

    def print_car(self):
        for item, value in self.attrs.items():
            if item == 'characters':
                continue
            print(f"{item}: {value}")
        print('_______________________________________________________________________________________\n')

    def set_characters_attr(self):
        lst_character = self.attrs['characters'].split(' | ')
        for item in lst_character:
            if 'передний' in item:
                self.attrs['wheel'] = 'передний'
            elif 'задний' in item:
                self.attrs['wheel'] = 'задний'
            elif '4WD' in item:
                self.attrs['wheel'] = 'полный'
            elif 'л.с.' in item:
                self.attrs['engine'] = lst_character[0]
            elif 'АКПП' in item:
                self.attrs['trans'] = 'автомат'
            elif 'механика' in item:
                self.attrs['trans'] = 'механика'
            elif 'робот' in item:
                self.attrs['trans'] = 'робот'
            elif 'вариатор' in item:
                self.attrs['trans'] = 'вариатор'
            elif 'бензин' in item:
                self.attrs['fuel'] = 'бензин'
            elif 'дизель' in item:
                self.attrs['fuel'] = 'дизель'
            elif 'гибрид' in item:
                self.attrs['fuel'] = 'гибрид'
            elif 'электро' in item:
                self.attrs['fuel'] = 'электрический'
            elif 'км' in item:
                self.attrs['run'] = lst_character[-1]

    def get_attrs(self):
        return self.attrs
