import os
import random
import string
import subprocess


def is_file_exist(input_file):
    return os.path.isfile(input_file)


# 转换Word文件为PDF文件
def convert_word_to_pdf(input_file, output_file, output_path):
    # 检查是否安装了LibreOffice库
    if not is_libreoffice_installed():
        assert Exception(f"转换失败，系统中未安装LibreOffice库")

    # 检查输入文件是否存在
    if not is_file_exist(input_file):
        assert Exception(f"转换失败，输入文件不存在")
        return

    # 定义转换命令
    command = [
        'libreoffice',  # 根据你的系统可能需要写为 'soffice' 或者 '/usr/bin/libreoffice'
        '--headless',  # 在后台无界面模式运行
        '--convert-to', 'pdf',  # 指定输出格式为PDF
        '--outdir', output_path,  # 指定输出目录
        input_file,  # 输入的Word文件路径
    ]

    # 添加自定义输出文件名
    output_filename = f"{output_path}/{output_file}"
    command.extend(['--infilter="writer8FILTERXML"'])  # 对于.doc文件（如果适用）
    command.append(f'"{output_filename}"')  # 这里添加带有完整路径和名称的输出文件

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        assert Exception(f"转换失败，失败原因: {e}")
    else:
        return output_filename


# 检查是否安装了LibreOffice
def is_libreoffice_installed():
    try:
        # 尝试执行一个无害且快速完成的LibreOffice命令
        subprocess.run(['libreoffice', '--help'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True  # 如果没有抛出异常，则认为LibreOffice已安装
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False  # 如果找不到命令或执行时出现问题，则认为未安装


def generate_random_strings(length, charset=string.ascii_letters + string.digits):
    """
    生成n个长度为length的随机字符串，字符集默认包含大小写字母和数字。

    参数：
    n (int)：需要生成的随机字符串的数量。
    length (int)：每个随机字符串的长度。
    charset (str)：用于生成字符串的字符集，可以自定义。

    返回：
    字符串
    """
    return ''.join(random.choices(charset, k=length))
