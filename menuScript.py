
import pyzipper
# import py7zr
from py7zr import SevenZipFile
from py7zr.callbacks import ExtractCallback
from rich.progress import Progress
import os
import sys
import time


work_path = os.getcwd()
# print("work>>",work_path)

# 程序运行时的目录
exe_path = os.path.dirname(sys.argv[0])
# print("exe>>",exe_path)

password_path = os.path.join(exe_path, "passwords.txt")

passwords = []

if not os.path.exists(password_path):
    with open(password_path, "w") as f:
        f.write("bili codejack\n")



# 写入本地压缩密码
def save_password(password):
    if password in passwords or not password or password == "noreqpasswordbybilicodejack":
        return
    # 追加写入
    with open(password_path, "a") as f:
        f.write(password + "\n")


# 读取本地压缩密码 并去除换行符
def read_passwords():
    global passwords
    with open(password_path, "r") as f:
        passwords = list(set([line.strip() for line in f.readlines()]))




def identify_file_type(file_path):
    signatures = {
        b'PK\x03\x04': 'ZIP',
        # b'Rar!\x1a\x07\x00': 'RAR', # RAR格式没办法支持 
        # b'Rar!\x1a\x07\x01\x00': 'RAR5',  # 添加RAR 5.0的签名
        b'7z\xbc\xaf\x27\x1c': '7z',
    }
    with open(file_path, 'rb') as file:
        file_signature = file.read(max(len(sig) for sig in signatures))
    for signature, file_type in signatures.items():
        if file_signature.startswith(signature):
            return file_type
    return "Unknown file type"



def last3_exit():
    # 倒计时三秒关闭
    t = 3
    for i in range(3):
        print(f"（＞人＜；） 倒计时{t-i}秒  后关闭")
        time.sleep(1)


PAS_password = ""
def unzip_file(zip_path, extract_to):
    global PAS_password
    zip_file = pyzipper.AESZipFile(zip_path)
    zip_file.setpassword(PAS_password.encode('utf-8'))
    try:
        zip_file.testzip()
        if not PAS_password:
            PAS_password = "noreqpasswordbybilicodejack"
    except Exception as e:
        PAS_password = ""
        if "password required" in str(e):
            for password in passwords:
                try:
                    zip_file.setpassword(password.encode('utf-8'))
                    zip_file.testzip()
                    PAS_password = password
                    break
                except Exception as e:
                    continue

    if not PAS_password:
        print("密码错误 请自行输入一次密码 下次所有使用该软件的用户就都不需要输入这个密码了")
        PAS_password = input("请输入密码:")
        unzip_file(zip_path, extract_to)
        return
    
    # 获取所有文件的列表
    list_of_files = zip_file.namelist()
    total_size = sum([zip_file.getinfo(name).file_size for name in list_of_files])
    progress = Progress()
    progress_bar = progress.add_task("[red]（＞人＜；）解压中 请稍等", total=total_size)
    progress.start()
    # 逐个解压文件
    for file in list_of_files:
        file_info = zip_file.getinfo(file)
        extracted_path = zip_file.extract(file, path=extract_to)
        progress.update(progress_bar, advance=file_info.file_size)
        # 尝试修正中文乱码
        try:
            correct_filename = None
            try:
                correct_filename = file.encode('cp437').decode('gbk')
            except:
                correct_filename = file.encode('cp437').decode('utf-8')
            correct_path = os.path.join(extract_to, correct_filename)
            if extracted_path != correct_path:
                os.rename(extracted_path, correct_path)
        except Exception as e:
            continue
    progress.stop()
    # 追加压缩密码
    save_password(PAS_password)
    print("\n \033[1;32mヽ(*。>Д<)o゜解压完成\033[0m \n")
    # 倒计时三秒关闭
    last3_exit()
    sys.exit(0)

        


class MyExtractCallback(ExtractCallback):
    def __init__(self, total_size):
        super().__init__()
        # 初始化进度条
        self.total_size = int(total_size)
        self.progress = Progress()
        self.progress_bar = self.progress.add_task("[red]（＞人＜；）解压中 请稍等", total=total_size)
        self.progress.start()


    def report_start(self, processing_file_path, processing_bytes):
        pass


    def report_update(self, decompressed_bytes):
        self.progress.update(self.progress_bar, advance=int(decompressed_bytes))
        pass


    def report_end(self, processing_file_path, wrote_bytes):
        pass


    def report_warning(self):
        # print("report_warning")
        pass
    
    def report_postprocess(self):
        # print("report_postprocess")
        self.progress.update(self.progress_bar, advance=self.total_size)
        self.progress.stop()

    def report_start_preparation(self):
        # print("report_start_preparation")
        pass


def u7z_extract_all(archive, path):
    # 红色输出
    print("\n \033[1;31m（＞人＜；）解压中 请稍等\033[0m \n")
    archive.extractall(path=path)
    # archive.ex
    print("\n \033[1;32mヽ(*。>Д<)o゜解压完成\033[0m \n")
    # # 追加压缩密码
    save_password(PAS_password)
    # # 倒计时三秒关闭
    last3_exit()
    sys.exit(0)


def unzip_7z_file(file_path, output_path):
    global PAS_password
    try:
        archive = SevenZipFile(file_path, mode='r', password=PAS_password)
        if not PAS_password:
            PAS_password = "noreqpasswordbybilicodejack"
    except Exception as e:
        PAS_password = ""
        if "Corrupt input data" in str(e):
            for password in passwords:
                try:
                    archive = SevenZipFile(file_path, mode='r', password=password)
                    PAS_password = password
                    u7z_extract_all(archive, output_path)
                    return
                except Exception as e:
                    PAS_password = ""
                    continue
            
    if not PAS_password:
        print("密码错误 请自行输入一次密码 下次所有使用该软件的用户就都不需要输入这个密码了")
        PAS_password = input("请输入密码:")
        unzip_7z_file(file_path, output_path)
        return
    
    u7z_extract_all(archive, output_path)
    

if __name__ == "__main__":
    read_passwords()

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        output_path = "CodeJackOutPut"
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        else:
            output_path = f"CodeJackOutPut_{time.strftime('%Y%m%d%H%M%S')}"
            os.mkdir(output_path)

        type_name = identify_file_type(file_path)
        if type_name == "ZIP":
            unzip_file(file_path, output_path)
        elif type_name == "7z":
            unzip_7z_file(file_path, output_path)
        else:
            print("不支持的文件格式")
            last3_exit()