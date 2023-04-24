class Car:
    def __init__(self, **kwargs):
        self.attrs = kwargs
        self.attrs['engine'] = None
        self.attrs['fuel'] = None
        self.attrs['wheel'] = None
        self.attrs['trans'] = None
        self.attrs['run'] = None
        self.set_characters_attr()

    def print_car(self):
        for item, value in self.attrs.items():
            if item == 'characters':
                continue
            print(f"{item}: {value}")
        print('_______________________________________________________________________________________\n')

    def set_characters_attr(self):
        lst_character = self.attrs['characters']
        for item in lst_character:
            if item in ['передний', 'задний', '4WD']:
                self.attrs['wheel'] = item
            elif 'л.с.' in item:
                self.attrs['engine'] = item
            elif item in ['АКПП', 'механика', 'робот', 'вариатор']:
                self.attrs['trans'] = item
            elif item in ['бензин', 'дизель', 'гибрид', 'электро']:
                self.attrs['fuel'] = item
            elif 'км' in item:
                self.attrs['run'] = item
        # if 'fuel' not in self.attrs.keys():
        #     self.attrs['fuel'] = None
        # if 'run' not in self.attrs.keys():
        #     self.attrs['run'] = None
        # if 'trans' not in self.attrs.keys():
        #     self.attrs['trans'] = None
        # if 'wheel' not in self.attrs.keys():
        #     self.attrs['wheel'] = None
        # if 'engine' not in self.attrs.keys():
        #     self.attrs['engine'] = None

    def get_attrs(self):
        return self.attrs
