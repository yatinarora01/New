import qrcode
import json

# Define your products
products = [
    {
        "name": "Colors",
        "price": 120,
        "weight": 150
    },
    {
        "name": "Sauce",
        "price": 35,
        "weight": 28
    },
    {
        "name": "Lays",
        "price": 40,
        "weight": 55
    }
]

# Function to generate QR code
def generate_qr(data, filename):
    qr = qrcode.QRCode(
        version=1,  # size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(data))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR Code saved as {filename}")

# Generate QR codes for each product
for product in products:
    filename = f"{product['name'].lower()}_qr.png"
    generate_qr(product, filename)
