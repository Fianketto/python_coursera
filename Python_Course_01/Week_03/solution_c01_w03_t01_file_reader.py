class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self):
        try:
            f = open(self.file_path, 'r')
            result_string = f.read()
        except BaseException:
            result_string = ""
        return result_string
