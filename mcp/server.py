from flask import Flask, request, jsonify, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

state = {
    "stage": "Booting...",
    "urls_processed": 0,
    "issues_found": 0,
    "severities": {"High": 0, "Medium": 0, "Low": 0}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SEO Command Center - Live Dashboard</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; background: #1e1e1e; color: #fff; }
        .card { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .progress { width: 100%; background: #444; border-radius: 4px; overflow: hidden; margin-top: 10px; }
        .bar { height: 20px; background: #4caf50; width: 0%; transition: width 0.4s ease; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .stat { background: #3d3d3d; padding: 15px; border-radius: 6px; text-align: center; }
        .stat h3 { margin: 0 0 10px 0; font-size: 14px; color: #aaa; text-transform: uppercase; }
        .stat p { margin: 0; font-size: 28px; font-weight: bold; }
        .high { color: #ff5252; } .medium { color: #fb8c00; } .low { color: #4caf50; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body>
    <h1>🚀 SEO Command Center</h1>
    <div class="card">
        <h3>Current Stage: <span id="stage" style="color: #4caf50;">Booting...</span></h3>
        <div class="progress"><div class="bar" id="bar"></div></div>
    </div>
    <div class="grid">
        <div class="stat"><h3>URLs Processed</h3><p id="urls">0</p></div>
        <div class="stat"><h3>Total Issues</h3><p id="issues">0</p></div>
        <div class="stat">
            <h3>Severities</h3>
            <p style="font-size: 16px; margin-top: 8px;">
                <span class="high" id="high">0</span> High | 
                <span class="medium" id="medium">0</span> Med | 
                <span class="low" id="low">0</span> Low
            </p>
        </div>
    </div>
    <script>
        const socket = io();
        socket.on('state_update', function(data) {
            document.getElementById('stage').innerText = data.stage;
            document.getElementById('urls').innerText = data.urls_processed;
            document.getElementById('issues').innerText = data.issues_found;
            document.getElementById('high').innerText = data.severities.High;
            document.getElementById('medium').innerText = data.severities.Medium;
            document.getElementById('low').innerText = data.severities.Low;
            let pct = 0;
            const stageLower = data.stage.toLowerCase();
            if(stageLower.includes('ingest')) pct = 25;
            if(stageLower.includes('detect')) pct = 50;
            if(stageLower.includes('fix')) pct = 75;
            if(stageLower.includes('report') || stageLower.includes('complete')) pct = 100;
            document.getElementById('bar').style.width = pct + '%';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/update', methods=['POST'])
def update_state():
    global state
    data = request.json
    if not data: return jsonify({"error": "No payload"}), 400
    state.update(data)
    socketio.emit('state_update', state)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7700, allow_unsafe_werkzeug=True)
