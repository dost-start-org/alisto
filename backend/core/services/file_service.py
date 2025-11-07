"""
File Service for handling image uploads to Cloudinary
"""
import base64
import io
import uuid
from PIL import Image
import cloudinary
import cloudinary.uploader
from django.conf import settings


class FileService:
    """Service for handling file operations including base64 to file conversion and Cloudinary uploads"""
    
    @staticmethod
    def initialize_cloudinary():
        """Initialize Cloudinary configuration from Django settings"""
        if not hasattr(settings, 'CLOUDINARY_CONFIG'):
            return False
        
        config = settings.CLOUDINARY_CONFIG
        cloudinary.config(
            cloud_name=config.get('CLOUD_NAME'),
            api_key=config.get('API_KEY'),
            api_secret=config.get('API_SECRET'),
            secure=True
        )
        return True
    
    @staticmethod
    def is_base64(data):
        """Check if the provided data is a base64 encoded string"""
        if not data or not isinstance(data, str):
            return False
        
        # Check if it's a data URL (e.g., data:image/png;base64,...)
        if data.startswith('data:'):
            return True
        
        # Check if it looks like base64 (basic check)
        try:
            if len(data) < 50:  # Too short to be an image
                return False
            # Try to decode a small portion to verify it's valid base64
            base64.b64decode(data[:100])
            return True
        except Exception:
            return False
    
    @staticmethod
    def is_url(data):
        """Check if the provided data is a URL"""
        if not data or not isinstance(data, str):
            return False
        return data.startswith(('http://', 'https://'))
    
    @staticmethod
    def extract_base64_data(base64_string):
        """
        Extract the actual base64 data from a data URL or plain base64 string
        Returns: (base64_data, image_format)
        """
        if base64_string.startswith('data:'):
            # Format: data:image/png;base64,iVBORw0KG...
            header, encoded = base64_string.split(',', 1)
            # Extract format from header (e.g., 'image/png' -> 'png')
            format_part = header.split(';')[0].split(':')[1]
            image_format = format_part.split('/')[1] if '/' in format_part else 'png'
            return encoded, image_format
        else:
            # Assume it's plain base64, default to png
            return base64_string, 'png'
    
    @staticmethod
    def validate_image(base64_data):
        """
        Validate that the base64 data represents a valid image
        Returns: (is_valid, error_message)
        """
        try:
            # Decode base64
            image_data = base64.b64decode(base64_data)
            
            # Check file size (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if len(image_data) > max_size:
                return False, "Image size exceeds 10MB limit"
            
            # Try to open as image
            image = Image.open(io.BytesIO(image_data))
            
            # Validate image format
            valid_formats = ['JPEG', 'PNG', 'GIF', 'WEBP', 'BMP']
            if image.format not in valid_formats:
                return False, f"Invalid image format. Supported formats: {', '.join(valid_formats)}"
            
            # Validate dimensions (optional, adjust as needed)
            max_dimension = 4096
            if image.width > max_dimension or image.height > max_dimension:
                return False, f"Image dimensions exceed {max_dimension}x{max_dimension} pixels"
            
            return True, None
            
        except base64.binascii.Error:
            return False, "Invalid base64 encoding"
        except Exception as e:
            return False, f"Invalid image data: {str(e)}"
    
    @staticmethod
    def upload_to_cloudinary(base64_string, folder='alisto'):
        """
        Upload a base64 encoded image to Cloudinary
        Returns: (success, url_or_error_message)
        """
        try:
            # Initialize Cloudinary
            if not FileService.initialize_cloudinary():
                return False, "Cloudinary not configured properly"
            
            # Extract base64 data
            base64_data, image_format = FileService.extract_base64_data(base64_string)
            
            # Validate image
            is_valid, error_msg = FileService.validate_image(base64_data)
            if not is_valid:
                return False, error_msg
            
            # Generate unique filename
            filename = f"{uuid.uuid4()}.{image_format}"
            
            # Prepare the data URL for Cloudinary
            if not base64_string.startswith('data:'):
                base64_string = f"data:image/{image_format};base64,{base64_data}"
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                base64_string,
                folder=folder,
                public_id=filename.split('.')[0],
                resource_type='image',
                overwrite=True,
                invalidate=True
            )
            
            # Return the secure URL
            return True, result.get('secure_url')
            
        except Exception as e:
            return False, f"Failed to upload image: {str(e)}"
    
    @staticmethod
    def process_image_field(image_data, folder='alisto'):
        """
        Process an image field that can be either a base64 string or URL
        If base64, uploads to Cloudinary and returns the URL
        If URL, returns it as-is
        Returns: (success, url_or_error_message)
        """
        if not image_data:
            return True, None
        
        # If it's already a URL, return it
        if FileService.is_url(image_data):
            return True, image_data
        
        # If it's base64, upload to Cloudinary
        if FileService.is_base64(image_data):
            return FileService.upload_to_cloudinary(image_data, folder)
        
        # Invalid format
        return False, "Image must be either a valid URL or base64 encoded string"
