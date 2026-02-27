class Player:
    _name = None
    _number = None
    _is_manager = None
    _title = None
    _classification = None
    _translated_value = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def page_title(self) -> str:
        if not self._name.strip().startswith("[["):
            return self._name
        temp_name = self.name.replace("[[", "").replace("]]", "").strip()
        return temp_name.split("|")[0] if len(temp_name.split("|")) > 0 else temp_name

    @property
    def classification(self) -> str:
        return self._classification

    @property
    def translated_value(self) -> str:
        return self._translated_value

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
        self._number = int(value) if type(value) is str else value

    @is_manager.setter
    def is_manager(self, value):
        self._is_manager = bool(value)

    @title.setter
    def title(self, value):
        self._title = value

    @classification.setter
    def classification(self, value):
        self._classification = value

    @translated_value.setter
    def translated_value(self, value):
        self._translated_value = value
