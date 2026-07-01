# RTİB E-Mail İmza Oluşturucu v2

Bu sürümde düzeltildi:

- Yeni logo yüklenmese bile varsayılan RTİB logosu otomatik gelir.
- Ön izleme her durumda görünür.
- İndirme butonları her durumda görünür.
- Logo yolu artık dosyanın bulunduğu klasöre göre çalışır: `Path(__file__).resolve().parent`.
- `streamlit.components.v1` doğrudan import edildi.

## Çalıştırma

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub / Streamlit Cloud

Repository'ye şu dosyaları yükleyin:

```text
app.py
requirements.txt
README.md
.gitignore
.streamlit/config.toml
.streamlit/secrets.example.toml
assets/rtib_logo.png
```

Streamlit Cloud'da main file path:

```text
app.py
```

## Şifre koruması

Secrets bölümüne ekleyin:

```toml
PASSWORD = "rtib-guclu-sifre"
```

Şifre istemiyorsanız secrets içine PASSWORD eklemeyin.

## Kullanım

1. Kullanıcı bilgilerini girin.
2. Kurumsal metinler ve logo bölümünü değiştirmek zorunda değilsiniz.
3. Ön izleme otomatik görünür.
4. HTML imzayı indirin.
5. HTML dosyasını tarayıcıda açıp imza alanını kopyalayın.
6. Outlook veya Yandex Webmail imza alanına yapıştırın.
