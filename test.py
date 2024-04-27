import pyzipper
from tqdm import tqdm
import os


def unzip_file(zip_path, extract_to, password=None):
    # 打开ZIP文件
    with pyzipper.AESZipFile(zip_path) as zip_file:
        if password:
            zip_file.pwd = password.encode('utf-8')
        
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



# 使用示例
unzip_file(r'D:\Codes\zipAutoUnzipScopeWallpaperEngine\test_files\TestZipReqPas.zip', 'tmp', password='123456')