
# Optimized Password Audit with Pattern Constraints

# Trie Node
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def contains_banned_word(self, password):
        password = password.lower()

       
        for i in range(len(password)):
            node = self.root
            j = i

            while j < len(password) and password[j] in node.children:
                node = node.children[password[j]]

                if node.is_end:
                    return True

                j += 1

        return False
    
banned_words = ["admin", "password", "hello", "qwerty"]

trie = Trie()
for word in banned_words:
    trie.insert(word)


def audit_password(password):
    # Check length first
    if not 6 <= len(password) <= 12:
        return "WEAK_LENGTH"

    # Check character patterns
    has_lower = any(ch.islower() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(ch in "$#@" for ch in password)

    if not (has_lower and has_upper and has_digit and has_special):
        return "WEAK_PATTERN"

    if trie.contains_banned_word(password):
        return "COMPROMISED"

    
    for i in range(len(password) - 3):
        if password[i] == password[i + 1] == password[i + 2] == password[i + 3]:
            return "WEAK_PATTERN"

    return "STRONG"

passwords = [
    "Abc@123",
    "abc",
    "abcdef1@",
    "Admin@123",
    "Abcd1111@A"
]

for password in passwords:
    print(password, ":", audit_password(password))
