import leetcode
import os
import shutil
import json
import base64
import win32crypt
from Cryptodome.Cipher import AES
from sqlalchemy import create_engine, text

def get_encryption_key():
    """Retrieve Chrome's AES encryption key."""
    local_state_path = os.path.join(
        os.getenv("APPDATA"), "..", "Local", "Google", "Chrome", "User Data", "Local State"
    )

    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.loads(file.read())

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # Strip the "DPAPI" prefix

    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def decrypt_cookie(encrypted_cookie, key):
    """Decrypt Chrome's AES-encrypted cookies."""
    try:
        iv = encrypted_cookie[3:15]
        encrypted_cookie = encrypted_cookie[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_cookie)[:-16].decode()
    except:
        return win32crypt.CryptUnprotectData(encrypted_cookie, None, None, None, 0)[1]


def get_session_info():
    """Retrieve LEETCODE_SESSION and CSRF token from Chrome's cookies database."""
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

def get_user_problems(session, csrf):
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

    #user_info = get_session_info()
    # if not user_info[0] or not user_info[1]:
    #     raise ValueError("Error in accessing user's session info")

    # session = user_info[0]
    # csrf = user_info[1]
    configuration = leetcode.Configuration()

    configuration.api_key['x-csrftoken'] = csrf
    configuration.api_key['csrftoken'] = csrf
    configuration.api_key['LEETCODE_SESSION'] = session
    configuration.api_key['Referer'] = 'https://leetcode.com'
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))
    api_response = api_instance.api_problems_topic_get(topic="algorithms")

    slug_to_solved_status = {
        pair.stat.question__title_slug: True if pair.status == "ac" else False
        for pair in api_response.stat_status_pairs
    }

    completed = []
    for i in slug_to_solved_status:
        #print(i, slug_to_solved_status[i])
        if i in problems and slug_to_solved_status[i]:
            completed.append(i)
    return completed

if "__main__" == __name__:
    get_user_problems()