from pathlib import Path
import pandas as pd

# 定义源码所在的目录路径，根据实际情况进行调整
source_code_directory_path = Path("/home/kali/Desktop/urijs/src/")

# 初始化计数器
total_words = 0
total_lines = 0

# 准备存储每个文件统计数据的列表
files_data = []

# 遍历目录中的每个文件
for file_path in source_code_directory_path.rglob("*"):  # 使用rglob以递归查找所有文件
    if file_path.is_file():  # 确保是文件而不是目录
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines_count = len(lines)
            total_lines += lines_count
            words_count = sum(len(line.split()) for line in lines)
            total_words += words_count
            
            # 将当前文件的统计数据添加到列表中
            files_data.append({
                "File Name": file_path.name,
                "Number of Words": words_count,
                "Number of Lines": lines_count
            })

# 创建DataFrame
df = pd.DataFrame(files_data)

# 输出总计的单词数和行数
print(f"Total Number of Words in source code: {total_words}")
print(f"Total Number of Lines in source code: {total_lines}")

# 保存到CSV文件
csv_file_path = "/home/kali/Desktop/source_code_statistics.csv"
df.to_csv(csv_file_path, index=False)

# 输出CSV文件路径
csv_file_path
