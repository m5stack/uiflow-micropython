import sys
import subprocess
import re

def parse_backtrace(elf_file_path, backtrace):
    addresses = backtrace.split(' ')
    for address in addresses:
        if ':' in address:
            addr = address.split(':')[0]  # 只需要冒号前的地址部分

            # 构建命令
            command = f"xtensa-esp32-elf-addr2line -pfiaC -e {elf_file_path} {addr}"

            # 运行命令并捕获输出
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 打印结果
            print(result.stdout)

            # 错误处理
            if result.stderr:
                print("Error:", result.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python parse_backtrace.py <elf_path> <backtrace_string>")
        sys.exit(1)

    elf_file_path = sys.argv[1]
    backtrace = sys.argv[2]


    parse_backtrace(elf_file_path, backtrace)
