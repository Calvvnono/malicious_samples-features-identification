from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np
import os
import re
import base64
import json
import math
from math import log2
from collections import Counter
from scipy.stats import entropy
from pygments.lexers import get_lexer_for_filename
from pygments.token import Operator, Punctuation

source_code_directory_path = Path("node_modules/urijs/")
GL_code_directory_path = Path("temp/separate/urijs/")

# 初始化
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
num_of_base64 = 0
num_of_ip = 0
total_words_meta = 0
total_lines_meta = 0
num_of_base64_meta = 0
num_of_ip_meta = 0
install_hook = 0
mean_shannon_identifier = 0
max_shannon_identifier = 0
std_shannon_identifier = 0
q3_shannon_identifier = 0
mean_shannon_string = 0
max_shannon_string = 0
std_shannon_string = 0
q3_shannon_string = 0
homo_count_i = 0
hetero_count_i = 0
homo_count_s = 0
hetero_count_s = 0
mean_shannon_identifier_meta = 0
max_shannon_identifier_meta = 0
std_shannon_identifier_meta = 0
q3_shannon_identifier_meta = 0
mean_shannon_string_meta = 0
max_shannon_string_meta = 0
std_shannon_string_meta = 0
q3_shannon_string_meta = 0
homo_count_i_meta = 0
hetero_count_i_meta = 0
homo_count_s_meta = 0
hetero_count_s_meta = 0

""" 1.源代码总行数和总词数 """
# 遍历目录中的每个文件
for file_path in source_code_directory_path.glob("**/*.js"):  # 递归读取
    if file_path.is_file():  # 确保是文件而不是目录
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
            total_lines += len(lines)  # 累加行数
            total_words += sum(len(line.split()) for line in lines)  # 累加单词数   

""" 2.各种符号占源代码字符数比例的统计量 """ 
# 存储每个文件的加号占总字数的比例
plus_ratios = []
equal_ratios = []
bracket_ratios = []
plus_count = 0
equal_count = 0
bracket_count = 0

def extract_text_elements(source_code, lexer):
    tokens = lexer.get_tokens(source_code)
    plus_cnt = 0
    equal_cnt = 0
    bracket_cnt = 0
    for token_type, value in tokens:
        if token_type in Operator and value == '+':
            plus_cnt += 1
        elif token_type in Operator and value == '=':
            equal_cnt += 1
        elif token_type in Punctuation and (value == '['):
            bracket_cnt += 1
    return plus_cnt, equal_cnt, bracket_cnt

for file_path in source_code_directory_path.glob("**/*.js"):
    if file_path.is_file():
        file_size = os.path.getsize(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            source_code = file.read()
            lexer = get_lexer_for_filename(file_path.name, stripall=True)
            plus_count, equal_count, bracket_count = extract_text_elements(source_code, lexer)

            plus_ratio = plus_count / file_size
            plus_ratios.append(plus_ratio)
            equal_ratio = equal_count / file_size
            equal_ratios.append(equal_ratio)
            bracket_ratio = bracket_count / file_size
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

""" 3.检测base64和IP串 """
# 定义匹配IP地址的正则表达式模式
ip_pattern = re.compile(r'\b(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b')
for file_path in source_code_directory_path.glob("**/*.js"):
    if file_path.is_file():  
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()
            ip_matches = ip_pattern.findall(file_content)
            num_of_ip += len(ip_matches)

for file_path in source_code_directory_path.glob("**/*.js"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()
            #content = file_content.split()
            potential_base64_strings = re.findall(r'(?<=\b)[A-Za-z0-9+/=]+(?=\b)', file_content)
            for potential_base64_string in potential_base64_strings:
                try:
                    # 使用 base64 解码字符串
                    decoded_bytes = base64.b64decode(potential_base64_string)
                    # 尝试将解码后的字节数据转换为字符串，确保解码成功
                    decoded_string = decoded_bytes.decode('utf-8')
                    num_of_base64 += 1
                except Exception as e:
                    pass

""" 4.metadata总行数和总词数 """
for file_path in source_code_directory_path.glob("package.json"):  # 递归读取
    if file_path.is_file():  # 确保是文件而不是目录
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            total_lines_meta += len(lines)  # 累加行数
            total_words_meta += sum(len(line.split()) for line in lines)  # 累加单词数      
            
# """ 5.metadata检测base64和IP串 """
# # 定义匹配IP地址的正则表达式模式
# ip_pattern = re.compile(r'\b(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b')
# for file_path in source_code_directory_path.glob("package.json"):
#     if file_path.is_file():  
#         with open(file_path, 'r', encoding='utf-8') as file:
#             file_content = file.read()
#             ip_matches = ip_pattern.findall(file_content)
#             num_of_ip += len(ip_matches)

# for file_path in source_code_directory_path.glob("package.json"):
#     if file_path.is_file():
#         with open(file_path, 'r', encoding='utf-8') as file:
#             file_content = file.read()
#             #content = file_content.split()
#             potential_base64_strings = re.findall(r'(?<=\b)[A-Za-z0-9+/=]+(?=\b)', file_content)
#             for potential_base64_string in potential_base64_strings:
#                 try:
#                     # 使用 base64 解码字符串
#                     decoded_bytes = base64.b64decode(potential_base64_string)
#                     # 尝试将解码后的字节数据转换为字符串，确保解码成功
#                     decoded_string = decoded_bytes.decode('utf-8')
#                     num_of_base64 += 1
#                 except Exception as e:
#                     pass
""" 统计各类型文件 """
file_types = ['bat', 'bz2', 'c', 'cert', 'conf' ,'cpp' ,'crt', 'css', 'csv', 'deb' ,'erb', 'gemspec', 'gif', 'gz', 'h', 'html', 'ico' ,'ini' ,'jar', 'java', 'jpg', 'js', 'json', 'key' ,'m4v' ,'markdown' ,'md' ,'pdf', 'pem', 'png', 'ps', 'py', 'rb', 'rpm', 'rst','sh' ,'svg', 'toml', 'ttf', 'txt','xml', 'yaml', 'yml', 'eot', 'exe', 'jpeg', 'properties', 'sql', 'swf', 'tar', 'woff', 'woff2', 'aac','bmp', 'cfg' ,'dcm', 'dll', 'doc', 'flac','flv', 'ipynb', 'm4a', 'mid', 'mkv', 'mp3', 'mp4', 'mpg', 'ogg','otf', 'pickle', 'pkl' ,'psd', 'pxd' ,'pxi', 'pyc', 'pyx', 'r', 'rtf', 'so', 'sqlite' ,'tif', 'tp', 'wav', 'webp' ,'whl', 'xcf', 'xz', 'zip' ,'mov' ,'wasm', 'webm']
file_type_counts = defaultdict(int)

for file_path in source_code_directory_path.glob("**/*"):
    if file_path.is_file():
        # 获取文件后缀
        file_extension = file_path.suffix[1:].lower()  # 去掉点号，并转换为小写
        # 检查文件后缀是否在指定的类型列表中
        file_type_counts[file_extension] += 1

""" 6.检测安装钩子 """
for file_path in source_code_directory_path.glob("package.json"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            # 解析 JSON 文件
            data = json.load(file)
            # 检查是否包含 install、post-install、pre-install 关键字
            if 'scripts' in data and any(script in data['scripts'] for script in ['install', 'postinstall', 'preinstall']):
                install_hook = 1
                break

""" 7.计算标识符的香农熵统计量 """
shannon_entropies = []
for file_path in GL_code_directory_path.glob("**/*_identifier.js"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                if line:
                    shannon_entropy = entropy([line.count(c) / len(line) for c in set(line)], base=2) / 2
                    shannon_entropies.append(shannon_entropy)
# 计算统计值
mean_shannon_identifier = np.mean(shannon_entropies)
std_shannon_identifier = np.std(shannon_entropies)
q3_shannon_identifier = np.percentile(shannon_entropies, 75)
max_shannon_identifier = np.max(shannon_entropies)

""" 8.计算字符串的香农熵统计量 """
shannon_entropies_ = []
for file_path in GL_code_directory_path.glob("**/*_strings.js"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                if line:
                    shannon_entropy = entropy([line.count(c) / len(line) for c in set(line)], base=2) / 2
                    shannon_entropies_.append(shannon_entropy)
# 计算统计值
mean_shannon_string = np.mean(shannon_entropies_)
std_shannon_string = np.std(shannon_entropies_)
q3_shannon_string = np.percentile(shannon_entropies_, 75)
max_shannon_string = np.max(shannon_entropies_)

""" 9.同质标识符数量 """
hetero = []
for file_path in GL_code_directory_path.glob("**/*_identifier.js"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # 判断整行字符串是否全部由L、U、D或S中的一个字符组成
                if(len(set(line.strip()))) == 1:
                    homo_count_i += 1
                else:
                    if line not in hetero:
                        hetero.append(line)
                        hetero_count_i += 1

""" 10.同质字符串数量 """
hetero = []
for file_path in GL_code_directory_path.glob("**/*_strings.js"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # 判断整行字符串是否全部由L、U、D或S中的一个字符组成
                if(len(set(line.strip()))) == 1:
                    homo_count_s += 1
                else:
                    if line not in hetero:
                        hetero.append(line)
                        hetero_count_s += 1

""" 11.metadata标识符的香农熵统计量 """
shannon_entropies_meta = []
for file_path in GL_code_directory_path.glob("**/*_identifier.json"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                if line:
                    shannon_entropy_meta = entropy([line.count(c) / len(line) for c in set(line)], base=2) / 2
                    shannon_entropies_meta.append(shannon_entropy_meta)
# 计算统计值
mean_shannon_identifier_meta = np.mean(shannon_entropies_meta)
std_shannon_identifier_meta = np.std(shannon_entropies_meta)
q3_shannon_identifier_meta = np.percentile(shannon_entropies_meta, 75)
max_shannon_identifier_meta = np.max(shannon_entropies_meta)

""" 12.metadata字符串的香农熵统计量 """
shannon_entropies__meta = []
for file_path in GL_code_directory_path.glob("**/*_strings.json"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                if line:
                    shannon_entropy_meta = entropy([line.count(c) / len(line) for c in set(line)], base=2) / 2
                    shannon_entropies__meta.append(shannon_entropy_meta)
# 计算统计值
mean_shannon_string_meta = np.mean(shannon_entropies__meta)
std_shannon_string_meta = np.std(shannon_entropies__meta)
q3_shannon_string_meta = np.percentile(shannon_entropies__meta, 75)
max_shannon_string_meta = np.max(shannon_entropies__meta)

""" 13.metadata同质标识符数量 """
hetero = []
for file_path in GL_code_directory_path.glob("**/*_identifier.json"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # 判断整行字符串是否全部由L、U、D或S中的一个字符组成
                if(len(set(line.strip()))) == 1:
                    homo_count_i_meta += 1
                else:
                    if line not in hetero:
                        hetero.append(line)
                        hetero_count_i_meta += 1

""" 14.metadata同质字符串数量 """
hetero = []
for file_path in GL_code_directory_path.glob("**/*_strings.json"):
    if file_path.is_file():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # 判断整行字符串是否全部由L、U、D或S中的一个字符组成
                if(len(set(line.strip()))) == 1:
                    homo_count_s_meta += 1
                else:
                    if line not in hetero:
                        hetero.append(line)
                        hetero_count_s_meta += 1

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
    "Number of base64 chunks in source code":   "?",
    "num of ip address":              [num_of_ip],
    "Number of sospicious token in source code":  "?",
    "Number of Words in metadata":    [total_words_meta],
    "Number of lines in metadata":    [total_lines_meta],
    "Number of base64 chunks in metadata":  "?",
    "Number of IP address in metadata":[num_of_ip_meta],
    ".bat": file_type_counts['bat'],
    ".bz2": file_type_counts['bz2'],
    ".c": file_type_counts['c'],
    ".cert": file_type_counts['cert'],
    ".conf": file_type_counts['conf'],
    ".cpp": file_type_counts['cpp'],
    ".crt": file_type_counts['crt'],
    ".css": file_type_counts['css'],
    ".csv": file_type_counts['csv'],
    ".deb": file_type_counts['deb'],
    ".erb": file_type_counts['erb'],
    ".gemspec": file_type_counts['gemspec'],
    ".gif": file_type_counts['gif'],
    ".gz": file_type_counts['gz'],
    ".h": file_type_counts['h'],
    ".html": file_type_counts['html'],
    ".ico": file_type_counts['ico'],
    ".ini": file_type_counts['ini'],
    ".jar": file_type_counts['jar'],
    ".java": file_type_counts['java'],
    ".jpg": file_type_counts['jpg'],
    ".js": file_type_counts['js'],
    ".json": file_type_counts['json'],
    ".key": file_type_counts['key'],
    ".m4v": file_type_counts['m4v'],
    ".markdown": file_type_counts['markdown'],
    ".md": file_type_counts['md'],
    ".pdf": file_type_counts['pdf'],
    ".pem": file_type_counts['pem'],
    ".png": file_type_counts['png'],
    ".ps": file_type_counts['ps'],
    ".py": file_type_counts['py'],
    ".rb": file_type_counts['rb'],
    ".rpm": file_type_counts['rpm'],
    ".rst": file_type_counts['rst'],
    ".sh": file_type_counts['sh'],
    ".svg": file_type_counts['svg'],
    ".toml": file_type_counts['toml'],
    ".ttf": file_type_counts['ttf'],
    ".txt": file_type_counts['txt'],
    ".xml": file_type_counts['xml'],
    ".yaml": file_type_counts['yaml'],
    ".yml": file_type_counts['yml'],
    ".eot": file_type_counts['eot'],
    ".exe": file_type_counts['exe'],
    ".jpeg": file_type_counts['jpeg'],
    ".properties": file_type_counts['properties'],
    ".sql": file_type_counts['sql'],
    ".swf": file_type_counts['swf'],
    ".tar": file_type_counts['tar'],
    ".woff": file_type_counts['woff'],
    ".woff2": file_type_counts['woff2'],
    ".aac": file_type_counts['aac'],
    ".bmp": file_type_counts['bmp'],
    ".cfg": file_type_counts['cfg'],
    ".dcm": file_type_counts['dcm'],
    ".dll": file_type_counts['dll'],
    ".doc": file_type_counts['doc'],
    ".flac": file_type_counts['flac'],
    ".flv": file_type_counts['flv'],
    ".ipynb": file_type_counts['ipynb'],
    ".m4a": file_type_counts['m4a'],
    ".mid": file_type_counts['mid'],
    ".mkv": file_type_counts['mkv'],
    ".mp3": file_type_counts['mp3'],
    ".mp4": file_type_counts['mp4'],
    ".mpg": file_type_counts['mpg'],
    ".ogg": file_type_counts['ogg'],
    ".otf": file_type_counts['otf'],
    ".pickle": file_type_counts['pickle'],
    ".pkl": file_type_counts['pkl'],
    ".psd": file_type_counts['psd'],
    ".pxd": file_type_counts['pxd'],
    ".pxi": file_type_counts['pxi'],
    ".pyc": file_type_counts['pyc'],
    ".pyx": file_type_counts['pyx'],
    ".r": file_type_counts['r'],
    ".rtf": file_type_counts['rtf'],
    ".so": file_type_counts['so'],
    ".sqlite": file_type_counts['sqlite'],
    ".tif": file_type_counts['tif'],
    ".tp": file_type_counts['tp'],
    ".wav": file_type_counts['wav'],
    ".webp": file_type_counts['webp'],
    ".whl": file_type_counts['whl'],
    ".xcf": file_type_counts['xcf'],
    ".xz": file_type_counts['xz'],
    ".zip": file_type_counts['zip'],
    ".mov": file_type_counts['mov'],
    ".wasm": file_type_counts['wasm'],
    ".webm": file_type_counts['webm'],
    "presence of installation script" :[install_hook],
    "shannon mean identifier source code" :[mean_shannon_identifier],
    "shannon std identifier source code" :[std_shannon_identifier],
    "shannon max identifier source code" :[max_shannon_identifier],
    "shannon q3 identifier source code" :[q3_shannon_identifier],
    "shannon mean string source code" :[mean_shannon_string],
    "shannon std string source code" :[std_shannon_string],
    "shannon max string source code" :[max_shannon_string],
    "shannon q3 string source code" :[q3_shannon_string],
    "homogeneous identifiers in source code" : [homo_count_i],
    "homogeneous strings in source code" : [homo_count_s],
    "heterogeneous identifiers in source code" : [hetero_count_i],
    "heterogeneous strings in source code" : [hetero_count_s],
    "shannon mean identifier metadata" :[mean_shannon_identifier_meta],
    "shannon std identifier metadata" :[std_shannon_identifier_meta],
    "shannon max identifier metadata" :[max_shannon_identifier_meta],
    "shannon q3 identifier metadata" :[q3_shannon_identifier_meta],
    "shannon mean string metadata" :[mean_shannon_string_meta],
    "shannon std string metadata" :[std_shannon_string_meta],
    "shannon max string metadata" :[max_shannon_string_meta],
    "shannon q3 string metadata" :[q3_shannon_string_meta],
    "homogeneous identifiers metadata" : [homo_count_i_meta],
    "homogeneous strings metadata" : [homo_count_s_meta],
    "heterogeneous identifiers metadata" : [hetero_count_i_meta],
    "heterogeneous strings metadata" : [hetero_count_s_meta]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存到CSV文件
csv_file_path = "source_code_statistics.csv"
df.to_csv(csv_file_path, index=False)
