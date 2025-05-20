import requests
import base64
import json
import re

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

valid_nodes = []

def is_valid_vmess(line):
    try:
        decoded = base64.b64decode(line[8:] + "==").decode('utf-8')
        data = json.loads(decoded)
        return "add" in data and "port" in data and "id" in data
    except Exception:
        return False

def is_valid_vless_or_trojan(line):
    # vless://uuid@host:port?param=xxx#name
    return bool(re.match(r'^(vless|trojan)://[a-zA-Z0-9\-_.@:]+(:\d+)?', line))

def is_valid_ss(line):
    try:
        if '#' in line:
            line = line.split('#')[0]
        content = line[5:]
        if '@' in base64.b64decode(content + "==").decode('utf-8'):
            return True
        return False
    except Exception:
        return False

def is_valid_node(line):
    line = line.strip()
    if line.startswith('vmess://'):
        return is_valid_vmess(line)
    elif line.startswith('vless://') or line.startswith('trojan://'):
        return is_valid_vless_or_trojan(line)
    elif line.startswith('ss://'):
        return is_valid_ss(line)
    return False

for url in urls:
    try:
        print(f"📥 获取：{url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.strip().splitlines()
        for line in lines:
            line = line.strip()
            if is_valid_node(line):
                valid_nodes.append(line)
            else:
                print(f"⚠️ 无效节点：{line[:60]}...")
    except Exception as e:
        print(f"❌ 获取失败 {url}：{e}")

# 去重
unique_nodes = list(dict.fromkeys(valid_nodes))

# 输出 merged.txt
with open("merged.txt", "w", encoding="utf-8") as f:
    f.writelines(node + "\n" for node in unique_nodes)

print(f"✅ 合并完成，合法节点数：{len(unique_nodes)}")

# 输出 base64 订阅
base64_encoded = base64.b64encode('\n'.join(unique_nodes).encode('utf-8')).decode('utf-8')

with open("merged_base64.txt", "w", encoding="utf-8") as f:
    f.write(base64_encoded)

print("✅ Base64 已写入 merged_base64.txt")
