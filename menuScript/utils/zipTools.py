import pyzipper
from py7zr import SevenZipFile
import rarfile
import os
import sys

exe_path = os.path.dirname(sys.argv[0])
password_path = os.path.join(exe_path, "passwords.txt")

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


PASSWORDS = []

if not os.path.exists(password_path):
    with open(password_path, "w") as f:
        f.write("bili codejack\n")

with open(password_path, "r") as f:
    PASSWORDS = list(set([line.strip() for line in f.readlines()]))

def save_password(password):
    if password in PASSWORDS: return
    with open(password_path, "a") as f:
        f.write(password + "\n")

def find_zip_password(zip_path):
    """
    返回zip压缩包的密码
    返回: 2005 表示不需要密码
    返回: None 表示未找到密码
    返回: str 表示找到的密码
    """
    zip_file = pyzipper.AESZipFile(zip_path)
    file_list = zip_file.namelist()
    for test_file in file_list:
        try:
            with zip_file.open(test_file) as f:
                if not f.read(10) == b'':
                    return 2005
        except Exception as e:
            if "password required" in str(e):
                break
    
    # 寻找密码
    for password in PASSWORDS:
        try:
            zip_file.setpassword(password.encode('utf-8'))
            for test_file in file_list:
                with zip_file.open(test_file) as f:
                    if not f.read(10) == b'':
                        save_password(password)
                        return password
        except Exception as e:
            continue

    print("＞﹏＜ 没找到合适的密码 请你手动输入一次 下次就不需要了")
    while True:
        password = input("请输入密码: ")
        try:
            zip_file.setpassword(password.encode('utf-8'))
            for test_file in file_list:
                with zip_file.open(test_file) as f:
                    if not f.read(10) == b'':
                        save_password(password)
                        return password
        except Exception as e:
            print("密码错误")
            continue


def find_7z_password(zip_path):
    """
    返回7z压缩包的密码
    返回: 2005 表示不需要密码
    返回: None 表示未找到密码
    返回: str 表示找到的密码
    """
    try:
        SevenZipFile(zip_path, mode='r')
        return 2005
    except Exception as e:
        if "Password is required" in str(e):
            for password in PASSWORDS:
                try:
                    SevenZipFile(zip_path, mode='r', password=password)
                    save_password(password)
                    return password
                except Exception as e:
                    continue

    print("＞﹏＜ 没找到合适的密码 请你手动输入一次 下次就不需要了")
    while True:
        password = input("输入密码: ")
        try:
            SevenZipFile(zip_path, mode='r', password=password)
            save_password(password)
            return password
        except Exception as e:
            print("密码错误")
            continue


# if __name__ == '__main__':
#     test_path = r"D:\SteamLibrary\steamapps\workshop\content\431960\2659676207\pas.rar"
#     print(identify_file_type(test_path))