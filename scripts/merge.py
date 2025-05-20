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
        print(f"🔗 正在获取：{url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        decoded = base64.b64decode(resp.text.strip() + '===').decode(errors="ignore")
        lines = [line.strip() for line in decoded.splitlines() if line.strip()]
        all_lines.extend(lines)
    except Exception as e:
        print(f"❌ 获取失败：{url} 错误：{e}")

# 保存为 merged（原始节点列表）
with open("merged", "w", encoding="utf-8") as f:
    for line in all_lines:
        f.write(line + "\n")

print("✅ 成功合并所有订阅，输出为 merged")
