import tarfile
import os
import tempfile

class Compress:
    def __init__(self):
        pass
    
    def check_temp_dir(self) -> None:
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
    
    def compress_file(self, file_path : str) -> str:
        self.check_temp_dir()
        tar_path = f".{tempfile.NamedTemporaryFile().name}.tar.gz"
         
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(file_path)
        tar.close()
        
        return tar_path