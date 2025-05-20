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
        print(f"Fetching {url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        # 解码 base64 内容
        b64 = resp.text.strip()
        # 自动补等号对齐
        b64 += '=' * (-len(b64) % 4)
        decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
        lines = [line.strip() for line in decoded.splitlines() if line.strip()]
        all_lines.extend(lines)
    except Exception as e:
        print(f"⚠️ 无法处理 {url}：{e}")

# 去重（可选）
unique_lines = list(dict.fromkeys(all_lines))

# 写入 merged.txt
with open("merged.txt", "w", encoding="utf-8") as f:
    for line in unique_lines:
        f.write(line + "\n")

print("✅ 成功合并生成 merged.txt")
