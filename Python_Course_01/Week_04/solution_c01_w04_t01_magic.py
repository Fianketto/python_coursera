import os
import tempfile


class File:
    file_count = 0

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines = []
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass
        self.update_iter_items()

    def __str__(self):
        return self.file_path

    def __add__(self, other_file):
        File.file_count += 1
        new_file_path = os.path.join(tempfile.gettempdir(), str(File.file_count) + "_my_file.txt")
        # new_file_path = os.path.join(str(File.file_count) + "_my_file.txt")
        new_content = self.read() + other_file.read()
        new_file = File(new_file_path)
        new_file.write(new_content)
        return new_file

    def __iter__(self):
        return (x for x in self.lines)

    def update_iter_items(self):
        with open(self.file_path, 'r') as f:
            self.lines = f.readlines()

    def read(self):
        try:
            with open(self.file_path, 'r') as f:
                file_content = f.read()
        except BaseException:
            file_content = ""
        return file_content

    def write(self, new_content: str):
        with open(self.file_path, 'w') as f:
            print(new_content, file=f, end="")
        self.update_iter_items()
        return len(new_content)
