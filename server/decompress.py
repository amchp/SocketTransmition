import tarfile
import os
import tempfile

class Decompress:
    def __init__(self):
        pass
    
    def check_files_dir(self) -> None:
        if not os.path.exists("files"):
            os.mkdir("files")
    
    def check_temp_dir(self) -> None:
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
    
    def decompress_data(self, data : bytes) -> str:
        self.check_temp_dir()
        self.check_files_dir()
        
        tar_path = f".{tempfile.NamedTemporaryFile().name}.tar.gz"
        with open(tar_path, "wb") as file:
            file.write(data)
        file.close()
         
        with tarfile.open(tar_path, "r:*") as tar:
            for member in tar.getmembers():
                if member.isdir():
                    continue 
                 
                temporal_file = tempfile.NamedTemporaryFile().name
                temporal_file = os.path.basename(temporal_file)
                
                member.name = temporal_file + os.path.basename(member.name)
                print(member.name)
                
                tar.extract(member, "files")
                    
        os.remove(tar_path)
        
        return tar_path
        
        
            
        