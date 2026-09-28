from generators.streaming.stream_db import get_cells, get_subscriptions


cells = get_cells()
subs = get_subscriptions()

print("Cells:", len(cells))
print(cells[:5])

print("Subscriptions:", len(subs))
print(subs[:5])