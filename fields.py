from abc import abstractmethod


class Field():
    def __init__(self, default):
        self.default = default


    @property
    def default(self):
        return self._default

    @default.setter
    @abstractmethod
    def default(self, value):
        pass

    @abstractmethod
    def check(self, value):
        pass


class CharField(Field):
    def __init__(self, min_length=0, max_length=100, default=''):
        self.min = min_length
        self.max = max_length
        super().__init__(default)

    def __repr__(self):
        return "TEXT"

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value
        if self.min > len(value):
            self._default += ' ' * (self.min - len(value))
        elif self.max < len(value):
            self._default = value[0:self.max]

    def check(self, value):
        if not isinstance(value, str):
            raise ValueError(
                f'CharField: Value {value} must be of string type')
        if len(value) < self.min:
            raise ValueError(
                f'CharField: Value is too short ({len(value)} when more than {self.min} is needed)')
        if len(value) > self.max:
            raise ValueError(
                f'CharField: Value is too long ({len(value)} when less than {self.max} is needed)')


class IntegerField(Field):
    def __init__(self, min_value=-1000, max_value=999999999, default=0):
        self.min = min_value
        self.max = max_value
        super().__init__(default)

    def __repr__(self):
        return "INTEGER"

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        if self.min > value:
            self._default = self.min
        elif self.max < value:
            self._default = self.max
        else:
            self._default = value

    def check(self, value):
        if not isinstance(value, int):
            raise ValueError(
                f'IntegerField: Value {value} must be of integer type')
        if value < self.min:
            raise ValueError(
                f'IntegerField: Value is too small ({value} when more than {self.min} is needed)')
        if value > self.max:
            raise ValueError(
                f'IntegerField: Value is too big ({value} when less than {self.max} is needed)')
