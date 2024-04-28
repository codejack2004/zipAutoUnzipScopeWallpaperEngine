import sys
import os
import time
from utils.zipTools import identify_file_type, find_zip_password, find_7z_password
from utils.bandizip import unzip_file, last3_exit


def create_output_folder():
    output_path = "CodeJackOutPut"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    else:
        output_path = f"CodeJackOutPut_{time.strftime('%Y%m%d%H%M%S')}"
        os.mkdir(output_path)
    return output_path

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        file_type = identify_file_type(file_path)
        match file_type:
            case "ZIP":
                password = find_zip_password(file_path)
                if password == 2005:
                    unzip_file(file_path, create_output_folder())
                elif type(password) == str:
                    unzip_file(file_path, create_output_folder(), password)
            case "7z":
                password = find_7z_password(file_path)
                if password == 2005:
                    unzip_file(file_path, create_output_folder())
                elif type(password) == str:
                    unzip_file(file_path, create_output_folder(), password)
            case _:
                print("不支持的文件类型！")
                last3_exit()



if __name__ == '__main__':
    main()
    