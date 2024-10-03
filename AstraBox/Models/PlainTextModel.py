

class PlainTextModel:
    def __init__(self, name) -> None:
        self.name = name
        self.text_lines = None


    def try_decode(self, data:bytearray):
        for encoding in ['utf-8', 'ascii', 'cp866']:
            try:
                lines = data.decode(encoding)
                break
            except UnicodeDecodeError as e:
                print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
        print(f'good encoding {encoding}')
        return lines
    
    def set_text_from_bytearray(self, data):

        self.text_lines = self.try_decode(data)

    def get_text(self):
        return self.text_lines     