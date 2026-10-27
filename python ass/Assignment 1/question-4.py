
import csv
from collections import defaultdict

input_file = "transactions.csv"

credit_total = defaultdict(float)
debit_total = defaultdict(float)

try:
    with open(input_file, "r", newline="") as file, \
         open("credit.csv", "w", newline="") as cf, \
         open("debit.csv", "w", newline="") as df, \
         open("error.csv", "w", newline="") as ef:

        reader = csv.DictReader(file)
        fields = ["account", "type", "amount"]

        cw = csv.DictWriter(cf, fieldnames=fields)
        dw = csv.DictWriter(df, fieldnames=fields)
        ew = csv.writer(ef)

        cw.writeheader()
        dw.writeheader()
        ew.writerow(["row", "account", "type", "amount", "reason"])

        for row_num, row in enumerate(reader, start=2):
            try:
                account = row["account"].strip()
                trans_type = row["type"].strip().lower()
                amount = float(row["amount"])

                if not account:
                    raise ValueError("Missing account")

                if trans_type not in ("credit", "debit"):
                    raise ValueError("Invalid transaction type")

                if amount <= 0:
                    raise ValueError("Amount must be positive")

                clean_row = {
                    "account": account,
                    "type": trans_type,
                    "amount": amount
                }

                if trans_type == "credit":
                    cw.writerow(clean_row)
                    credit_total[account] += amount
                else:
                    dw.writerow(clean_row)
                    debit_total[account] += amount

            except (ValueError, KeyError, TypeError) as e:
                ew.writerow([
                    row_num,
                    row.get("account", ""),
                    row.get("type", ""),
                    row.get("amount", ""),
                    str(e) or "Invalid row"
                ])

except FileNotFoundError:
    print("Error: transactions.csv file not found.")
    raise SystemExit(1)
except OSError as e:
    print("File error:", e)
    raise SystemExit(1)


accounts = set(credit_total) | set(debit_total)
balances = []

for account in accounts:
    net = credit_total[account] - debit_total[account]
    balances.append((account, net))

balances.sort(key=lambda item: abs(item[1]), reverse=True)

print("\nAccount-wise Net Balance Change")
for account, net in balances:
    print(account, ":", round(net, 2))
