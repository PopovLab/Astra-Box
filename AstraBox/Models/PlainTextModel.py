

from pathlib import Path

def try_decode(data:bytearray):
    for encoding in ['utf-8', 'ascii', 'cp866']:
        try:
            lines = data.decode(encoding)
            break
        except UnicodeDecodeError as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
    print(f'good encoding {encoding}')
    return lines

class PlainTextModel:
    def __init__(self, text_lines, file_path: Path):
        self.text_lines = text_lines
        self._file_path = file_path
        self.name = file_path.name

    @classmethod
    def from_file(cls, file_path):
        if file_path.exists():
            print(f'{file_path.name} exists!!')
            with file_path.open(mode= "rb") as file:
                data = file.read()
                text_lines = try_decode(data)
                
        return cls(text_lines, file_path)


    def get_text(self):
        return self.text_lines     