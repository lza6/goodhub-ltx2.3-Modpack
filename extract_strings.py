import re
import os

def extract_strings(filepath, min_length=8):
    """从二进制文件中提取可打印ASCII字符串"""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        # 提取连续的可打印字符
        pattern = rb'[a-zA-Z0-9_\-\.]{' + str(min_length).encode() + b',}'
        strings = re.findall(pattern, data)
        return set(s.decode('utf-8', errors='ignore') for s in strings)
    except Exception as e:
        print(f"Error: {e}")
        return []

def search_activation_strings(filepath):
    """搜索激活相关的字符串"""
    keywords = ['license', 'activate', 'auth', 'verify', 'key', 'token',
                'secret', 'code', 'password', 'passwd', 'pwd', 'serial',
                'registration', 'register', 'activ', 'licen', 'auth']

    strings = extract_strings(filepath)
    matches = []

    for s in strings:
        s_lower = s.lower()
        for kw in keywords:
            if kw in s_lower:
                matches.append(s)
                break

    return sorted(set(matches))

# 列出所有pyd文件
pyd_files = [
    'D:/LTX2.3_v4.0/app.pyd',
    'D:/LTX2.3_v4.0/core.pyd',
    'D:/LTX2.3_v4.0/LTX2_3_a2v.pyd',
    'D:/LTX2.3_v4.0/LTX2_3_DZQY.pyd',
    'D:/LTX2.3_v4.0/LTX2_3_i2v.pyd',
    'D:/LTX2.3_v4.0/LTX2_3_SWZ.pyd',
    'D:/LTX2.3_v4.0/LTX2_3_t2v.pyd',
    'D:/LTX2.3_v4.0/system_monitor.pyd'
]

for pyd_file in pyd_files:
    if os.path.exists(pyd_file):
        print(f"\n{'='*60}")
        print(f"文件: {pyd_file}")
        print('='*60)
        matches = search_activation_strings(pyd_file)
        if matches:
            for m in matches:
                print(f"  {m}")
        else:
            print("  未找到激活相关字符串")

print("\n\n完成!")