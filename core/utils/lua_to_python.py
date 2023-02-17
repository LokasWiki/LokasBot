import os
import re

from core.utils.regex_scanner import RequestsScanner

portal_aliases_file_name = "portal_aliases.txt"

def save_lue_table(name,text):
    home_path = os.path.expanduser("~")
    lue_path = os.path.join(home_path, name)
    with open(lue_path, 'w') as f:
        f.write(text)


def get_lue_table(name):
    home_path = os.path.expanduser("~")
    lue_path = os.path.join(home_path, name)
    with open(lue_path) as f:
        content = f.read()
    return content


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

        if self.data.items() == 0:
            self._parse_table()

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



