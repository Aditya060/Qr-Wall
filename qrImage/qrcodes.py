import os
from PIL import Image
import qrcode
from psd_tools import PSDImage  # New import for PSD support

# Paths for image and output
IMAGE_PATH = 'static/images/Final_Image.psd'  # PSD file path
SEGMENT_DIR = 'static/images/segments'
QR_CODE_DIR = 'static/images/qr_codes'

ROWS, COLS = 6, 4  # 6 rows and 4 columns for 24 segments
SEGMENT_SIZE = 1000  # Each segment will be 1000x1000 pixels

def segment_image():
    """Split the PSD image into square segments and generate QR codes."""
    # Load the PSD file
    psd = PSDImage.open(IMAGE_PATH)
    
    # Convert PSD to a PIL image object
    img = psd.composite()  # Merge all layers and get the final rendered image
    img = img.convert('RGB')  # Ensure it's in RGB mode

    width, height = img.size
    print(f"Image size: {width}x{height}")

    # Ensure output directories exist
    os.makedirs(SEGMENT_DIR, exist_ok=True)
    os.makedirs(QR_CODE_DIR, exist_ok=True)

    # Counter for segment naming
    segment_counter = 1

    # Generate segments
    for row in range(ROWS):
        for col in range(COLS):
            # Define box coordinates for the segment
            left = col * SEGMENT_SIZE
            top = row * SEGMENT_SIZE
            right = left + SEGMENT_SIZE
            bottom = top + SEGMENT_SIZE

            # Crop and save the segment
            segment = img.crop((left, top, right, bottom))
            segment_name = f'segment_{segment_counter}.jpg'
            segment.save(os.path.join(SEGMENT_DIR, segment_name))

            # Generate corresponding QR code for each segment
            generate_qr_code(segment_counter, SEGMENT_SIZE, SEGMENT_SIZE)

            segment_counter += 1

    print("Cropped images saved successfully.")
    
    # Generate QR code for the full image
    generate_full_image_qr_code()

def generate_qr_code(segment_number, width, height):
    """Generate QR code for each image segment."""
    qr_url = f'http://127.0.0.1:8000/reveal/segment_{segment_number}/'

    # Create QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,  # Set box size to 1 pixel for better control over the final size
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    # Create an image for the QR code
    qr_img = qr.make_image(fill='black', back_color='white')

    # Resize QR code to match segment size
    qr_img = qr_img.resize((width, height), Image.LANCZOS)

    # Save the QR code
    qr_img_name = f'qr_code_segment_{segment_number}.png'
    qr_img.save(os.path.join(QR_CODE_DIR, qr_img_name))

def generate_full_image_qr_code():
    """Generate a QR code for the full image."""
    full_image_url = 'http://127.0.0.1:8000/reveal/segment_0'

    # Create QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=4,
    )
    qr.add_data(full_image_url)
    qr.make(fit=True)

    # Create an image for the QR code
    qr_img = qr.make_image(fill='black', back_color='white')

    # Resize QR code to 450x450 pixels
    qr_img = qr_img.resize((450, 450), Image.LANCZOS)

    # Save the QR code
    qr_img_name = 'qr_code_segment_0.png'
    qr_img.save(os.path.join(QR_CODE_DIR, qr_img_name))

if __name__ == '__main__':
    segment_image()
