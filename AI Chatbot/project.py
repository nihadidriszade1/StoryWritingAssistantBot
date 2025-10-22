import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from dotenv import load_dotenv


load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyasına ekleyin.")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API anahtarı yapılandırmasında hata: {e}")
    st.info("Lütfen Google AI Studio veya Google Cloud Console'dan geçerli bir API anahtarı alın ve .env dosyasına 'GOOGLE_API_KEY=your-api-key' şeklinde ekleyin.")
    st.stop()


def generate_story(prompt):
    model_name = 'gemini-2.5-flash'  
    try:
        model = genai.GenerativeModel(model_name)
        full_prompt = (
            "Sen, akıcı ve gerçekçi bir Türkçe hikaye yazarı AI'sın. "
            "Kullanıcının talebine göre yaratıcı, ayrıntılı ve doğal bir hikaye yaz. "
            f"Kullanıcı talebi: {prompt}\n"
            "Hikaye, Türkçe dilinde, akıcı, sürükleyici ve gerçekçi olmalı. En az 200 kelime yaz."
        )
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Hikaye üretilirken hata oluştu: {e}")
        return "Hikaye üretilemedi. Lütfen tekrar deneyin veya API anahtarını kontrol edin."


def save_to_pdf(story):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont("Helvetica", 12)
        text = c.beginText(40, 800)
        for line in story.split("\n"):
            text.textLine(line)
        c.drawText(text)
        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"PDF oluşturulurken hata oluştu: {e}")
        return None


def main():
    st.title("Hikaye Yazarı Chatbot")
    st.write("İstediğiniz hikayeyi tarif edin, size akıcı ve gerçekçi bir hikaye yazayım!")

    
    user_input = st.text_area(
        "Hikaye talebinizi yazın (örneğin, 'Korku hikayesi, karanlık bir ormanda geçen, ana karakter bir dedektif'):",
        height=100
    )

    if st.button("Hikaye Oluştur"):
        if not user_input.strip():
            st.error("Lütfen bir hikaye talebi girin!")
            return
        
       
        with st.spinner("Hikaye yazılıyor..."):
            story = generate_story(user_input)
        
     
        st.write("### Oluşturulan Hikaye")
        st.write(story)
        
       
        pdf_buffer = save_to_pdf(story)
        if pdf_buffer:
            st.download_button(
                label="Hikayeyi PDF olarak indir",
                data=pdf_buffer,
                file_name="hikaye.pdf",
                mime="application/pdf"
            )
        else:
            st.error("PDF indirme işlemi başarısız oldu.")

if __name__ == "__main__":
    main()