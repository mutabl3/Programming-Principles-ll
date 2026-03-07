import re
import json

file_path = '/Users/amirbakiev/Desktop/PP2/Practice5/raw.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

prices = re.findall(r'Стоимость\s*(\d{1,3}(?: \d{3})*,\d{2})', text)
prices = [float(p.replace(' ', '').replace(',', '.')) for p in prices]
print("Prices", prices)

products = re.findall(r'^\d+\.\s*(.+?)\s+\d+,\d+\s*x', text, re.MULTILINE)
print(f"\nProducts names:")
for i, product in enumerate(products, 1):
    print(f"{i}. {product.strip()}")

total_match = re.search(r'ИТОГО:\s*(\d{1,3}(?: \d{3})*,\d{2})', text)
total = float(total_match.group(1).replace(' ', '').replace(',', '.'))
print(f"\nTotal amount: {total:,.2f}".replace(',', ' '))

datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)
if datetime_match:
    print(f"\nDate: {datetime_match.group(1)}")
    print(f"Time: {datetime_match.group(2)}")

payment = re.search(r'(Банковская карта|Наличные)', text)
print(f"Payment method: {payment.group(1)}")

with open('receipt_output.json', 'w', encoding='utf-8') as f:
    json.dump(text, f, ensure_ascii=False, indent=4)