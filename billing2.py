import cv2
import requests
from pyzbar import pyzbar
import json

# Backend URL
backend_url = "http://172.20.10.10:3000/add-item"  # Replace with your backend URL
delete_url = "http://172.20.10.10:3000/delete-item"  # Endpoint for deleting products

# Predefined products with their details
products = {
    "colors": {
        "name": "Colors",
        "price": 120,
        "weight": 150
    },
    "sauce": {
        "name": "Sauce",
        "price": 35,
        "weight": 28
    },
    "lays": {
        "name": "Lays",
        "price": 40,
        "weight": 55
    }
}

# Set to track scanned products
scanned_products = set()

def send_product_data(product):
    """Send product data to the backend."""
    try:
        if product['name'] in scanned_products:
            print(f"Product already scanned: {product['name']}")
            return  # Product already scanned
        response = requests.post(backend_url, json=product)
        response.raise_for_status()
        print(f"Sent to backend: {product}")
        print(f"Backend response: {response.json()}")
        scanned_products.add(product['name'])  # Add product to scanned set
    except Exception as e:
        print(f"Error sending product data to backend: {e}")

def decode_qr(frame):
    """Detect and decode QR codes in the frame."""
    qr_codes = pyzbar.decode(frame)
    for qr in qr_codes:
        qr_data = qr.data.decode('utf-8')
        try:
            data = json.loads(qr_data)
            product_key = data['name'].lower()
            if product_key in products:
                product_info = products[product_key]
                print(f"Detected product: {product_info['name']}")
                send_product_data(product_info)
            else:
                print(f"Unknown product: {data['name']}")
        except json.JSONDecodeError:
            print("Invalid QR code format.")
        except KeyError:
            print("QR code missing required fields.")

def main():
    # Initialize webcam (0 for default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Set the camera frame size to a smaller size (640x480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Starting video capture. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Decode QR codes in the frame
        decode_qr(frame)

        # Display the frame
        cv2.imshow('Billing2 - QR Code Scanner', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
