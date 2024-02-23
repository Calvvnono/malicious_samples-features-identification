from pathlib import Path
import pandas as pd
import numpy as np
import os

source_code_directory_path = Path("node_modules/urijs")

# 初始化计数器
total_words = 0
total_lines = 0
mean_plus_ratio = 0
max_plus_ratio = 0
std_plus_ratio = 0
q3_plus_ratio = 0
mean_equal_ratio = 0
max_equal_ratio = 0
std_equal_ratio = 0
q3_equal_ratio = 0
mean_bracket_ratio = 0
max_bracket_ratio = 0
std_bracket_ratio = 0
q3_bracket_ratio = 0

""" 1.源代码总行数和总词数 """
# 遍历目录中的每个文件
for file_path in source_code_directory_path.glob("**/*.js"):  # 递归读取
    if file_path.is_file():  # 确保是文件而不是目录
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            total_lines += len(lines)  # 累加行数
            total_words += sum(len(line.split()) for line in lines)  # 累加单词数      

""" 2.各种符号占源代码字符数比例的统计量 """ 
# 存储每个文件的加号占总字数的比例
plus_ratios = []
equal_ratios = []
bracket_ratios = []
# 遍历目录中的每个文件
for file_path in source_code_directory_path.glob("**/*.js"):
    if file_path.is_file():  # 确保是文件而不是目录
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            total_characters = len(content)

            plus_count = content.count('+')
            plus_ratio = plus_count / total_characters if total_characters > 0 else 0
            plus_ratios.append(plus_ratio)

            equal_count = content.count('=')
            equal_ratio = equal_count / total_characters if total_characters > 0 else 0
            equal_ratios.append(equal_ratio)

            bracket_count = content.count('[') + content.count(']')
            bracket_ratio = bracket_count / total_characters if total_characters > 0 else 0
            bracket_ratios.append(bracket_ratio)
# 将比例列表转换为NumPy数组
ratios_array_p = np.array(plus_ratios)
ratios_array_e = np.array(equal_ratios)
ratios_array_b = np.array(bracket_ratios)
# 计算均值、最大值、标准差和三分位点
mean_plus_ratio = np.mean(ratios_array_p)
max_plus_ratio = np.max(ratios_array_p)
std_plus_ratio = np.std(ratios_array_p)
q3_plus_ratio = np.percentile(ratios_array_p, 75)

mean_equal_ratio = np.mean(ratios_array_e)
max_equal_ratio = np.max(ratios_array_e)
std_equal_ratio = np.std(ratios_array_e)
q3_equal_ratio = np.percentile(ratios_array_e, 75)

mean_bracket_ratio = np.mean(ratios_array_b)
max_bracket_ratio = np.max(ratios_array_b)
std_bracket_ratio = np.std(ratios_array_b)
q3_bracket_ratio = np.percentile(ratios_array_b, 75)

# 准备数据
data = {
    "Number of Words in source code": [total_words],
    "Number of lines in source code": [total_lines],
    "plus ratio mean":                [mean_plus_ratio],
    "plus ratio max":                 [max_plus_ratio],
    "plus ratio std":                 [std_plus_ratio],
    "plus ratio q3":                  [q3_plus_ratio],
    "equal ratio mean":               [mean_equal_ratio],
    "equal ratio max":                [max_equal_ratio],
    "equal ratio std":                [std_equal_ratio],
    "equal ratio q3":                 [q3_equal_ratio],
    "bracket ratio mean":             [mean_bracket_ratio],
    "bracket ratio max":              [max_bracket_ratio],
    "bracket ratio std":              [std_bracket_ratio],
    "bracket ratio q3":               [q3_bracket_ratio],
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存到CSV文件
csv_file_path = "source_code_statistics.csv"
df.to_csv(csv_file_path, index=False)
