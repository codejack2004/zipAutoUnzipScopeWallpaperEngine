import os
import aspose.zip as zp
import zipfile
from py7zr import SevenZipFile
from utils.toast import toaster
from tqdm import tqdm
from colorama import Fore, Style, init
import time
import pyzipper
from tqdm import tqdm
import os
# 初始化colorama
init()

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


def get_file_name(file_path):
    return os.path.basename(file_path).split(".")[0]


cloud_passwords = [
    "password",
    "123456",
    "admin",
    "2005",
    "codejack"
]




def unzip_file(zip_path, extract_to):
    # 打开ZIP文件
    with pyzipper.AESZipFile(zip_path) as zip_file:
        # if password:
        #     zip_file.pwd = password.encode('utf-8')
        
        # 获取所有文件的列表
        list_of_files = zip_file.namelist()
        total_size = sum([zip_file.getinfo(name).file_size for name in list_of_files])
        
        # 设置tqdm进度条
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Extracting")
        
        # 逐个解压文件
        for file in list_of_files:
            file_info = zip_file.getinfo(file)
            extracted_path = zip_file.extract(file, path=extract_to)
            
            # 尝试修正中文乱码
            correct_filename = None
            try:
                correct_filename = file.encode('cp437').decode('gbk')
            except:
                correct_filename = file.encode('cp437').decode('utf-8')
            
            correct_path = os.path.join(extract_to, correct_filename)

            if extracted_path != correct_path:
                os.rename(extracted_path, correct_path)
            
            # 更新进度条
            progress_bar.update(file_info.file_size)
        
        # 关闭进度条
        progress_bar.close()




def check_password(zip_path, zip_type):
    """
    查看是否有密码 如果无密码 返回 False
    有密码 则直接返回密码
    """
    if zip_type == "ZIP":
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            try:
                zip_ref.testzip()
                return None
            except Exception as e:
                pass

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for password in cloud_passwords:
                try:
                    zip_ref.setpassword(bytes(password, "utf-8"))
                    zip_ref.testzip()
                    return password
                except Exception as e:
                    pass
        while True:
            toaster.show_toast("codeJack>>", "没找到合适的密码 请您手动输入一次 之后 所有使用这个软件的用户就都不需要输入这个密码了", duration=5,threaded=True, icon_path="D:/Codes/zipAutoUnzipScopeWallpaperEngine/images/favicon.ico")
            password = input("请输入密码: ")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                try:
                    zip_ref.setpassword(bytes(password, "utf-8"))
                    zip_ref.testzip()
                    return password
                except Exception as e:
                    print("密码错误 请重新输入")



def extract_zip(zip_path, zip_type, extract_to):
    if zip_type == "ZIP":
        res = check_password(zip_path, zip_type)
        if res is None:
            unzip_file(zip_path, extract_to, None)
        else:
            print("有密码", res)
            options = zp.ArchiveLoadOptions()
            options.decryption_password = res
            with zp.Archive(zip_path, options) as archive:
                archive.extract_to_directory(extract_to)

    elif zip_type == "7z":
        try:
            with SevenZipFile(zip_path, mode='r') as z:
                z.extractall(extract_to)
                return
        except Exception as e:
            if "Password is required" in str(e):
                is_open = False
                for password in cloud_passwords:
                    try:
                        with SevenZipFile(zip_path, mode='r', password=password) as z:
                            z.extractall(extract_to)
                            is_open = True
                    except Exception as e:
                        pass
                if is_open: return
                while True:
                    toaster.show_toast("codeJack>>", "没找到合适的密码 请您手动输入一次 之后 所有使用这个软件的用户就都不需要输入这个密码了", duration=5, threaded=True, icon_path="D:/Codes/zipAutoUnzipScopeWallpaperEngine/images/favicon.ico")
                    password = input("请输入密码: ")
                    try:
                        with SevenZipFile(zip_path, mode='r', password=password) as z:
                            z.extractall(extract_to)
                            return
                    except Exception as e:
                        print("密码错误 请重新输入")
                    
