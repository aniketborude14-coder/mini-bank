purchases = 0
discount = 0
total = 0
count = 0

items = {"sadi": 500, "shirt": 1000, "shoes": 1500, "hat": 700, "socks": 300}

for item, price in items.items():
    print(f"{item}: {price}")

selected = input(f"\nEnter the items you want to purchase {list(items.keys())}: ").split(",")

for item in selected:
    item = item.strip()
    if item in items:
        purchases += items[item]
        count += 1

print(f"\nTotal items purchased: {count}")

if purchases > 3000:
    discount = purchases * 0.1
    total = purchases - discount
    print(f"\nDiscount: {discount}")
    print(f"\nTotal: {total}")
else:
    total = purchases
    print(f"\nTotal: {total}")
    print("\nAdd more items to avail discount.")

