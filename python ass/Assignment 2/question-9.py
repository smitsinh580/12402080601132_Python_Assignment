
class Product:
    def __init__(self, name, stock, purchase_price, selling_price):
        self.name = name
        self.stock = stock
        self.purchase_price = purchase_price
        self.selling_price = selling_price

    def __add__(self, other):
        return Product(
            self.name,
            self.stock + other.stock,
            min(self.purchase_price, other.purchase_price),
            max(self.selling_price, other.selling_price)
        )


class Inventory:
    def __init__(self):
        self.products = {}

    def add(self, product):
        if product.name in self.products:
            self.products[product.name] = (
                self.products[product.name] + product
            )
        else:
            self.products[product.name] = product

    def delete(self, name):
        if name in self.products:
            del self.products[name]
            print(name, "deleted")
        else:
            print("Product not found")

    def update(self, name, stock, purchase, selling):
        if name in self.products:
            p = self.products[name]
            p.stock = stock
            p.purchase_price = purchase
            p.selling_price = selling
        else:
            print("Product not found")

    def total_value(self):
        return sum(
            p.stock * p.purchase_price
            for p in self.products.values()
        )

    def __lt__(self, other):
        return self.total_value() < other.total_value()

    def __add__(self, other):
        result = Inventory()

        for p in self.products.values():
            result.add(Product(
                p.name, p.stock,
                p.purchase_price, p.selling_price
            ))

        for p in other.products.values():
            result.add(Product(
                p.name, p.stock,
                p.purchase_price, p.selling_price
            ))

        return result

    def display(self):
        for p in self.products.values():
            print(
                p.name, "| Stock:", p.stock,
                "| Purchase:", p.purchase_price,
                "| Selling:", p.selling_price
            )
        print("Total Inventory Value:", self.total_value())


# Main program
inv1 = Inventory()
inv2 = Inventory()

inv1.add(Product("Pen", 10, 5, 10))
inv1.add(Product("Book", 5, 30, 50))

inv2.add(Product("Pen", 20, 4, 12))
inv2.add(Product("Pencil", 15, 2, 5))

print("Inventory 1:")
inv1.display()

print("\nInventory 2:")
inv2.display()

print("\nIs Inventory 1 smaller?", inv1 < inv2)

print("\nMerged Inventory:")
merged = inv1 + inv2
merged.display()

print("\nAfter Updating Book:")
inv1.update("Book", 10, 25, 45)
inv1.display()

inv1.delete("Pen")
print("\nAfter Deletion:")
inv1.display()
