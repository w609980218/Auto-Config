import requests

# 要抓取的订阅链接列表
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
        # 直接取原始 base64 文本行（不解码）
        lines = [line.strip() for line in resp.text.strip().splitlines() if line.strip()]
        all_lines.extend(lines)
    except Exception as e:
        print(f"⚠️ 错误处理 {url}：{e}")

# 去重（保留顺序，按需保留）
unique_lines = list(dict.fromkeys(all_lines))

# 写入 merged.txt（覆盖旧文件）
with open("merged.txt", "w", encoding="utf-8") as f:
    for line in unique_lines:
        f.write(line + "\n")

print(f"✅ 成功合并 {len(unique_lines)} 条，生成 merged.txt")
