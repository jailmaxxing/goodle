import requests

# === CONFIGURATION ===
API_TOKEN = "58wYM1e5IHKb5hPrDBrK0lLWtCqLtz05dvDT9qMT"
ZONE_NAME = "jaildev.site"
RECORD_NAME = "goodle.jaildev.site"
PROXIED = False  # Set to True if you want Cloudflare proxy (orange cloud)
TTL = 120        # Time-to-live in seconds

# === HEADERS FOR CLOUDFLARE API ===
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# === STEP 1: Get your public IP ===
ip = requests.get("https://ipv4.icanhazip.com").text.strip()
print(f"[INFO] Current IP: {ip}")

# === STEP 2: Get Zone ID ===
zone_url = f"https://api.cloudflare.com/client/v4/zones?name={ZONE_NAME}"
zone_response = requests.get(zone_url, headers=headers).json()

if not zone_response["success"]:
    print("[ERROR] Could not fetch Zone ID.")
    print(zone_response)
    exit()

zone_id = zone_response["result"][0]["id"]
print(f"[INFO] Zone ID: {zone_id}")

# === STEP 3: Get Record ID ===
record_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={RECORD_NAME}"
record_response = requests.get(record_url, headers=headers).json()

if not record_response["success"] or not record_response["result"]:
    print("[ERROR] Could not find DNS record.")
    print(record_response)
    exit()

record = record_response["result"][0]
record_id = record["id"]
current_ip = record["content"]

print(f"[INFO] Record ID: {record_id}")
print(f"[INFO] Current DNS IP: {current_ip}")

# === STEP 4: Update if IP has changed ===
if ip != current_ip:
    print("[INFO] IP has changed. Updating DNS record...")

    update_data = {
        "type": "A",
        "name": RECORD_NAME,
        "content": ip,
        "ttl": TTL,
        "proxied": PROXIED
    }

    update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    update_response = requests.put(update_url, headers=headers, json=update_data).json()

    if update_response["success"]:
        print("[SUCCESS] DNS record updated successfully.")
    else:
        print("[ERROR] Failed to update DNS record.")
        print(update_response)
else:
    print("[INFO] IP has not changed. No update needed.")
