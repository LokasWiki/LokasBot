import re

from core.utils.regex_scanner import RequestsScanner


class LuaToPython:
    def __init__(self, input_lua):
        self.input_lua = input_lua
        self.data = {}
        self._parse_table()

    def _parse_table(self):
        scanner = RequestsScanner()
        scanner.pattern = r"\[(?:\"|')(?P<key>.*?)(?:\"|')\]\s*=\s*(?P<value>\{[.|\w|\W]*?\})"
        scanner.scan(self.input_lua)

        if scanner.have_requests:
            for request in scanner.requests:
                self.data[request['key']] = self._parse_value(request['value'])

    def _parse_value(self,value):
        value_list = []
        scanner = RequestsScanner()
        scanner.pattern = r"(?:\"|')(?P<item>.*?)(?:\"|')"
        scanner.scan(value)
        if scanner.have_requests:
            for request in scanner.requests:
                value_list.append(request['item'])
        return value_list

    def search(self,search_item):
        name = None
        for item in self.data:
            if item == search_item:
                name = item
                break
            for value in self.data[item]:
                if search_item == value:
                    name = item
                    break
        return name
