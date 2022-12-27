import zipfile

class ZipReader:
    def __init__(self, zip_file) -> None:
        self.zip_file = zip_file


    def get_file_list(self, folder):
        length = len(folder)
        with zipfile.ZipFile(self.zip_file) as zip:
            list =  [ z.filename for z in zip.filelist if (z.filename.startswith(folder)  and len(z.filename)>length )]
        list.sort()  
        return list        