
import json

filename = "sensors.jsonl"
devices = {}
valid_count = 0
corrupted_count = 0

with open(filename, "r") as file:
    for line in file:
        try:
            data = json.loads(line)

            device = data["device"]
            temp = float(data["temperature"])

            if not isinstance(device, str) or not device.strip():
                raise ValueError("Invalid device")

            if not isinstance(data["temperature"], (int, float)) or isinstance(data["temperature"], bool):
                raise ValueError("Temperature must be numeric")

            if device not in devices:
                devices[device] = []

            devices[device].append(temp)
            valid_count += 1

        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            corrupted_count += 1

# Display statistics
print("Device Temperature Statistics")

for device, temps in devices.items():
    print("\nDevice:", device)
    print("Minimum:", min(temps), "°C")
    print("Maximum:", max(temps), "°C")
    print("Average:", round(sum(temps) / len(temps), 2), "°C")

print("\nValid Records:", valid_count)
print("Corrupted Records:", corrupted_count)
