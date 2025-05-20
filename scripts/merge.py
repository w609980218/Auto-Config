import requests
import base64

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

for url in urls:
    try:
        print(f"📥 获取：{url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = [line.strip() for line in resp.text.strip().splitlines() if line.strip()]
        all_lines.extend(lines)
    except Exception as e:
        print(f"⚠️ 错误处理 {url}：{e}")

unique_lines = list(dict.fromkeys(all_lines))

with open("merged.txt", "w", encoding="utf-8") as f:
    for line in unique_lines:
        f.write(line + "\n")

print(f"✅ 成功合并 {len(unique_lines)} 条，生成 merged.txt")

with open('merged.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

combined_text = '\n'.join(lines)

base64_bytes = base64.b64encode(combined_text.encode('utf-8'))
base64_str = base64_bytes.decode('utf-8')

# 写入 Base64 订阅文件
with open("merged_base64.txt", "w", encoding="utf-8") as f:
    f.write(base64_str)

print("✅ 已写入 Base64 订阅内容到 merged_base64.txt")
