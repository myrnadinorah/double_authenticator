import streamlit as st
import pyotp
import qrcode
from io import BytesIO

st.set_page_config(page_title="Secure Login", layout="centered")

# --- Static user data (for demo) ---
VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"
SECRET = "JBSWY3DPEHPK3PXP"  # You would store one per user in real apps

st.title("🔐 Secure Login with 2FA")

# --- Step 1: Login ---
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        st.session_state["authenticated"] = True
        st.success("✅ Password correct. Now enter your 2FA code from Google Authenticator.")
    else:
        st.session_state["authenticated"] = False
        st.error("❌ Invalid credentials")

# --- Step 2: Two-Factor Authentication ---
if st.session_state.get("authenticated"):
    totp = pyotp.TOTP(SECRET)

    # Generate and show QR code only on first login
    st.write("Scan this QR code in your Google Authenticator app:")
    uri = totp.provisioning_uri(name=username, issuer_name="StreamlitApp")
    qr = qrcode.make(uri)
    buf = BytesIO()
    qr.save(buf)
    st.image(buf.getvalue())

    otp_input = st.text_input("Enter the 6-digit code from your Authenticator")

    if st.button("Verify 2FA"):
        if totp.verify(otp_input):
            st.success("🎉 Login successful!")
        else:
            st.error("❌ Invalid 2FA code")
