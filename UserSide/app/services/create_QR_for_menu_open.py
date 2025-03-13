import qrcode

# Data to encode in the QR code
data = "http://3.93.76.24/api/1"

# Create a QR code object with specific settings
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code (1 is the smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in pixels
    border=4,  # Thickness of the border (minimum is 4)
)

# Add data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Save the image to a file
img.save("melodyqr.png")

print("QR Code saved as qrcode.png")
