class FileWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Create the file if it doesn't exist
        with open(self.file_path, 'a+') as file:
            pass  # No need to do anything, just ensure the file is created

    def writefile(self, content: str):
        with open(self.file_path, 'a') as file:
            file.write(content + '\n')