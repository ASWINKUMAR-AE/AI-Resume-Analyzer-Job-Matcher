import os
import uuid
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """
    Validates if file extension is in allowed set (pdf, docx, txt).
    """
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file_obj, student_id):
    """
    Safely saves uploaded resume to local disk with unique filename.
    Returns (saved_filename, full_file_path, file_type).
    """
    if not file_obj or not file_obj.filename:
        raise ValueError("No file uploaded or filename is empty.")

    original_filename = secure_filename(file_obj.filename)
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'txt'
    
    if ext not in Config.ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file extension: .{ext}. Allowed extensions: {', '.join(Config.ALLOWED_EXTENSIONS)}")

    # Unique sanitized filename: student_{id}_{uuid}_{filename}
    unique_token = uuid.uuid4().hex[:8]
    safe_filename = f"student_{student_id}_{unique_token}_{original_filename}"
    file_path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)

    file_obj.save(file_path)
    return original_filename, file_path, ext
