import yaml
import time
import os

# 全局唯一时间戳
GLOBAL_TIMESTAMP = str(int(time.time()))


def read_yaml(file_path, key):
    #动态计算项目根目录的绝对路径
    # 1. __file__ 指向 yaml_util.py 本身
    # 2. dirname(__file__) 拿到 common 文件夹的路径
    # 3. 再套一层 dirname，精准锁定项目根目录 ruoyi/
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # 将传进来的 "data/menu_data.yml" 拼接到项目根目录后面
    abs_file_path = os.path.join(base_dir, file_path)

    # 直接使用绝对路径读取文件，永远不会偏移
    with open(abs_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("${TIMESTAMP}", GLOBAL_TIMESTAMP)
    data = yaml.safe_load(content)
    return data.get(key)