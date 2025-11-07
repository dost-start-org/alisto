# Image Upload Configuration Guide

This document explains how to configure and use the base64 image upload feature with Cloudinary integration.

## Overview

The application now supports accepting base64-encoded images in addition to image URLs for the following fields:

- `image_url` in Emergency Reports
- `image_url` in Emergency Verifications
- `logo_url` in Agencies

When a base64 string is provided, the system automatically:

1. Validates the image (format, size, dimensions)
2. Uploads it to Cloudinary
3. Stores the Cloudinary URL in the database

## Configuration

### 1. Install Required Packages

The following packages have been added to `requirements.txt`:

```
cloudinary==1.41.0
Pillow==11.0.0
```

Install them with:

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Add the following environment variables to your `.env` file:

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

To get these credentials:

1. Sign up at [Cloudinary](https://cloudinary.com/)
2. Go to your Dashboard
3. Copy your Cloud Name, API Key, and API Secret

### 3. Run Migrations

Apply the database migrations:

```bash
python manage.py migrate
```

## Usage

### Accepting Base64 Images

All endpoints that previously accepted `image_url` or `logo_url` now accept:

1. **Base64 string with data URL prefix** (recommended):

```json
{
  "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

2. **Plain base64 string**:

```json
{
  "image_url": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

3. **Regular URL** (backward compatible):

```json
{
  "image_url": "https://example.com/image.png"
}
```

### Endpoints Updated

#### 1. Emergency Reports (`POST /api/emergencies/reports/`)

```json
{
  "emergency_type": "uuid-here",
  "longitude": 120.9842,
  "latitude": 14.5995,
  "details": "Emergency details here",
  "image_url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

#### 2. Emergency Verifications (`POST /api/emergencies/verifications/`)

```json
{
  "report": "report-uuid-here",
  "vote": true,
  "details": "Verification details",
  "image_url": "data:image/png;base64,iVBORw0KGg..."
}
```

#### 3. Agencies (`POST /api/agencies/`)

```json
{
  "name": "Agency Name",
  "logo_url": "data:image/png;base64,iVBORw0KGg...",
  "hotline_number": "123-456-7890",
  "latitude": 14.5995,
  "longitude": 120.9842
}
```

## Image Validation

The system validates images with the following constraints:

- **Max file size**: 10MB
- **Supported formats**: JPEG, PNG, GIF, WEBP, BMP
- **Max dimensions**: 4096 x 4096 pixels

If validation fails, you'll receive an error message indicating the issue.

## Cloudinary Folder Structure

Images are organized in Cloudinary by type:

- Emergency Reports: `alisto/emergency_reports/`
- Emergency Verifications: `alisto/emergency_verifications/`
- Agency Logos: `alisto/agency_logos/`

## Error Handling

Common errors and their meanings:

- `"Image size exceeds 10MB limit"` - The image file is too large
- `"Invalid image format"` - The image format is not supported
- `"Image dimensions exceed 4096x4096 pixels"` - The image is too large
- `"Invalid base64 encoding"` - The provided string is not valid base64
- `"Cloudinary not configured properly"` - Environment variables are missing or incorrect
- `"Image must be either a valid URL or base64 encoded string"` - Invalid input format

## Testing

### Test with Base64 String

You can convert an image to base64 using Python:

```python
import base64

with open('test_image.jpg', 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    data_url = f"data:image/jpeg;base64,{encoded_string}"
    print(data_url)
```

### Test with cURL

```bash
curl -X POST http://localhost:8000/api/emergencies/reports/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_type": "uuid-here",
    "longitude": 120.9842,
    "latitude": 14.5995,
    "details": "Test emergency report",
    "image_url": "data:image/png;base64,iVBORw0KGgoAAAA..."
  }'
```

## Troubleshooting

### Issue: "Cloudinary not configured properly"

**Solution**: Ensure all three environment variables are set:

- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

### Issue: "Failed to upload image"

**Possible causes**:

1. Invalid Cloudinary credentials
2. Network connectivity issues
3. Cloudinary quota exceeded

**Solution**: Check your Cloudinary dashboard for account status and usage.

### Issue: Images not displaying

**Solution**: Ensure the Cloudinary URL returned is publicly accessible. Check your Cloudinary security settings.

## Development Notes

### File Service Module

The image processing logic is centralized in `core/services/file_service.py`. Key methods:

- `process_image_field(image_data, folder)` - Main entry point for processing images
- `validate_image(base64_data)` - Validates image data
- `upload_to_cloudinary(base64_string, folder)` - Handles Cloudinary upload

### Serializers

Serializers automatically handle image processing in their `validate_image_url()` or `validate_logo_url()` methods. The validation happens before saving to the database.

## Security Considerations

1. **Image validation** prevents malicious file uploads
2. **Size limits** prevent denial-of-service attacks
3. **Format restrictions** ensure only safe image formats are accepted
4. **Cloudinary** handles image optimization and security

## Future Enhancements

Potential improvements:

- Add image resizing/optimization before upload
- Support for multiple images per report
- Image compression options
- Thumbnail generation
- Image moderation via Cloudinary add-ons
