def is_ec2_linux():
    import os

    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """
    EC2 프라이빗 ip 조회 후 리스트로 반환
    """
    from urllib.request import urlopen

    if not is_ec2_linux():
        return None
    try:
        response = urlopen("http://169.254.169.254/latest/meta-data/local-ipv4")
        ec2_ip = response.read().decode("utf-8")
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None
