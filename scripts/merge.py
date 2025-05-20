import requests
import base64
import re

# 支持的协议开头
SUPPORTED_SCHEMES = ("vmess://", "vless://", "ss://", "trojan://")

# 节点订阅链接
urls = [
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/wenode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/v2rayshare.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodefree.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodev2ray.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/ndnode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt"
]

all_lines = []

def is_valid_node(line):
    # 判断是否是支持的代理协议格式
    return line.startswith(SUPPORTED_SCHEMES)

for url in urls:
    try:
        print(f"📥 获取：{url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = [line.strip() for line in resp.text.strip().splitlines() if is_valid_node(line.strip())]
        all_lines.extend(lines)
    except Exception as e:
        print(f"⚠️ 错误处理 {url}：{e}")

# 去重并保留顺序
unique_lines = list(dict.fromkeys(all_lines))

# 写入纯文本节点 merged.txt
with open("merged.txt", "w", encoding="utf-8") as f:
    f.writelines(line + "\n" for line in unique_lines)

print(f"✅ 成功合并 {len(unique_lines)} 条合法节点，生成 merged.txt")

# 合并为 base64 并写入 merged_base64
combined_text = '\n'.join(unique_lines)
base64_encoded = base64.b64encode(combined_text.encode("utf-8")).decode("utf-8")

with open("merged_base64", "w", encoding="utf-8") as f:
    f.write(base64_encoded)

print("✅ 已写入 Base64 订阅内容到 merged_base64")
