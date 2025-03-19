import leetcode
import browser_cookie3

def get_session_info():
    leetcode_session = None
    token = None
    cookies = browser_cookie3.chrome(domain_name='leetcode.com')
    for cookie in cookies:
        if cookie.name == 'LEETCODE_SESSION':
            leetcode_session = cookie.value
        elif cookie.name == 'csrftoken':
            token = cookie.value
    return [leetcode_session, token]

def get_user_problems():
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

    user_info = get_session_info()
    if not user_info[0] or not user_info[1]:
        raise ValueError("Error in accessing user's session info")

    session = user_info[0]
    csrf = user_info[1]
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