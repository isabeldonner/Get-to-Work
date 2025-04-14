import leetcode
import os
import shutil
import json
import base64
import win32crypt
from Cryptodome.Cipher import AES
from sqlalchemy import create_engine, text
import leetcode.auth
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def get_encryption_key():
    local_state_path = os.path.join(
        os.getenv("APPDATA"), "..", "Local", "Google", "Chrome", "User Data", "Local State"
    )

    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.loads(file.read())

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]

    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def decrypt_cookie(encrypted_cookie, key):
    try:
        iv = encrypted_cookie[3:15]
        encrypted_cookie = encrypted_cookie[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_cookie)[:-16].decode()
    except:
        return win32crypt.CryptUnprotectData(encrypted_cookie, None, None, None, 0)[1]


def get_session_info():
    cookies_db_path = os.path.join(
        os.getenv("APPDATA"), "..", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies"
    )

    temp_db = "temp_cookies.db"
    shutil.copy2(cookies_db_path, temp_db)  # Copy DB to avoid lock issues

    # Create SQLAlchemy database engine
    engine = create_engine(f"sqlite:///{temp_db}")

    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%leetcode.com%'"
        ))

        key = get_encryption_key()
        session, csrf = None, None

        for row in result:
            name, encrypted_value = row
            decrypted_value = decrypt_cookie(encrypted_value, key)

            if name == "LEETCODE_SESSION":
                session = decrypted_value
            elif name == "csrftoken":
                csrf = decrypted_value

    os.remove(temp_db)  # Clean up the temporary database file
    return [session, csrf]

def get_submission_id(username, problems):
    graphql_url = "https://leetcode.com/graphql"
    query_recent = '''
        query recentAcSubmissions($username: String!, $limit: Int!) {
          recentAcSubmissionList(username: $username, limit: $limit) {
            id
            title
            titleSlug
            timestamp
          }
        }
        '''
    variables_recent = {
        "username": username,
        "limit": 75
    }
    response_recent = requests.post(
        graphql_url,
        json={"query": query_recent, "variables": variables_recent}
    )
    data_recent = response_recent.json()
    submissions = data_recent.get("data", {}).get("recentAcSubmissionList", [])
    if not submissions:
        print("No submissions found")
        return None

    ids = {}
    for i in range(len(submissions)):
        if submissions[i]["titleSlug"] in problems:
            ids[submissions[i]["titleSlug"]] = submissions[i]["id"]
    return ids

def get_submission_code(submission_url, session_cookie, csrf_token):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://leetcode.com/")
        time.sleep(1)

        driver.add_cookie({
            "name": "LEETCODE_SESSION",
            "value": session_cookie,
            "domain": ".leetcode.com",
            "secure": True
        })
        driver.add_cookie({
            "name": "csrftoken",
            "value": csrf_token,
            "domain": ".leetcode.com",
            "secure": True
        })
        driver.get(submission_url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-track-load='code_editor']"))
        )

        elements = driver.find_elements(By.TAG_NAME, "PRE")
        if not elements:
            print("No solution element found")
            return None
        else:
            candidates = []
            for element in elements:
                code = element.get_attribute("innerText")
                if "Solution" in code:
                    candidates.append(code)

            size = len(candidates[0])
            index = 0
            for i in range(len(candidates)):
                if len(candidates[i]) >= size:
                    size = len(candidates[i])
                    index = i
            return candidates[index]
    except Exception as e:
        print(f"Scraping error: {str(e)}")
        return None
    finally:
        driver.quit()

def get_user_completed(instance):
    problems = [
        'two-sum',
        'longest-substring-without-repeating-characters',
        'longest-palindromic-substring',
        'container-with-most-water',
        '3sum',
        'remove-nth-node-from-end-of-list',
        'valid-parentheses',
        'merge-two-sorted-lists',
        'merge-k-sorted-lists',
        'search-in-rotated-sorted-array',
        'combination-sum',
        'rotate-image',
        'group-anagrams',
        'maximum-subarray',
        'spiral-matrix',
        'jump-game',
        'merge-intervals',
        'insert-interval',
        'unique-paths',
        'climbing-stairs',
        'set-matrix-zeroes',
        'minimum-window-substring',
        'word-search',
        'decode-ways',
        'validate-binary-search-tree',
        'same-tree',
        'binary-tree-level-order-traversal',
        'maximum-depth-of-binary-tree',
        'construct-binary-tree-from-preorder-and-inorder-traversal',
        'best-time-to-buy-and-sell-stock',
        'binary-tree-maximum-path-sum',
        'valid-palindrome',
        'longest-consecutive-sequence',
        'clone-graph',
        'word-break',
        'linked-list-cycle',
        'reorder-list',
        'maximum-product-subarray',
        'find-minimum-in-rotated-sorted-array',
        'reverse-bits',
        'number-of-1-bits',
        'house-robber',
        'number-of-islands',
        'reverse-linked-list',
        'course-schedule',
        'implement-trie-prefix-tree',
        'design-add-and-search-words-data-structure',
        'word-search-ii',
        'house-robber-ii',
        'contains-duplicate',
        'invert-binary-tree',
        'kth-smallest-element-in-a-bst',
        'lowest-common-ancestor-of-a-binary-search-tree',
        'product-of-array-except-self',
        'valid-anagram',
        'meeting-rooms',
        'meeting-rooms-ii',
        'graph-valid-tree',
        'missing-number',
        'alien-dictionary',
        'encode-and-decode-strings',
        'find-median-from-data-stream',
        'serialize-and-deserialize-binary-tree',
        'longest-increasing-subsequence',
        'coin-change',
        'number-of-connected-components-in-an-undirected-graph',
        'counting-bits',
        'top-k-frequent-elements',
        'sum-of-two-integers',
        'pacific-atlantic-water-flow',
        'longest-repeating-character-replacement',
        'non-overlapping-intervals',
        'subtree-of-another-tree',
        'palindromic-substrings',
        'longest-common-sunsequence'
    ]

    api_response = instance.api_problems_topic_get(topic="algorithms")

    slug_to_solved_status = {
        pair.stat.question__title_slug: True if pair.status == "ac" else False
        for pair in api_response.stat_status_pairs
    }

    completed = []
    for i in slug_to_solved_status:
        # print(i, slug_to_solved_status[i])
        if i in problems and slug_to_solved_status[i]:
            completed.append(i)
    return completed

def get_user_code(session, token, username):
    submissions = {}

    configuration = leetcode.Configuration()
    configuration.api_key['x-csrftoken'] = token
    configuration.api_key['csrftoken'] = token
    configuration.api_key['LEETCODE_SESSION'] = session
    configuration.api_key['Referer'] = 'https://leetcode.com'
    configuration.debug = False
    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    completed = get_user_completed(api_instance)
    submission_ids = get_submission_id(username, completed)
    for problem in completed:
        temp_id = submission_ids[problem]
        url = f"https://leetcode.com/problems/{problem}/submissions/{temp_id}"
        code = get_submission_code(url, session, token)
        submissions[problem] = code

    return submissions