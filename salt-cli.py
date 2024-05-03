import argparse
import requests

def determine_syndic_for_minion(target_minion, syndic_urls, auth_token):
    # Query Salt syndics to determine the syndic for the minion
    for syndic_url in syndic_urls:
        response = requests.get(f"{syndic_url}/minions/{target_minion}", headers={"X-Auth-Token": auth_token})
        if response.status_code == 200:
            return syndic_url
    return None

def execute_command_on_syndic(syndic_url, command, target_minion, auth_token):
    # Execute Salt command on the specified syndic
    data = {"client": "local", "tgt": target_minion, "fun": command}
    response = requests.post(f"{syndic_url}/run", headers={"X-Auth-Token": auth_token}, json=data)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Execute Salt commands on minions via syndic")
    parser.add_argument("command", help="Salt command to execute")
    parser.add_argument("target_minion", help="Target minion for the command")
    args = parser.parse_args()

    # Syndic URLs and authentication tokens (replace with your actual values)
    syndic_urls = ["http://master-1:8000", "http://master-2:8000"]
    auth_tokens = {
        "master-1": "9b:be:84:49:d7:d0:a0:8f:e1:f6:96:46:96:82:58:bb:6c:58:e9:32:94:cf:fd:16:e0:78:e3:d7:b7:a6:69:7b",
        "master-2": "72:91:93:6c:5d:d3:21:9c:c7:98:1d:a3:2f:79:57:81:6d:76:19:58:cb:93:15:dc:b4:68:92:d9:d4:21:90:34"
    }

    # Determine syndic for the minion
    for url in syndic_urls:
        syndic_url = determine_syndic_for_minion(args.target_minion, [url], auth_tokens[args.target_minion])
        if syndic_url:
            # Execute command on the correct syndic
            response = execute_command_on_syndic(syndic_url, args.command, args.target_minion, auth_tokens[args.target_minion])
            print(response)
            break
    else:
        print("Minion not found on any syndic.")

if __name__ == "__main__":
    main()
