import csv
from collections import defaultdict

INPUT_FILE = "transactions.csv"
FIELDS = ["account", "type", "amount"]


def main():
    credit_totals = defaultdict(float)
    debit_totals = defaultdict(float)

    try:
        with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)

            # Check that the input file has the required column names.
            if not reader.fieldnames:
                raise ValueError("Input CSV is empty or has no header row.")

            normalized_headers = {
                header.strip().lower(): header for header in reader.fieldnames if header
            }
            required = {"account", "type", "amount"}
            missing = required - set(normalized_headers)
            if missing:
                raise ValueError(
                    "Missing required CSV column(s): " + ", ".join(sorted(missing))
                )

            with open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
                 open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
                 open("error.csv", "w", newline="", encoding="utf-8") as error_file:

                credit_writer = csv.DictWriter(credit_file, fieldnames=FIELDS)
                debit_writer = csv.DictWriter(debit_file, fieldnames=FIELDS)
                error_writer = csv.writer(error_file)

                credit_writer.writeheader()
                debit_writer.writeheader()
                error_writer.writerow(
                    ["row_number", "account", "type", "amount", "reason"]
                )

                for row_number, row in enumerate(reader, start=2):
                    raw_account = row.get(normalized_headers["account"], "")
                    raw_type = row.get(normalized_headers["type"], "")
                    raw_amount = row.get(normalized_headers["amount"], "")

                    try:
                        # A row with too many CSV values is malformed.
                        if None in row:
                            raise ValueError("Too many columns in row")

                        account = (raw_account or "").strip()
                        transaction_type = (raw_type or "").strip().lower()
                        amount_text = (raw_amount or "").strip()

                        if not account:
                            raise ValueError("Missing account")
                        if transaction_type not in ("credit", "debit"):
                            raise ValueError("Type must be credit or debit")
                        if not amount_text:
                            raise ValueError("Missing amount")

                        amount = float(amount_text)
                        if amount <= 0:
                            raise ValueError("Amount must be greater than zero")

                        valid_record = {
                            "account": account,
                            "type": transaction_type,
                            "amount": amount,
                        }

                        if transaction_type == "credit":
                            credit_writer.writerow(valid_record)
                            credit_totals[account] += amount
                        else:
                            debit_writer.writerow(valid_record)
                            debit_totals[account] += amount

                    except (ValueError, TypeError, KeyError) as error:
                        reason = str(error) or "Invalid row"
                        error_writer.writerow(
                            [row_number, raw_account, raw_type, raw_amount, reason]
                        )

    except FileNotFoundError:
        print(
            "ERROR: transactions.csv was not found.\n"
            "Put transactions.csv in the same folder as this Python file, then run again."
        )
        return
    except (OSError, csv.Error, ValueError) as error:
        print("ERROR:", error)
        return

    all_accounts = set(credit_totals) | set(debit_totals)
    balances = [
        (account, credit_totals[account] - debit_totals[account])
        for account in all_accounts
    ]
    balances.sort(key=lambda item: (-abs(item[1]), item[0]))

    print("Processing complete.")
    print("Created: credit.csv, debit.csv, error.csv")
    print("\nAccount-wise Net Balance Change (largest absolute change first):")
    if not balances:
        print("No valid transactions found.")
    else:
        for account, net_change in balances:
            print(f"{account}: {net_change:.2f}")


if __name__ == "__main__":
    main()
