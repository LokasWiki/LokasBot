import os


class File:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.file_path = ""
        self.contents = ""

    def set_stub_path(self, name):
        # Construct the file path
        self.file_path = os.path.join(self.script_dir, name)

    def get_file_content(self):
        # Open the file in read mode
        with open(self.file_path) as file:
            # Read the contents of the file
            self.contents = file.read()
