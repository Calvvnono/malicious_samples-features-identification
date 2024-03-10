import os
from pygments.lexers import get_lexer_for_filename
from pygments.token import String, Name

input_directory = 'node_modules/urijs/'
output_directory = 'separate/urijs/'

def extract_text_elements(source_code, lexer):
    tokens = lexer.get_tokens(source_code)
    strings = []
    identifiers = []

    for token_type, value in tokens:
        if token_type in String:
            strings.append(value)
        elif token_type in Name:
            identifiers.append(value)
    return strings, identifiers

# 创建输出目录
os.makedirs(output_directory, exist_ok=True)

for root, dirs, files in os.walk(input_directory):
    for file_name in files:
        if file_name.endswith(".js"):
            input_path = os.path.join(root, file_name)

            # 获取通用 lexer
            lexer = get_lexer_for_filename(file_name, stripall=True)
            
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as file:
                js_source_code = file.read()

            js_strings, js_identifiers = extract_text_elements(js_source_code, lexer)

            # 去掉字符串两端双引号并写入文件
            output_strings_path = os.path.join(output_directory, file_name.replace(".js", "_strings.js"))
            with open(output_strings_path, 'w', encoding='utf-8') as output_file:
                for js_string in js_strings:
                    # 去掉引号
                    stripped_string = js_string.strip('\'').strip('"')
                    output_file.write(f"{stripped_string}\n")
            
            output_identifiers_path = os.path.join(output_directory, file_name.replace(".js", "_identifier.js"))
            with open(output_identifiers_path, 'w', encoding='utf-8') as output_file:
                for js_identifier in js_identifiers:
                    stripped_identifier = js_identifier.strip('"')
                    output_file.write(f"{stripped_identifier}\n")

for root, dirs, files in os.walk(input_directory):
    for file_name in files:
        if file_name.endswith("package.json"):
            input_path = os.path.join(root, file_name)

            # 获取通用 lexer
            lexer = get_lexer_for_filename(file_name, stripall=True)
            
            with open(input_path, 'r', encoding='utf-8') as file:
                js_source_code = file.read()

            js_strings, js_identifiers = extract_text_elements(js_source_code, lexer)

            # 去掉字符串两端双引号并写入文件
            output_strings_path = os.path.join(output_directory, file_name.replace(".json", "_strings.json"))
            with open(output_strings_path, 'w', encoding='utf-8') as output_file:
                for js_string in js_strings:
                    stripped_string = js_string.strip('"')
                    output_file.write(f"{stripped_string}\n")

            # 去掉标识符两端双引号并写入文件
            output_identifiers_path = os.path.join(output_directory, file_name.replace(".json", "_identifier.json"))
            with open(output_identifiers_path, 'w', encoding='utf-8') as output_file:
                for js_identifier in js_identifiers:
                    stripped_identifier = js_identifier.strip('"')
                    output_file.write(f"{stripped_identifier}\n")


