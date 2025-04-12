import socket, struct, random, time
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
timestamp = now.strftime("%Y-%m-%d %H:%M UTC")

def chechubben(server, timeout=5):
    udp_socket = None
    try:
        if ":" in server:
            host, port = server.split(":")
            targetServer = (host, int(port))
        else:
            targetServer = (server, 19132)

        magicCrap = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx'
        pingPacket = b'\x02' + struct.pack(">q", random.randint(5, 20)) + magicCrap

        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.settimeout(timeout)
        udp_socket.sendto(pingPacket, targetServer)
        data = udp_socket.recvfrom(2048)[0]
        len_val = data[34]
        serverName = data[35:35 + len_val].decode('utf-8').split(';')[2]
        return f"✅ Online - '{serverName}'"
    except socket.gaierror:
        return "❌ Server did not respond at all (DNS failed)"
    except socket.timeout:
        return f"⚠️ Timed out after {timeout}s"
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        if udp_socket:
            udp_socket.close()

def generate_html_report(results):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>MCPI Server Status</title>")
        f.write('<style>body{font-family:sans-serif;padding:1em;}li{margin:.5em 0;}</style>')
        f.write("</head><body>")
        f.write(f"<p>Last updated: {timestamp}</p>")
        for server, status in results:
            f.write(f"<li><strong>{server}</strong>: {status}</li>")
        f.write("</ul></body></html>")

if __name__ == "__main__":
    servers = [
        "mcpi.izor.in",
        "unoffical-mcpi-rd.duckdns.org:5000",
        "retrocraft.bounceme.net"
    ]

    results = []
    for server in servers:
        status = chechubben(server)
        results.append((server, status))

    generate_html_report(results)
