import streamlit as st
import pyotp
import qrcode
from io import BytesIO

st.set_page_config(page_title="Secure Login", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #808080;
        }
        .logo {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

logo_url = "https://raw.githubusercontent.com/myrnadinorah/double_authenticator/main/logi.png"
st.markdown(f'<div class="logo"><img src="{logo_url}" width="600"></div>', unsafe_allow_html=True)

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"
SECRET = "JBSWY3DPEHPK3PXP"  # In production, generate/store one per user

#st.title("🔐 Secure Login with 2FA")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        st.session_state["authenticated"] = True
        st.success("✅ Password correct. Now enter your 2FA code from Google Authenticator.")
    else:
        st.session_state["authenticated"] = False
        st.error("❌ Invalid credentials")

if st.session_state.get("authenticated"):
    totp = pyotp.TOTP(SECRET)

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


