import winreg as reg


# 查看右键菜单是否存在
def check_menu():
    key = reg.HKEY_CLASSES_ROOT
    sub_key = r'*\\shell\\AutoUnzipScopeWallpaperEngine\\command'
    try:
        registry_key = reg.OpenKey(key, sub_key, 0, reg.KEY_READ)
        command = reg.QueryValue(registry_key, None)
        reg.CloseKey(registry_key)
        return True
    except WindowsError as e:
        return False



# 设置右键菜单
def set_menu(menu_exe_path, icon_path=None):
    print(menu_exe_path, icon_path)
    command = f'"{menu_exe_path}" "%1"'  # 修改路径到你的Python脚本
    key = reg.HKEY_CLASSES_ROOT
    sub_key = r'*\\shell\\AutoUnzipScopeWallpaperEngine\\command'
    try:
        reg.CreateKey(key, r'*\\shell\\AutoUnzipScopeWallpaperEngine\\command')
        registry_key = reg.OpenKey(key, sub_key, 0, reg.KEY_WRITE) 
        reg.SetValue(registry_key, '', reg.REG_SZ, command)
        reg.CloseKey(registry_key)

        if icon_path:
            # 在AutoUnzipScopeWallpaperEngine里添加一个字符串值
            key = reg.CreateKey(key, r'*\\shell\\AutoUnzipScopeWallpaperEngine')
            reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, icon_path)


        print("右键菜单项添加成功！")
        return True
    except WindowsError as e:
        print(e)
        print("添加右键菜单项失败！")
        return False


# 删除右键菜单
def del_menu():
    key = reg.HKEY_CLASSES_ROOT
    del_keys = [r'*\\shell\\AutoUnzipScopeWallpaperEngine\\command', r'*\\shell\\AutoUnzipScopeWallpaperEngine']
    try:
        for sub_key in del_keys:
            reg.DeleteKey(key, sub_key)
        print("右键菜单项删除成功！")
        return True
    except WindowsError as e:
        print(e)
        print("删除右键菜单项失败！")
        return False



# 启动终端的彩色输出
def set_cmd_ascii_color():
    key = reg.HKEY_CURRENT_USER
    key = reg.CreateKey(key, r'Console')
    reg.SetValueEx(key, "VirtualTerminalLevel", 0, reg.REG_DWORD, 1)
   

if __name__ == "__main__":
    pass
    # del_menu()
    # set_menu(r'D:\Codes\zipAutoUnzipScopeWallpaperEngine\dist\menuScript.exe', r'D:\Codes\zipAutoUnzipScopeWallpaperEngine\images\favicon.ico')
    # set_cmd_ascii_color()