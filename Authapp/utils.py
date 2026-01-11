import pyotp
import qrcode
import base64
from io import BytesIO

def generate_otp_secret():
    return pyotp.random_base32()

def get_totp(secret):
    return pyotp.TOTP(secret)

def generate_qr_code(username,secret):
    totp=pyotp.TOTP(secret)
    uri=totp.provisioning_uri(name=username,issuer_name="AuthGuard")
    qr=qrcode.make(uri)
    buffer=BytesIO()
    qr.save(buffer,format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

