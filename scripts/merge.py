import requests
import base64
import yaml
import json

urls = [
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/wenode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/v2rayshare.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodefree.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodev2ray.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/ndnode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt"
]

proxies = []

for url in urls:
    try:
        print(f"Fetching {url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        content = base64.b64decode(resp.text.strip() + '===').decode(errors="ignore")
        for line in content.splitlines():
            if line.startswith("vmess://"):
                vmess_raw = line[8:]
                try:
                    vmess_json = base64.b64decode(vmess_raw + '===').decode()
                    vmess = json.loads(vmess_json)
                    node = {
                        "name": vmess.get("ps", f"{vmess['add']}:{vmess['port']}"),
                        "type": "vmess",
                        "server": vmess["add"],
                        "port": int(vmess["port"]),
                        "uuid": vmess["id"],
                        "alterId": int(vmess.get("aid", 0)),
                        "cipher": "auto",
                        "tls": vmess.get("tls", "") == "tls",
                        "network": vmess.get("net", "tcp"),
                        "udp": True
                    }
                    if vmess.get("net") == "ws":
                        node["ws-opts"] = {
                            "path": vmess.get("path", ""),
                            "headers": {
                                "Host": vmess.get("host", "")
                            }
                        }
                    proxies.append(node)
                except Exception as e:
                    print(f"Error decoding vmess: {e}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

config = {
    "port": 7890,
    "socks-port": 7891,
    "allow-lan": True,
    "mode": "Rule",
    "log-level": "info",
    "external-controller": "127.0.0.1:9090",
    "proxies": proxies,
    "proxy-groups": [
        {
            "name": "🚀 节点选择",
            "type": "select",
            "proxies": [p["name"] for p in proxies]
        }
    ],
    "rules": [
        "MATCH,🚀 节点选择"
    ]
}

with open("merged_clash.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True)

print("✅ 合并完成，生成 merged_clash.yaml")
