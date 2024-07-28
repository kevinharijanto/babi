import requests
from urllib.parse import parse_qs
from colorama import init, Fore
import sys
import time
import random
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
import json
init(autoreset=True)

def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

# Function to read data from akun.txt
with open('query.txt', 'r') as file:
    lines = file.readlines()

# Extract authorization data from each line
# authorizations = [parse_qs(line.strip()) for line in lines if line.strip()]
authorizations = [line.strip() for line in lines]

def get_uname(auth):
    parsed = urllib.parse.parse_qs(auth)
    data = parsed.get('user', [None])[0]
    userdata = json.loads(data)
    return userdata.get('username')

def get_token(auth):
    # Step 1: Get Token
    url = "https://api.prod.piggypiggy.io/tgBot/login"
    parsed = urllib.parse.parse_qs(auth)
    params = {
        "query_id"  : parsed.get('query_id', [None])[0],
        "user"      : parsed.get('user', [None])[0],
        "auth_date" : parsed.get('auth_date', [None])[0],
        "hash"      : parsed.get('hash', [None])[0],
    }

    try:
        response = requests.get(url, params=params)
        # Check if GET request is successful
        if response.status_code == 200:
            print(Fore.GREEN + "Token Berhasil Didapatkan!")
            data = response.json()
            # print(data.get('data', {}).get('newPlayer')) # true = akun baru, false = akun lama
            token = data.get('data', {}).get('token', 'No Token Found')
            return token
        elif response.status_code not in [500, 503, 502, 520, 521]:
            print(f"Request with token {auth} failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"get token error with token auth: {e}")

def get_player_info(headers, auth, index):
    url = "https://api.prod.piggypiggy.io/game/GetPlayerBase"
   
    response_game = requests.post(url, headers=headers)
    # Print response from /game/GetPlayerBase
    if response_game.status_code == 200:
        # print(Fore.GREEN + "Game data berhasil didapatkan!")
        game_data   = response_game.json().get('data', {})
        balance     = game_data.get('currency', 'No Balance')
        salary      = game_data.get('currrencyPool', 'No Salary')
        result = (
            f"{get_random_color()}{index+1} | "
            f"{get_random_color()}{get_uname(auth)} | "
            f"{get_random_color()}Balance: {balance} | "
            f"{get_random_color()}Salary: {salary}"
        )
        return result
        # player_id = game_data.get('playerID', 0)

def get_task_info(headers):
    task_url = "https://api.prod.piggypiggy.io/game/GetDailyTaskInfo"
    payload = {"PlayerID": 0}
    try:
        response = requests.post(task_url, headers=headers, json=payload)
        if response.status_code == 200:
            task_list = response.json().get('data', {})
            return task_list
        else:
            print(Fore.RED + f"Request for Task failed with status code: {response.status_code}", end='')
            time.sleep(1)  # Add a small delay to make it readable

    except requests.exceptions.RequestException as e:
        print(f"gagal mengerjakan task: {e}")

def check_and_run_task(headers, task_list):
    task_a = task_list['mapTask']
    for key, value in task_a.items():
        # print(f"Key: {key}, Complete Count: {value['compeleteCount']}")
        match key:
            case '1001':
                if value['compeleteCount'] < 2:
                    run_task(headers, 1001)
                    print('Menyelesaikan task 1, tunggu 30 detik..')
                    time.sleep(31)
                    claim_task(headers, 1001)
                    print('Sukses claim task 1')

            case '1002':
                if value['compeleteCount'] < 5:
                    run_task(headers, 1002)
                    print('Menyelesaikan task 2, tunggu 20 detik..')
                    time.sleep(21)
                    claim_task(headers, 1002)
                    print('Sukses claim task 2')
            
            case '1003':
                if value['compeleteCount'] < 8:
                    run_task(headers, 1003)
                    print('Menyelesaikan task 3, tunggu 10 detik..')
                    time.sleep(11)
                    claim_task(headers, 1003)
                    print('Sukses claim task 3')

            case '1004':
                if value['compeleteCount'] < 8:
                    run_task(headers, 1004)
                    print('Menyelesaikan task 4, tunggu 20 detik..')
                    time.sleep(21)
                    claim_task(headers, 1004)
                    print('Sukses claim task 4')

            case '1005':
                if value['compeleteCount'] < 5:
                    run_task(headers, 1005)
                    print('Menyelesaikan task 5, tunggu 10 detik..')
                    time.sleep(11)
                    claim_task(headers, 1005)
                    print('Sukses claim task 5')

            case '1006':
                if value['compeleteCount'] < 5:
                    run_task(headers, 1006)
                    print('Menyelesaikan task 6, tunggu 30 detik..')
                    time.sleep(31)
                    claim_task(headers, 1006)
                    print('Sukses claim task 6')

            case '9001':
                if value['compeleteCount'] < 1:
                    run_task(headers, 9001)
                    print('Menyelesaikan task 7, tunggu 2 detik..')
                    time.sleep(1)
                    claim_task(headers, 9001)
                    print('Sukses claim task 7')

            case '9002':
                if value['compeleteCount'] < 1:
                    invite(headers, 9002)
                    print('Menyelesaikan task 8, tunggu 2 detik..')
                    time.sleep(1)
                    claim_task(headers, 9002)
                    print('Sukses claim task 8')

            case '9003':
                if value['compeleteCount'] < 1:
                    time.sleep(1)
                    print('Menyelesaikan task 9, tunggu 2 detik..')
                    claim_task(headers, 9003)
                    print('Sukses claim task 9')

    print("All Task Done!")

def run_task(headers, task_id):
    task_url = "https://api.prod.piggypiggy.io/game/TakeTask"
    payload = {"TaskID": task_id, "PlayerID": 0}
    try:
        response = requests.post(task_url, headers=headers, json=payload)
        if response.status_code == 200:
            task_response = response.json()
            if task_response.get('code') == 0:
                print(Fore.GREEN + f"Task {task_id} berhasil dikerjakan!")
                # last_task_id = task_id  # Save the successful task ID
                # time.sleep(10) # ambil dr database brp lama waktu tunggu
                #claim task
                # bisa juga, hajar gas semua task, baru claim last task aja
        else:
            print(Fore.RED + f"Request for Task {task_id} failed with status code: {response.status_code}", end='')
            time.sleep(1)  # Add a small delay to make it readable

    except requests.exceptions.RequestException as e:
        print(f"gagal mengerjakan task: {e}")

def claim_task(headers, task_id):
    task_url = "https://api.prod.piggypiggy.io/game/CompleteTask"
    payload = {"TaskID": task_id, "PlayerID": 0}
    try:
        response = requests.post(task_url, headers=headers, json=payload)
        if response.status_code == 200:
            task_response = response.json()
            if task_response.get('code') == 0:
                print(Fore.GREEN + f"Task {task_id} berhasil diclaim!")
                # last_task_id = task_id  # Save the successful task ID
                # time.sleep(10) # ambil dr database brp lama waktu tunggu
                #claim task
        else:
            print(Fore.RED + f"Request for Task {task_id} failed with status code: {response.status_code}", end='')
            time.sleep(1)  # Add a small delay to make it readable

    except requests.exceptions.RequestException as e:
        print(f"gagal mengerjakan task: {e}")    

def invite(headers, bonus_id):
    task_url = "https://api.prod.piggypiggy.io/game/AddSchedule"
    payload = {"Type": 1, "Id": bonus_id, "PlayerID": 0}
    try:
        response = requests.post(task_url, headers=headers, json=payload)
        if response.status_code == 200:
            task_response = response.json()
            if task_response.get('code') == 0:
                print(Fore.GREEN + f"Task {bonus_id} berhasil diclaim!")
                # last_task_id = task_id  # Save the successful task ID
                # time.sleep(10) # ambil dr database brp lama waktu tunggu
                #claim task
        else:
            print(Fore.RED + f"Request for Task {bonus_id} failed with status code: {response.status_code}", end='')
            time.sleep(1)  # Add a small delay to make it readable
    except requests.exceptions.RequestException as e:
        print(f"gagal mengerjakan task: {e}") 
    # json = {'Type': 1, 'Id': 9002, 'PlayerID': 0} # type 1
    # json = {'Type': 2, 'Id': 1101, 'PlayerID': 0} # type 2 buat achievement

def add_and_claim_bonus(headers):
    # claim all bonus
    addBonus(headers, 1001)
    print('Menyelesaikan bonus 1..')
    time.sleep(1)
    claimBonus(headers, 1001)
    print('Sukses bonus 1')

    addBonus(headers, 1101)
    print('Menyelesaikan bonus 2..')
    time.sleep(1)
    claimBonus(headers, 1101)
    print('Sukses bonus 2')

    addBonus(headers, 1201)
    print('Menyelesaikan bonus 3..')
    time.sleep(1)
    claimBonus(headers, 1201)
    print('Sukses bonus 3')

    addBonus(headers, 1301)
    print('Menyelesaikan bonus 4..')
    time.sleep(1)
    claimBonus(headers, 1301)
    print('Sukses bonus 4')

    print("Sukses all bonus")

def addBonus(headers, bonus_id):
    task_url = "https://api.prod.piggypiggy.io/game/AddSchedule"
    payload = {"Type": 2, "Id": bonus_id, "PlayerID": 0}
    try:
        response = requests.post(task_url, headers=headers, json=payload)
        if response.status_code == 200:
            task_response = response.json()
            if task_response.get('code') == 0:
                print(Fore.GREEN + f"Task {bonus_id} berhasil diclaim!")
                # last_task_id = task_id  # Save the successful task ID
                # time.sleep(10) # ambil dr database brp lama waktu tunggu
                #claim task
        else:
            print(Fore.RED + f"Request for Task {bonus_id} failed with status code: {response.status_code}", end='')
            time.sleep(1)  # Add a small delay to make it readable

    except requests.exceptions.RequestException as e:
        print(f"gagal mengerjakan task: {e}") 

def claimBonus(headers, bonus_id):
    task_url = "https://api.prod.piggypiggy.io/game/CompleteAchievement"
    payload = {"AchievementID": bonus_id, "PlayerID": 0}
    try:
        response = requests.post(task_url, headers=headers, json=payload)
        if response.status_code == 200:
            task_response = response.json()
            if task_response.get('code') == 0:
                print(Fore.GREEN + f"Task {bonus_id} berhasil diclaim!")
                # last_task_id = task_id  # Save the successful task ID
                # time.sleep(10) # ambil dr database brp lama waktu tunggu
                #claim task
        else:
            print(Fore.RED + f"Request for Task {bonus_id} failed with status code: {response.status_code}", end='')
            time.sleep(1)  # Add a small delay to make it readable

    except requests.exceptions.RequestException as e:
        print(f"gagal mengerjakan task: {e}") 

def run_bot(index, auth):  
    while True:
        try:
            token = get_token(auth)
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": f"bearer {token}",
                "Cache-Control": "no-cache",
                "Content-Length": "0",
                "Content-Type": "application/json",
                "Origin": "https://restaurant-v2.piggypiggy.io",
                "Pragma": "no-cache",
                "Referer": "https://restaurant-v2.piggypiggy.io/",
                "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36"
            }
            
            # task_list = get_task_info(headers)
            # check_and_run_task(headers, task_list)
            claim_task(headers,9001)
            result = get_player_info(headers, auth, index)
            return result
            
        except Exception as e:
            return Fore.RED + f"Error fetching data for Akun {index + 1}: {e}"
 
for index, auth in enumerate(authorizations):
    run_bot(index, auth)

# def countdown_timer(seconds):
#     while seconds > 0:
#         mins, secs = divmod(seconds, 60)
#         time_format = '{:02d}:{:02d}'.format(mins, secs)
#         print(time_format, end='\r')  # Print on the same line
#         time.sleep(1)
#         seconds -= 1
    
#     print("00:00")  # Print the final countdown time
#     print("Time's up!")

# while True:
#     results = []        
#     # Use ThreadPoolExecutor to make requests concurrently
#     with ThreadPoolExecutor(max_workers=len(authorizations)) as executor:
#         futures = [executor.submit(run_bot, index, auth) for index, auth in enumerate(authorizations)]
#         for future in futures:
#             result = future.result()  # Wait for all threads to complete
#             if result:
#                 results.append(result)
    
#     if results:
#         # Clear the previous output
#         print("\033c", end="")  # ANSI escape code to clear the screen
#         # Print all results at once
#         print("\n".join(results), end="\r", flush=True)
    
#     countdown_timer(900)
#     # time.sleep(900)  # 15 menit