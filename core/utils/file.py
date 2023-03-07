import json
import os


class File:
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.file_path = ""
        self.contents = ""

    # todo:change this name
    def set_stub_path(self, name):
        # Construct the file path
        self.file_path = os.path.join(self.script_dir, name)

    def get_file_content(self):
        # Open the file in read mode
        with open(self.file_path) as file:
            # Read the contents of the file
            self.contents = file.read()

    def set_json_content(self, my_list):
        # Open the file in read mode
        with open(self.file_path,'w') as file:
            # Read the contents of the file
            json.dump(my_list, file)

    def get_json_content(self):
        # Open the file in read mode
        with open(self.file_path, 'w') as file:
            # Read the contents of the file
            my_list = json.load(file)
        return my_list
