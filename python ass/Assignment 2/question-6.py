
from collections import deque
from datetime import datetime, timedelta

X = 3   # Minimum failed attempts
T = 10  # Time window in minutes

logs = [
    ("10:00", "Amit", "192.168.1.1", "FAIL"),
    ("10:02", "Amit", "192.168.1.1", "FAIL"),
    ("10:05", "Amit", "192.168.1.1", "FAIL"),
    ("10:07", "Amit", "192.168.1.5", "SUCCESS"),
    ("10:08", "Rahul", "192.168.1.2", "FAIL"),
    ("10:09", "Rahul", "192.168.1.2", "SUCCESS")
]

# Sort logs by timestamp
logs.sort(key=lambda x: datetime.strptime(x[0], "%H:%M"))

windows = {}
suspicious = set()

for time_str, user, ip, status in logs:
    current_time = datetime.strptime(time_str, "%H:%M")

    if user not in windows:
        windows[user] = deque()

    window = windows[user]

    # Remove failures older than T minutes
    while window and current_time - window[0][0] > timedelta(minutes=T):
        window.popleft()

    if status == "FAIL":
        window.append((current_time, ip))

    elif status == "SUCCESS":
        if len(window) >= X:
            if any(fail_ip != ip for _, fail_ip in window):
                suspicious.add(user)

        window.clear()

print("Suspicious Users:")
if suspicious:
    for user in sorted(suspicious):
        print(user)
else:
    print("None")
