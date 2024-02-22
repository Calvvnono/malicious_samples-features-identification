from pathlib import Path
import pandas as pd

source_code_directory_path = Path("/home/kali/Desktop/urijs/src/")

# 初始化计数器
total_words = 0
total_lines = 0

# 遍历目录中的每个文件
for file_path in source_code_directory_path.glob("*.js"):  # 假设只统计JavaScript文件
    if file_path.is_file():  # 确保是文件而不是目录
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            total_lines += len(lines)  # 累加行数
            total_words += sum(len(line.split()) for line in lines)  # 累加单词数

# 准备数据
data = {
    "Number of Words in source code": [total_words],
    "Number of lines in source code": [total_lines]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存到CSV文件
csv_file_path = "/home/kali/Desktop/source_code_statistics.csv"
df.to_csv(csv_file_path, index=False)
