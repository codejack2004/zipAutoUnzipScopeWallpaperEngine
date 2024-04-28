"""
调用bandizip解压文件
"""
import subprocess
import time


# test_zip_path = r"D:\SteamLibrary\steamapps\workshop\content\431960\2922967143\OO骰子.zip.exe"
# test_unzip_dir = r"D:\SteamLibrary\steamapps\workshop\content\431960\2922967143\unzip"
def last3_exit():
    # 倒计时三秒关闭
    t = 3
    for i in range(3):
        print(f"（＞人＜；） 倒计时{t-i}秒  后关闭")
        time.sleep(1)

# 解压文件
def unzip_file(zip_file, unzip_dir, password = None):
    cmd = f"bz x -p:{password} -o:{unzip_dir} {zip_file}"
    print(cmd)
    subprocess.call(cmd, shell=True)

    print("解压完成")
    
    last3_exit()
    





# unzip_file(test_zip_path, test_unzip_dir, "touzidicegame1")