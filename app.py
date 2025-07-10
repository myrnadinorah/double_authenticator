import streamlit as st
import pyotp

st.title("Secure Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "secret":
        st.success("Password correct. Now enter your 2FA code.")
        
        secret = "JBSWY3DPEHPK3PXP"  
        totp = pyotp.TOTP(secret)
        st.info("Open Google Authenticator and enter the current code")

        otp = st.text_input("Enter the 6-digit code from Google Authenticator")

        if st.button("Verify 2FA"):
            if totp.verify(otp):
                st.success("Login successful! 🎉")
            else:
                st.error("Invalid 2FA code ❌")
    else:
        st.error("Invalid credentials")
        
st.write(f"Setup this QR in Google Authenticator:")
st.image(pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="StreamlitApp"))
