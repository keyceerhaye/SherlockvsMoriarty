import os
from PIL import Image
import glob

def compress_images(input_folder='game/images', output_folder='game/images/compressed', max_size_mb=0.2):
    """
    Compress all images in the input folder and save them to the output folder
    
    Args:
        input_folder (str): Path to folder containing images to compress
        output_folder (str): Path to save compressed images
        max_size_mb (float): Maximum target file size in megabytes
    """
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Supported image formats
    supported_formats = ['*.jpg', '*.jpeg', '*.png']
    
    # Get all image files
    image_files = []
    for format in supported_formats:
        image_files.extend(glob.glob(os.path.join(input_folder, format)))
        image_files.extend(glob.glob(os.path.join(input_folder, format.upper())))
    
    if not image_files:
        print(f"No images found in {input_folder}")
        return
        
    print(f"Found {len(image_files)} images to compress")
    
    for image_path in image_files:
        try:
            # Open image
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Get original dimensions
            width, height = img.size
            
            # Get original file size in MB
            file_size = os.path.getsize(image_path) / (1024 * 1024)
            
            # Get output path
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_folder, filename)
            
            # Start with resizing if image is very large
            if width > 1920 or height > 1080:
                # Calculate aspect ratio
                aspect_ratio = width / height
                if width > height:
                    new_width = 1920
                    new_height = int(1920 / aspect_ratio)
                else:
                    new_height = 1080
                    new_width = int(1080 * aspect_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Initial save with high quality
            quality = 85
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            current_size = os.path.getsize(output_path) / (1024 * 1024)
            
            # Gradually reduce quality until file size is under max_size_mb
            while current_size > max_size_mb and quality > 5:
                quality -= 5
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                current_size = os.path.getsize(output_path) / (1024 * 1024)
            
            # If still too large, try reducing dimensions
            if current_size > max_size_mb:
                while current_size > max_size_mb and width > 400 and height > 400:
                    width = int(width * 0.8)
                    height = int(height * 0.8)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                    current_size = os.path.getsize(output_path) / (1024 * 1024)
            
            print(f"Compressed {filename}: {file_size:.2f}MB -> {current_size:.2f}MB (Quality: {quality}%)")
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")

if __name__ == "__main__":
    # Example usage
    compress_images(
        input_folder='game/images',  # Path to your images folder
        output_folder='game/images/compressed',  # Where compressed images will be saved
        max_size_mb=0.2  # Maximum size in MB (200KB)
    )