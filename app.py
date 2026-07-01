import base64
from pathlib import Path
from html import escape

import streamlit as st
import streamlit.components.v1 as components


APP_TITLE = "RTİB E-Mail İmza Oluşturucu"
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_LOGO_PATH = BASE_DIR / "assets" / "rtib_logo.png"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✉️",
    layout="centered",
)


def load_css() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {
            max-width: 980px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .small-note {
            font-size: 13px;
            color: #666;
            line-height: 1.45;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def file_to_data_uri(file_bytes: bytes, mime: str = "image/png") -> str:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def default_logo_data_uri() -> str:
    """
    Default RTIB logosunu her durumda otomatik yükler.
    Yeni logo yüklenmese bile ön izleme ve indirme görünür.
    """
    if DEFAULT_LOGO_PATH.exists():
        return file_to_data_uri(DEFAULT_LOGO_PATH.read_bytes(), "image/png")
    return ""


def normalize_website(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    value = value.replace("https://", "").replace("http://", "").strip("/")
    return value


def normalize_tel_href(value: str) -> str:
    allowed = "+0123456789"
    return "".join(ch for ch in value if ch in allowed)


def build_signature(
    name: str,
    title: str,
    mobile: str,
    corporate_phone: str,
    email: str,
    website: str,
    address: str,
    logo_src: str,
    company_line_tr: str,
    company_line_ru: str,
    include_greetings: bool,
) -> str:
    name = escape(name.strip())
    title = escape(title.strip())
    mobile = escape(mobile.strip())
    corporate_phone = escape(corporate_phone.strip())
    email = escape(email.strip())
    website_clean = escape(normalize_website(website))
    address = escape(address.strip())
    company_line_tr = escape(company_line_tr.strip())
    company_line_ru = escape(company_line_ru.strip())

    greetings = ""
    if include_greetings:
        greetings = """
        <tr>
          <td style="padding:0 0 12px 0; font-size:14px; line-height:20px; color:#333333;">
            <div>Saygılarımla,</div>
            <div style="height:6px; line-height:6px;">&nbsp;</div>
            <div>С уважением,</div>
          </td>
        </tr>
        """

    title_html = ""
    if title:
        title_html = f'<div style="font-size:13px; line-height:19px; color:#555555; padding-top:3px;">{title}</div>'

    logo_html = ""
    if logo_src:
        logo_html = f"""
        <img src="{logo_src}" alt="RTİB" width="180" style="display:block; width:180px; max-width:180px; height:auto; border:0; outline:none; text-decoration:none;">
        """
    else:
        logo_html = """
        <div style="font-size:36px; line-height:38px; font-weight:bold; color:#e52b2f; letter-spacing:.5px;">RTİB</div>
        <div style="font-size:10px; line-height:12px; color:#0079b8;">Ассоциация российских и турецких предпринимателей</div>
        """

    website_html = ""
    if website_clean:
        website_html = f"""
        <span style="white-space:nowrap;">
          <span style="display:inline-block; background:#0079b8; color:#ffffff; font-size:11px; font-weight:bold; width:20px; height:20px; line-height:20px; text-align:center; border-radius:2px; margin-right:6px;">W</span>
          <a href="https://{website_clean}" style="color:#444444; text-decoration:none;">{website_clean}</a>
        </span>
        """

    email_html = ""
    if email:
        email_html = f"""
        <span style="white-space:nowrap; margin-right:18px;">
          <span style="display:inline-block; background:#0079b8; color:#ffffff; font-size:11px; font-weight:bold; width:20px; height:20px; line-height:20px; text-align:center; border-radius:2px; margin-right:6px;">E</span>
          <a href="mailto:{email}" style="color:#444444; text-decoration:none;">{email}</a>
        </span>
        """

    mobile_html = ""
    if mobile:
        mobile_html = f"""
        <div style="font-size:14px; line-height:20px; color:#222222; padding-top:8px;">
          <a href="tel:{normalize_tel_href(mobile)}" style="color:#222222; text-decoration:none;">{mobile}</a>
        </div>
        """

    signature = f"""
<table cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:640px; font-family:Arial, Helvetica, sans-serif; color:#222222; border-collapse:collapse;">
  {greetings}
  <tr>
    <td style="padding:0;">
      <table cellpadding="0" cellspacing="0" border="0" style="width:100%; border-collapse:collapse; border-top:3px solid #e52b2f;">
        <tr>
          <td style="padding:15px 18px 12px 0; width:190px; vertical-align:top;">
            {logo_html}
          </td>

          <td style="width:1px; background:#d7d7d7; font-size:0; line-height:0;">&nbsp;</td>

          <td style="padding:14px 0 12px 18px; vertical-align:top;">
            <div style="font-size:18px; line-height:22px; font-weight:bold; color:#222222; letter-spacing:.2px;">{name}</div>
            {title_html}
            <div style="font-size:13px; line-height:19px; color:#555555;">{company_line_tr}</div>
            <div style="font-size:13px; line-height:19px; color:#555555;">{company_line_ru}</div>
            {mobile_html}
          </td>
        </tr>
      </table>

      <table cellpadding="0" cellspacing="0" border="0" style="width:100%; border-collapse:collapse; border-top:1px solid #d7d7d7;">
        <tr>
          <td style="padding:10px 0 0 0; font-size:12px; line-height:18px; color:#444444;">
            <span style="display:inline-block; background:#2b2b2b; color:#ffffff; font-size:11px; font-weight:bold; width:20px; height:20px; line-height:20px; text-align:center; border-radius:2px; margin-right:6px;">A</span>
            <span>{address}</span>
          </td>
        </tr>

        <tr>
          <td style="padding:7px 0 0 0; font-size:12px; line-height:20px; color:#444444;">
            <span style="white-space:nowrap; margin-right:18px;">
              <span style="display:inline-block; background:#e52b2f; color:#ffffff; font-size:11px; font-weight:bold; width:20px; height:20px; line-height:20px; text-align:center; border-radius:2px; margin-right:6px;">T</span>
              <a href="tel:{normalize_tel_href(corporate_phone)}" style="color:#444444; text-decoration:none;">{corporate_phone}</a>
            </span>
            {email_html}
            {website_html}
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""
    return signature


def wrap_full_html(signature_html: str) -> str:
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>RTİB E-Mail Signature</title>
</head>
<body style="margin:0; padding:20px;">
{signature_html}
</body>
</html>
"""


def main() -> None:
    load_css()

    st.title(APP_TITLE)
    st.caption("Outlook, Yandex Webmail, Gmail ve diğer e-posta istemcileri için HTML imza üretir.")

    with st.sidebar:
        st.header("Ayarlar")

        password_enabled = st.secrets.get("PASSWORD", "") != ""
        if password_enabled:
            password = st.text_input("Giriş şifresi", type="password")
            if password != st.secrets["PASSWORD"]:
                st.warning("Devam etmek için şifre giriniz.")
                st.stop()

        st.info("Yeni logo yüklenmese bile sistem varsayılan RTİB logosu ile ön izleme ve indirme üretir.")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Ad Soyad", "Mustafa VATAN")
        title = st.text_input("Unvan / Görev", "Yönetim Kurulu Üyesi")
        mobile = st.text_input("Mobil Telefon", "+7 909 154 15 98")
        corporate_phone = st.text_input("Kurum Telefonu", "+8 (495) 514-13-74")

    with col2:
        email = st.text_input("E-posta", "info@rtib.org")
        website = st.text_input("Web Sitesi", "www.rtib.org")
        address = st.text_input(
            "Adres",
            "115184, г. Москва, Большой Овчинниковский пер. 16, офис 515",
        )
        include_greetings = st.checkbox("Saygılarımla / С уважением satırını ekle", value=True)

    uploaded_logo = None
    with st.expander("Kurumsal metinler ve logo", expanded=False):
        company_line_tr = st.text_input("Kurum satırı TR", "RTİB")
        company_line_ru = st.text_input(
            "Kurum satırı RU",
            "Ассоциация российских и турецких предпринимателей",
        )

        st.markdown("Varsayılan olarak `assets/rtib_logo.png` kullanılır.")
        use_uploaded_logo = st.checkbox("Farklı logo yükle", value=False)

        if use_uploaded_logo:
            uploaded_logo = st.file_uploader("Logo yükleyin", type=["png", "jpg", "jpeg", "webp"])
    # Önce her zaman varsayılan logo yüklenir.
    # Kullanıcı farklı logo yüklerse onunla değiştirilir.
    logo_src = default_logo_data_uri()

    if uploaded_logo is not None:
        mime = uploaded_logo.type or "image/png"
        logo_src = file_to_data_uri(uploaded_logo.read(), mime)

    if use_uploaded_logo and uploaded_logo is None:
        st.warning("Farklı logo seçildi ama dosya yüklenmedi. Şimdilik varsayılan RTİB logosu kullanılıyor.")

    signature_html = build_signature(
        name=name,
        title=title,
        mobile=mobile,
        corporate_phone=corporate_phone,
        email=email,
        website=website,
        address=address,
        logo_src=logo_src,
        company_line_tr=company_line_tr,
        company_line_ru=company_line_ru,
        include_greetings=include_greetings,
    )

    full_html = wrap_full_html(signature_html)

    st.divider()
    st.subheader("Ön İzleme")
    components.html(full_html, height=350, scrolling=True)

    st.subheader("HTML Çıktısı")
    st.code(full_html, language="html")

    safe_name = "_".join(name.strip().split()) or "rtib"

    col_download_1, col_download_2 = st.columns(2)

    with col_download_1:
        st.download_button(
            "HTML imzayı indir",
            data=full_html.encode("utf-8"),
            file_name=f"rtib_email_signature_{safe_name}.html",
            mime="text/html",
            use_container_width=True,
        )

    with col_download_2:
        st.download_button(
            "Sadece imza bloğunu indir",
            data=signature_html.encode("utf-8"),
            file_name=f"rtib_signature_block_{safe_name}.html",
            mime="text/html",
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="small-note">
        <b>Kullanım:</b> HTML dosyasını tarayıcıda açın, imza alanını seçip kopyalayın.
        Sonra Outlook veya Yandex Webmail imza ayarlarına yapıştırın.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
