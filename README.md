# malicious_samples-features-identification

# 运行方式：

1. 原Npm包统一放node_modules目录
2. split_Identifier_string.py将原包中的identifier和string分离，存进separate目录的同名包下文件
3. GL4.py将separate目录指定包下文件做GL映射，并存进temp/separate/目录
4. feature.py对temp/separate/目录下文件做数据统计

# 当前进度：

	1. string相关的一切，数据能看但都对不上，无法确认作者思路，万博意思就先这样。
	1. identifier的同质串，香农熵等全部匹配；只有异质串数量无法匹配，但已经找不到异质串的其他任何解释或识别方式。
	1. 其余简单数据全部匹配。

# TODO

	1. 批量下载良性Npm包，良/恶性比例在9：1左右。
	1. feature.py下每个功能为便于调试，独立做了递归扫描，可以整合成新的文件，两遍扫描解决所有数据。
	1. 对于split_Identifier_string.py，GL4.py，feature.py中的源/目标路径，循环处理所有包时用包名进行字符串拼接。