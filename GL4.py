import os
import re

input_directory = './separate/urijs/'
output_directory = './temp/'

def transform_string(s):
    result = ''
    for char in s:
        if char.islower():
            result += 'L'
        elif char.isupper():
            result += 'U'
        elif char.isdigit():
            result += 'D'
        elif char != '\n' and char != ' ':
            result += 'S'
        elif char == '\n':
            result += '\n'
    return result

for root, dirs, files in os.walk(input_directory):
    for file in files:
        input_file_path = os.path.join(root, file)
        output_file_path = os.path.join(output_directory, root, file)

        # 创建输出目录（如果不存在）
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(input_file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            transformed_content = transform_string(content)

        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(transformed_content)

def process_string(input_str):
    # 使用正则表达式去除多余空格，并用一个空格隔开每个字符串
    processed_str = ' '.join(re.findall(r'\S+', input_str))
    return processed_str

def process_files(input_directory):
    # 遍历指定目录下的所有文件
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            file_path = os.path.join(root, file)

            # 处理每个文件的内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                processed_content = process_string(content)

            # 将处理后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(processed_content)

# 处理所有文件，直接在源文件上进行修改
process_files("./temp/node_modules/urijs")
