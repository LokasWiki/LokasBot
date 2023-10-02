class Player:
    _name = None
    _number = None
    _is_manager = None
    _title = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def number(self) -> int:
        return self._number

    @property
    def is_manager(self) -> bool:
        return self._is_manager

    @property
    def title(self) -> str:
        return self.title

    @property
    def has_number(self) -> bool:
        return bool(self._number)

    @property
    def has_title(self) -> bool:
        return bool(self._title)

    @name.setter
    def name(self, value):
        self._name = str(value)

    @number.setter
    def number(self, value):
        self._number = int(value) if type(value) is int else None

    @is_manager.setter
    def is_manager(self, value):
        self._is_manager = bool(value)

    @title.setter
    def title(self, value):
        self._title = value
