import json
import time
import urllib.request
import urllib.error

API_URL = "http://localhost:8001/api/v1"

scenarios = [
    {"brand_name": "Example", "target_url": "https://example.com"}, 
    {"brand_name": "ImpossibleToFindBrand", "target_url": "https://www.google.com"},
    {"brand_name": "Python", "target_url": "https://www.python.org/"}
]

def post_mission(data):
    req = urllib.request.Request(
        f"{API_URL}/missions/",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error posting mission to {API_URL}: {e}")
        print("Make sure the Docker container is running (docker-compose up)")
        return None

def get_mission(mid):
    try:
        with urllib.request.urlopen(f"{API_URL}/missions/{mid}") as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        return None

def main():
    print("Populating database with test scenarios...")
    ids = []
    for sc in scenarios:
        res = post_mission(sc)
        if res:
            print(f"CREATED Mission {res['id']}: {sc['brand_name']} on {sc['target_url']}")
            ids.append(res['id'])
        else:
            print(f"FAILED to create mission for {sc['brand_name']}")
    
    if not ids:
        return

    print("\nSimulating wait for processing (15 seconds)...")
    time.sleep(15)
    
    print("\nRetrieving statuses:")
    for mid in ids:
        m = get_mission(mid)
        if m:
            print(f"Mission {mid}: [{m['status']}] Evidence: {m.get('evidence_path')}")

if __name__ == "__main__":
    main()
