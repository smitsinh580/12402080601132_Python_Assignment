
from html.parser import HTMLParser

class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []
        self.current = {}
        self.field = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "div" and attrs.get("class") == "product":
            self.current = {}

        elif tag == "h2" and self.current is not None:
            self.field = "name"

        elif tag == "span" and attrs.get("class") in ["price", "rating"]:
            self.field = attrs["class"]

    def handle_data(self, data):
        if self.field:
            self.current[self.field] = data.strip()

    def handle_endtag(self, tag):
        if tag in ["h2", "span"]:
            self.field = ""

        if tag == "div" and self.current:
            if all(k in self.current for k in ["name", "price", "rating"]):
                try:
                    self.products.append({
                        "name": self.current["name"],
                        "price": float(self.current["price"].replace("$", "")),
                        "rating": float(self.current["rating"])
                    })
                except ValueError:
                    pass
            self.current = {}


html = """
<div class="product">
<h2>Phone</h2>
<span class="price">$500</span>
<span class="rating">4.5</span>
</div>

<div class="product">
<h2>Laptop</h2>
<span class="price">$900</span>
<span class="rating">4.8</span>
</div>

<div class="product">
<h2>Phone</h2>
<span class="price">$450</span>
<span class="rating">4.5</span>
</div>
"""

parser = ProductParser()
parser.feed(html)

# Remove duplicates: higher rating wins, then lower price
unique = {}

for p in parser.products:
    name = p["name"]

    if (name not in unique or
        p["rating"] > unique[name]["rating"] or
        (p["rating"] == unique[name]["rating"] and
         p["price"] < unique[name]["price"])):
        unique[name] = p

products = sorted(
    unique.values(),
    key=lambda p: (-p["rating"], p["price"], p["name"])
)

k = int(input("Enter K: "))

print("\nTop Products:")
for p in products[:max(0, k)]:
    print(p["name"], "| Price:", p["price"],
          "| Rating:", p["rating"])
