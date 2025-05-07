import streamlit as st
import qrcode
from PIL import Image
import io
from pyzbar.pyzbar import decode


st.title("QR Code Generator & Decoder")

tab1, tab2 = st.tabs(["Generate QR Code", "Decode QR Code"])


with tab1:
    st.subheader("Generate QR Code")
    data = st.text_input("Enter URL: ",)
    
    
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    
    def generate_qr_code(url):
        qr.clear()
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        return img
    
    if st.button("Generate QR Code"):
        if data:
            qr_image = generate_qr_code(data)
            buf = io.BytesIO()
            qr_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.image(byte_im, caption="Generated QR Code", use_container_width=True)
            st.download_button(
                label="Download QR Code",
                data=byte_im,
                file_name="qr_code.png",
                mime="image/png"
            )
        else:
            st.error("Please enter a URL to generate a QR code")
    
    st.write(f"Current URL: {data}")

with tab2:
    st.subheader("Decode QR Code")
    uploaded_file = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        
        st.image(img, caption="Uploaded QR Code", use_container_width=True)
        
        try:
            decoded_objects = decode(img)
            
            if decoded_objects:
                st.success("QR Code decoded successfully!")
                for obj in decoded_objects:
                    st.write("Data:", obj.data.decode('utf-8'))
                    st.write("Type:", obj.type)
            else:
                st.warning("No QR code found in the image")
        except Exception as e:
            st.error(f"Error decoding QR code: {str(e)}")



st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; font-size: 20px;">
        Made with ❤️ by Nihal Khan Ghouri
    </div>
    """,
    unsafe_allow_html=True
)

