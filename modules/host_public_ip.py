import requests


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip_data = response.json()
        return ip_data["ip"]
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None


def main():
    public_ip = get_public_ip()
    if public_ip:
        print(f"Public IP Address: {public_ip}")
    else:
        print("Failed to retrieve public IP.")


if __name__ == "__main__":
    main()
