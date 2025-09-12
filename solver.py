import json
import random
import requests
import time
import os
import sys
import warnings

# Suppress InsecureRequestWarning for all cases
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Add resource_path function to handle bundled paths
def resource_path(relative_path):
    """Get the absolute path to a bundled resource, relative to this script's directory."""
    if hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    # Use the directory of this file (solver.py) as the base
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, '..', relative_path)

# Debug flag to control logging verbosity
debug = False  # Set to False to disable detailed debug logs

# Load configuration with dynamic path
config_path = resource_path('input/config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# Load proxies with dynamic path
proxies_path = resource_path('input/proxies.txt')
with open(proxies_path, 'r') as f:
    proxies = f.read().splitlines()

api_key = config["captcha"]["apikeys"]["razorcap"]
url = "https://discord.com/channels/@me"
sitekey = "a9b5fb07-92ff-493f-86fe-352a2803b3df"

class Solver:
    def __init__(self):
        self.proxy_list = proxies

    def get_proxy(self):
        """Select a random proxy from the list."""
        if not self.proxy_list:
            if debug:
                print("[ERROR] No proxies available in proxy list.")
            return None
        return random.choice(self.proxy_list).strip()

    def razorcap(self, rqdata, proxy=None, timeout=120):
        # Get captcha attempts from config
        max_attempts = config["captcha"].get("captcha_attempts", 1)

        # Always send requests without proxies; include proxy in payload
        proxies_for_request = None

        # Determine proxy based on config["captcha"]["proxyless"]
        if config["captcha"]["proxyless"]:
            proxy_to_use = None
        else:
            proxy_to_use = proxy if proxy else self.get_proxy()

        # Clean proxy string to avoid double http:// or https:// prefix
        if proxy_to_use:
            if proxy_to_use.startswith('http://'):
                proxy_to_use = proxy_to_use[len('http://'):]
            elif proxy_to_use.startswith('https://'):
                proxy_to_use = proxy_to_use[len('https://'):]
            proxy_to_use = proxy_to_use.strip()

        # Prepare the payload
        payload = {
            'key': api_key,
            'type': 'hcaptcha_enterprise',
            'data': {
                'sitekey': sitekey,
                'siteurl': "discord.com",
                'proxy': f"http://{proxy_to_use}" if proxy_to_use else None,
                'rqdata': rqdata
            }
        }

        # Log the request details if debug is enabled
        if debug:
            print(
                f"[DEBUG] Sending request to razorcap create_task: URL=https://api.razorcap.live/create_task, Payload={json.dumps(payload, indent=2)}")
            print(f"[WARNING] SSL verification is disabled for this request (verify=False)")

        for attempt in range(1, max_attempts + 1):
            try:
                # Create the captcha solving task
                response = requests.post(
                    'https://api.razorcap.live/create_task',
                    json=payload,
                    timeout=10,
                    proxies=proxies_for_request,
                    verify=False  # Skip SSL verification
                )
                if debug:
                    print(
                        f"[DEBUG] razorcap create_task response: Status={response.status_code}, Response={response.text}")

                if response.status_code != 200:
                    if debug:
                        print(
                            f"[ERROR] Failed to create task (attempt {attempt}/{max_attempts}): Status {response.status_code}, Response: {response.text}")
                    continue

                if "task_id" not in response.json():
                    if debug:
                        print(
                            f"[ERROR] Failed to create task (attempt {attempt}/{max_attempts}): No task_id in response: {response.text}")
                    continue

                task_id = response.json()["task_id"]
                if debug:
                    print(f"[DEBUG] razorcap task created: Task ID={task_id}")

                start_time = time.time()

                # Poll for the solution
                while time.time() - start_time < timeout:
                    result_response = requests.get(
                        f'https://api.razorcap.live/get_result/{task_id}',
                        timeout=10,
                        proxies=proxies_for_request,
                        verify=False
                    )
                    result = result_response.json()
                    if debug:
                        print(
                            f"[DEBUG] razorcap get_result response: Task ID={task_id}, Status={result_response.status_code}, Response={result}")

                    if result["status"] == "solved":
                        solution = result.get("response_key")
                        return solution
                    elif result["status"] == "solving":
                        if debug:
                            print(f"[DEBUG] razorcap task {task_id} is still solving...")
                        time.sleep(1)
                    elif result["status"] == "error":
                        error_message = result.get("error", "Unknown error")
                        if "Failed to solve captcha challenge" in error_message:
                            if debug:
                                print(f"[ERROR] Failed to solve captcha challenge (attempt {attempt}/{max_attempts})")
                        else:
                            if debug:
                                print(
                                    f"[ERROR] razorcap task {task_id} failed with error (attempt {attempt}/{max_attempts}): {error_message}")
                        break
                    else:
                        if debug:
                            print(f"[ERROR] razorcap unknown status: {result['status']}")
                        break

                # Retry with a new proxy if more attempts remain and not proxyless
                if attempt < max_attempts and not config["captcha"]["proxyless"]:
                    if debug:
                        print(f"[DEBUG] Retrying attempt {attempt + 1}/{max_attempts} after failure")
                    proxy_to_use = self.get_proxy()
                    if proxy_to_use:
                        if proxy_to_use.startswith('http://'):
                            proxy_to_use = proxy_to_use[len('http://'):]
                        elif proxy_to_use.startswith('https://'):
                            proxy_to_use = proxy_to_use[len('https://'):]
                        proxy_to_use = proxy_to_use.strip()
                    payload["data"]["proxy"] = f"http://{proxy_to_use}" if proxy_to_use else None
                    time.sleep(1)

            except requests.exceptions.ConnectionError as e:
                if debug:
                    print(
                        f"[ERROR] razorcap request failed - Connection Error (attempt {attempt}/{max_attempts}): {str(e)}")
            except requests.exceptions.Timeout as e:
                if debug:
                    print(f"[ERROR] razorcap request failed - Timeout (attempt {attempt}/{max_attempts}): {str(e)}")
            except Exception as e:
                if debug:
                    print(
                        f"[ERROR] razorcap request failed - General Error (attempt {attempt}/{max_attempts}): {str(e)}")

            if attempt < max_attempts:
                continue

        if debug:
            print("[ERROR] razorcap captcha solving failed after all attempts.")
        return None

    def aiclientz(self, rqdata, proxy=None, timeout=120):
        """AI Clientz captcha solver - faster solving times (6-20s)"""
        # Get captcha attempts from config
        max_attempts = config["captcha"].get("captcha_attempts", 1)
        
        # Get API key from config
        api_key = config["captcha"]["apikeys"].get("aiclientz")
        if not api_key:
            if debug:
                print("[ERROR] No AI Clientz API key found in config")
            return None

        # Always send requests without proxies; include proxy in payload
        proxies_for_request = None

        # Determine proxy based on config["captcha"]["proxyless"]
        if config["captcha"]["proxyless"]:
            proxy_to_use = None
        else:
            proxy_to_use = proxy if proxy else self.get_proxy()

        # Clean proxy string to avoid double http:// or https:// prefix
        if proxy_to_use:
            if proxy_to_use.startswith('http://'):
                proxy_to_use = proxy_to_use[len('http://'):]
            elif proxy_to_use.startswith('https://'):
                proxy_to_use = proxy_to_use[len('https://'):]
            proxy_to_use = proxy_to_use.strip()

        # Prepare the payload for AI Clientz
        payload = {
            'site_key': sitekey,
            'site_url': "discord.com",
            'rqd': rqdata,
            'proxy': f"http://{proxy_to_use}" if proxy_to_use else None,
            'key': api_key
        }

        # Log the request details if debug is enabled
        if debug:
            print(f"[DEBUG] Sending request to AI Clientz: Payload={json.dumps(payload, indent=2)}")

        for attempt in range(1, max_attempts + 1):
            try:
                if debug:
                    print(f"[DEBUG] Using AI Clientz endpoint: solve (10-20s solving time)")
                
                # Create the captcha solving task using the regular solve endpoint
                response = requests.post(
                    'http://captcha.aiclientz.com:1234/solve',
                    json=payload,
                    timeout=30,  # Increased timeout to 30 seconds for 10-20s solving time
                    proxies=proxies_for_request,
                    verify=False  # Skip SSL verification
                )
                
                if debug:
                    print(f"[DEBUG] AI Clientz response: Status={response.status_code}, Response={response.text}")

                if response.status_code != 200:
                    if debug:
                        print(f"[ERROR] Failed to create task (attempt {attempt}/{max_attempts}): Status {response.status_code}, Response: {response.text}")
                    continue

                response_data = response.json()
                if "captcha" not in response_data:
                    if debug:
                        print(f"[ERROR] Failed to create task (attempt {attempt}/{max_attempts}): No captcha in response: {response.text}")
                    continue

                captcha_solution = response_data["captcha"]
                if debug:
                    print(f"[DEBUG] AI Clientz captcha solved: {captcha_solution[:50]}...")

                return captcha_solution

            except requests.exceptions.ConnectionError as e:
                if debug:
                    print(f"[ERROR] AI Clientz request failed - Connection Error (attempt {attempt}/{max_attempts}): {str(e)}")
            except requests.exceptions.Timeout as e:
                if debug:
                    print(f"[ERROR] AI Clientz request failed - Timeout (attempt {attempt}/{max_attempts}): {str(e)}")
            except Exception as e:
                if debug:
                    print(f"[ERROR] AI Clientz request failed - General Error (attempt {attempt}/{max_attempts}): {str(e)}")

            if attempt < max_attempts:
                time.sleep(1)
                continue

        if debug:
            print("[ERROR] AI Clientz captcha solving failed after all attempts.")
        return None

    def check_aiclientz_balance(self):
        """Check the balance of the AI Clientz API key"""
        api_key = config["captcha"]["apikeys"].get("aiclientz")
        if not api_key:
            print("[ERROR] No AI Clientz API key found in config")
            return None

        try:
            payload = {'key': api_key}
            response = requests.post(
                'http://captcha.aiclientz.com:1234/check',
                json=payload,
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"[INFO] AI Clientz Balance - Credits Left: {data.get('credit_left', 'Unknown')}, Credits Used: {data.get('credit_used', 'Unknown')}, Lifetime Credits: {data.get('lifetime_credit', 'Unknown')}")
                return data
            else:
                print(f"[ERROR] Failed to check balance: Status {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            print(f"[ERROR] Error checking AI Clientz balance: {str(e)}")
            return None