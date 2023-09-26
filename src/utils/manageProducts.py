import csv

def load_products():
    with open(r"products.csv", newline="") as f:
        reader = csv.reader(f)
        return [item[0] for item in list(reader)]