import qrcode
from PIL import Image

# Function to generate a QR code
def generate_qr(data, filename):
    # Create a QRCode object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add data to the QR Code
    qr.add_data(data)
    qr.make(fit=True)

    # Create the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR Code saved as {filename}")

    # Example usage
if __name__ == "__main__":
    # Customize this data for your tote or cabinet
    print("Starting QR code generation...")
    data = "Tote 1: Christmas Decorations"
    filename = "tote1_qr.png"
    generate_qr(data, filename)
    print("QR code generation completed")