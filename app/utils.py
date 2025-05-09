import qrcode
import re
from io import BytesIO
import base64

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def generate_qr_base64(url: str) -> str:
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{qr_base64}"

def none_to_na(obj):
    return "N/A" if obj is None else obj

def apply_none_to_na(data):
    if isinstance(data, dict):
        return {k: apply_none_to_na(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [apply_none_to_na(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(apply_none_to_na(item) for item in data)
    else:
        return none_to_na(data)

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))