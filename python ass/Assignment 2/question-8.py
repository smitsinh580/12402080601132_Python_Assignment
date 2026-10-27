
MOD = 10**9 + 7

n, m = map(int, input("Enter rows and columns: ").split())

print("Enter grid (X for blocked cells):")
grid = [input().split() for _ in range(n)]

dp = [[None] * m for _ in range(n)]
ways = [[0] * m for _ in range(n)]

if grid[0][0] != "X":
    dp[0][0] = int(grid[0][0])
    ways[0][0] = 1

for i in range(n):
    for j in range(m):
        if grid[i][j] == "X" or (i == 0 and j == 0):
            continue

        value = int(grid[i][j])
        best = None
        count = 0

        # From left
        if j > 0 and dp[i][j - 1] is not None:
            best = dp[i][j - 1]
            count = ways[i][j - 1]

        # From top
        if i > 0 and dp[i - 1][j] is not None:
            score = dp[i - 1][j]
            if best is None or score > best:
                best = score
                count = ways[i - 1][j]
            elif score == best:
                count = (count + ways[i - 1][j]) % MOD

        # From diagonal
        if i > 0 and j > 0 and dp[i - 1][j - 1] is not None:
            score = dp[i - 1][j - 1]
            if best is None or score > best:
                best = score
                count = ways[i - 1][j - 1]
            elif score == best:
                count = (count + ways[i - 1][j - 1]) % MOD

        if best is not None:
            dp[i][j] = best + value
            ways[i][j] = count

# Print result
if dp[n - 1][m - 1] is None:
    print("IMPOSSIBLE")
else:
    print("Maximum Score:", dp[n - 1][m - 1])
    print("Number of Ways:", ways[n - 1][m - 1])
