from flask import Flask, request, jsonify
import time, threading

app = Flask(__name__)

# 最简单的指令队列：一个槽位 + 时间戳
cmd = {"type": "hello"}
cmd_time = 0
lock = threading.Lock()

@app.route("/push", methods=["POST"])
def push():
    """我发指令到这里"""
    global cmd, cmd_time
    data = request.get_json(force=True)
    with lock:
        cmd = data
        cmd_time = time.time()
    return jsonify({"ok": True, "got": data})

@app.route("/toy-next", methods=["GET"])
def toy_next():
    """bridge轮询这里取指令"""
    with lock:
        return jsonify(cmd)

@app.route("/", methods=["GET"])
def health():
    return "SX589A bridge online"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
