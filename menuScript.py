
import pyzipper
# import py7zr
from py7zr import SevenZipFile
from py7zr.callbacks import ExtractCallback
from rich.progress import Progress
import os
import sys
import time


passwords = []


if not os.path.exists("passwords.txt"):
    with open("passwords.txt", "w") as f:
        f.write("bili codejack\n")

# 写入本地压缩密码
def save_password(password):
    if password == "noreqpasswordbybilicodejack":
        return
    if password in passwords:
        return
    # 追加写入
    with open("passwords.txt", "a") as f:
        f.write(password + "\n")

# 读取本地压缩密码 并去除换行符
def read_passwords():
    global passwords
    with open("passwords.txt", "r") as f:
        passwords = list(set([line.strip() for line in f.readlines()]))

PAS_password = ""

def unzip_file(zip_path, extract_to):
    global PAS_password
    # 打开ZIP文件
    with pyzipper.AESZipFile(zip_path) as zip_file:
        with Progress() as progress:
            # 获取所有文件的列表
            list_of_files = zip_file.namelist()
            total_size = sum([zip_file.getinfo(name).file_size for name in list_of_files])
            progress_bar = progress.add_task("[red]（＞人＜；）解压中 请稍等", total=total_size)
            # 逐个解压文件
            for file in list_of_files:
                file_info = zip_file.getinfo(file)
                extracted_path = None
                try:
                    extracted_path = zip_file.extract(file, path=extract_to, pwd=PAS_password.encode('utf-8'))
                    progress.update(progress_bar, advance=file_info.file_size)
                    PAS_password = "noreqpasswordbybilicodejack"
                except Exception as e:
                    print(e)
                    if "password required" in str(e):
                        for password in passwords:
                            try:
                                extracted_path = zip_file.extract(file, path=extract_to, pwd=password.encode('utf-8'))
                                PAS_password = password
                                break
                            except Exception as e:
                                continue
                    elif "Bad password" in str(e):
                        PAS_password = ""

                if not PAS_password:
                    print("密码错误 请自行输入一次密码 下次所有使用该软件的用户就都不需要输入这个密码了")
                    PAS_password = input("请输入密码:")
                    unzip_file(zip_path, extract_to)
                    continue

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
                    # print(e)
                    continue
                        
        print("\n \033[1;32mヽ(*。>Д<)o゜解压完成\033[0m \n")
        # 倒计时三秒关闭
        t = 3
        for i in range(3):
            print(f"（＞人＜；） 倒计时{t-i}秒  后关闭")
            time.sleep(1)

        # 追加压缩密码
        save_password(PAS_password)
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


def unzip_7z_file(file_path, output_path):
    global PAS_password
    try:
        archive = SevenZipFile(file_path, mode='r', password=PAS_password)
    except Exception as e:
        PAS_password = ""
        if "Corrupt input data" in str(e):
            # print("密码错误")
            for password in passwords:
                try:
                    archive = SevenZipFile(file_path, mode='r', password=password)
                    PAS_password = password
                    unzip_7z_file(file_path, output_path)
                    break
                except Exception as e:
                    continue
            
    if not PAS_password:
        print("密码错误 请自行输入一次密码 下次所有使用该软件的用户就都不需要输入这个密码了")
        PAS_password = input("请输入密码:")
        unzip_7z_file(file_path, output_path)
        return
    
    total_size = archive.archiveinfo().uncompressed
    call_back = MyExtractCallback(total_size)
    archive.extractall(path=output_path, callback=call_back)
    print("\n \033[1;32mヽ(*。>Д<)o゜解压完成\033[0m \n")
    # 倒计时三秒关闭
    t = 3
    for i in range(3):
        print(f"（＞人＜；） 倒计时{t-i}秒  后关闭")
        time.sleep(1)

    # 追加压缩密码
    save_password(PAS_password)
    sys.exit(0)


if __name__ == "__main__":
    read_passwords()
    # unzip_file(r"test_files\Sadiubus_trial_v0.2.2.zip", "tmp")
    unzip_7z_file(r"test_files\Test7zReqPas.7z", "tmp")
    # if len(sys.argv) > 1:
    #     file_path = sys.argv[1]