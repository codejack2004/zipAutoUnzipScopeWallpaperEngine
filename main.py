import os
import sys
import time
from utils.toast import toaster


from utils.zip_tool import identify_file_type, get_file_name, extract_zip
from utils.set_menu import del_menu, set_menu, check_menu
work_path = os.getcwd()
images_path = os.path.join(work_path, 'images')



if __name__ == "__main__":
    if not check_menu():
        set_menu(os.path.join(work_path, 'AutoUnZipWE.exe'), os.path.join(images_path, 'favicon.ico'))
 
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            file_name = get_file_name(file_path)
            file_type = identify_file_type(file_path)
            if file_type == "Unknown file type":
                print("选择的文件不受支持")
                # 显示通知
                toaster.show_toast("codeJack>>", "你选择的是无效的压缩包文件", duration=4, threaded=True, icon_path=r"D:\Codes\zipAutoUnzipScopeWallpaperEngine\images\favicon.ico")
                # 四秒后退出
                print("倒计时4秒后退出")
                t = 4
                for i in range(4):
                    print(f"倒计时{t-i}秒")
                    time.sleep(1)
                sys.exit(0)
            else:
                if not os.path.exists(f"extracted"):
                    os.makedirs(f"extracted")

                extract_zip(file_path, file_type, f"extracted")
                input("按任意键退出")
                
    except Exception as e:
        print(e)
        input("按任意键退出")
