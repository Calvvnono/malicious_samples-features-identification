import openpyxl
import json

# 打开xlsx文件
wb = openpyxl.load_workbook("Labelled_Dataset.xlsx")
    
# 获取第一个工作表
sheet = wb.active
    
# 初始化一个空的字典来存储软件包信息
packages = {}

# 遍历第三列，提取软件包信息
for row in sheet.iter_rows(min_row=2, max_row=919, values_only=True):
    # 从字符串尾部向头部查找第一个 '-' 并进行拆分
    index = row[2][::-1].find('-')
            
    # 如果找到'-'
    if index != -1:
    # 更新 package_name 和 package_version
        package_name = row[2][:-index-1]
        package_version = row[2][-index:]
        
        # 检查 - 后面是否跟着数字
        if len(package_version)==1 :
            index = row[2][::-1].find('-', index+1)
            package_name = row[2][:-index-1]
            package_version = row[2][-index:]
        while not package_version[0].isdigit():
            # 继续向前找，直到找到一个数字开头的位置
            index = row[2][::-1].find('-', index+1)
            package_name = row[2][:-index-1]
            package_version = row[2][-index:]
    else:
        # 如果找不到'-',记录错误并继续处理下一行
        print(f"Error processing row: {row}, Unexpected format")
        continue
    packages[package_name] = f'^{package_version}'

# 将软件包信息写入package.json文件
with open("111.json", 'w') as json_file:
    json.dump({"dependencies": packages}, json_file, indent=2)