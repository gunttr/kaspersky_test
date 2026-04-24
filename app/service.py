#!.venv/bin/python3.12

from prometheus_client import Gauge, start_http_server
import time, subprocess, os

# читерный способ
def try_systemd_detect_virt() -> str | None:
    if (subprocess.run("systemd-detect-virt --container --quiet", shell=True).returncode == 0):
        return "container"
    if (subprocess.run("systemd-detect-virt --vm --quiet", shell=True).returncode == 0):
        return "vm" 

    return None

def is_running_in_docker() -> bool:
    # самый простой способ
    if os.path.exists("/.dockerenv"):
        return True
    
    # немного заковыристее
    output = subprocess.run(
        'mount | grep "overlay on / type overlay (rw,relatime,lowerdir=/var/lib/docker',
        shell=True,
        capture_output=True,
        text=True
    )

    if output.returncode == 0:
        return True
     
    return False

# для подмана
def is_running_in_podman() -> bool:
    if os.getenv("container"):
        return True
    
    return False

def is_running_in_vm() -> bool:
    path: str = "/sys/class/dmi/id/product_name"

    if os.path.exists(path):
        with open(path, "r") as file:
            name: str = file.read().lower()

            if "virtual" in name or "kvm" in name or "vmware" in name:
                return True

    return False

def get_host_type() -> str:
    
    result: str | None = try_systemd_detect_virt()
    
    if result:
        return result

    if is_running_in_docker() or is_running_in_podman():
        return "container"
    
    if is_running_in_vm():
        return "vm"

    return "baremetal"


def main():
    host_type_metric: Gauge = Gauge("host_type", "Type of host", ["type"])
    host_type: str = get_host_type()
    print(f"host_type: {host_type}")
    host_type_metric.labels(type=host_type).set(1)
    start_http_server(port=8080)
    
    print("The server is running")
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
