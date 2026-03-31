from flask import Flask, request, jsonify
import webbrowser
from main import handle_text_command

app = Flask(__name__)


@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Jarvis</title>

<style>
body {
    margin: 0;
    background: #000;
    font-family: Arial;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* PARTICLE */
#particleCanvas {
    margin-top: 30px;
}

/* TITLE */
h2 {
    margin: 20px 0;
}

/* CHAT */
#chat {
    width: 60%;
    max-width: 700px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 60vh;
    overflow-y: auto;
    margin-bottom: 120px;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE 10+ */
}
#chat::-webkit-scrollbar {
    display: none; /* WebKit */
}

/* MESSAGE ROW */
.msg {
    display: flex;
    width: 100%;
}

/* USER RIGHT */
.user {
    justify-content: flex-end;
}

.user .bubble {
    background: #67e8f9;
    color: black;
}

/* AI LEFT */
.bot {
    justify-content: flex-start;
}

.bot .bubble {
    background: #1f2937;
}

/* BUBBLE */
.bubble {
    padding: 10px 14px;
    border-radius: 15px;
    max-width: 70%;
    font-size: 14px;
    line-height: 1.4;
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* INPUT */
#inputBox {
    background: #111;
    padding: 10px 20px;
    border-radius: 30px;
    display: flex;
    align-items: center;
    width: 60%;
    max-width: 700px;
    height: 50px;
    position: fixed;
    bottom: 40px;
}

/* DOTS */
#dots {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: none;
    gap: 10px;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #67e8f9;
    animation: bounce 1s infinite ease-in-out;
}

.dot:nth-child(1){animation-delay:0s;}
.dot:nth-child(2){animation-delay:0.15s;}
.dot:nth-child(3){animation-delay:0.3s;}
.dot:nth-child(4){animation-delay:0.45s;}

@keyframes bounce {
    0%,100%{transform:translateY(0);opacity:0.6;}
    50%{transform:translateY(-10px);opacity:1;}
}

/* INPUT */
input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 16px;
}

/* BUTTON */
button {
    background: none;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
}
</style>

</head>

<body>

<canvas id="particleCanvas"></canvas>
<h2>Jarvis</h2>

<div id="chat"></div>

<div id="inputBox">
    <div id="dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>

    <input id="input" placeholder="Ask something..."
        onkeydown="if(event.key==='Enter') sendMessage()" />

    <button onclick="toggleMic()">🎤</button>
</div>

<script>
/* ---------------- PARTICLE ---------------- */
const canvas = document.getElementById("particleCanvas");
const ctx = canvas.getContext("2d");

let listening = false;
let recognition = null;
let isRecognizing = false;
let isWaitingForResponse = false;
let voices = [];

function resize(size){
    canvas.width = size;
    canvas.height = size;
}
resize(150);

let particles = [];

for(let i=0;i<400;i++){
    particles.push({
        angle: Math.random()*Math.PI*2,
        baseRadius: Math.random()*60,
        speed: Math.random()*0.01+0.002
    });
}

function draw(){
    const cx = canvas.width/2;
    const cy = canvas.height/2;

    ctx.clearRect(0,0,canvas.width,canvas.height);

    let time = Date.now()*0.002;

    particles.forEach(p=>{
        p.angle += p.speed*(listening ? 2 : 1);

        let breathe = Math.sin(time) * 10;
        let r = p.baseRadius + breathe + (listening ? 15 : 0);

        let x = cx + Math.cos(p.angle) * r;
        let y = cy + Math.sin(p.angle) * r;

        ctx.fillStyle = "#67e8f9";
        ctx.fillRect(x, y, 2, 2);
    });
}

function animate(){
    draw();
    requestAnimationFrame(animate);
}
animate();

/* ---------------- VOICES ---------------- */
function loadVoices() {
    voices = window.speechSynthesis.getVoices();
}

loadVoices();
window.speechSynthesis.onvoiceschanged = loadVoices;

function getPreferredMaleVoice() {
    if (!voices || voices.length === 0) return null;

    const preferredNames = [
        "Google UK English Male",
        "Microsoft David",
        "Microsoft Mark",
        "Microsoft George",
        "Microsoft Guy",
        "Alex",
        "Daniel",
        "David",
        "Mark"
    ];

    for (const name of preferredNames) {
        const voice = voices.find(v => v.name.toLowerCase().includes(name.toLowerCase()));
        if (voice) return voice;
    }

    let maleHint = voices.find(v =>
        v.name.toLowerCase().includes("male") &&
        v.lang.toLowerCase().startsWith("en")
    );
    if (maleHint) return maleHint;

    let englishVoice = voices.find(v => v.lang.toLowerCase().startsWith("en"));
    if (englishVoice) return englishVoice;

    return voices[0];
}

function speakResponse(text) {
    if (!("speechSynthesis" in window)) {
        return;
    }

    window.speechSynthesis.cancel();
    isWaitingForResponse = true;

    const utterance = new SpeechSynthesisUtterance(text);
    const selectedVoice = getPreferredMaleVoice();

    if (selectedVoice) {
        utterance.voice = selectedVoice;
        utterance.lang = selectedVoice.lang;
    } else {
        utterance.lang = "en-IN";
    }

    utterance.rate = 0.95;
    utterance.pitch = 0.75;
    utterance.volume = 1;

    utterance.onend = function() {
        isWaitingForResponse = false;
    };

    utterance.onerror = function() {
        isWaitingForResponse = false;
    };

    window.speechSynthesis.speak(utterance);
}

/* ---------------- SPEECH RECOGNITION ---------------- */
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = function () {
        listening = true;
        isRecognizing = true;

        const dots = document.getElementById("dots");
        const input = document.getElementById("input");

        resize(300);
        dots.style.display = "flex";
        input.style.opacity = "0";
    };

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("input");

        input.value = transcript;
        sendMessage();
    };

    recognition.onerror = function (event) {
        console.log("Speech recognition error:", event.error);

        const chat = document.getElementById("chat");
        chat.innerHTML += `
            <div class="msg bot">
                <div class="bubble">Mic error: ${event.error}</div>
            </div>
        `;

        stopMicUI();
    };

    recognition.onend = function () {
        isRecognizing = false;
        stopMicUI();
    };
} else {
    console.log("Speech recognition not supported in this browser.");
}

function stopMicUI() {
    listening = false;

    const dots = document.getElementById("dots");
    const input = document.getElementById("input");

    resize(150);
    dots.style.display = "none";
    input.style.opacity = "1";
    input.placeholder = "Ask something...";
}

/* ---------------- MIC BUTTON ---------------- */
function toggleMic(){
    if (!recognition) {
        const chat = document.getElementById("chat");
        chat.innerHTML += `
            <div class="msg bot">
                <div class="bubble">Speech recognition is not supported in this browser.</div>
            </div>
        `;
        return;
    }

    if (isRecognizing) {
        recognition.stop();
        stopMicUI();
        return;
    }

    try {
        recognition.start();
    } catch (error) {
        console.log("Mic start error:", error);
    }
}

/* ---------------- CHAT + TYPING ---------------- */
async function sendMessage(){
    if (isWaitingForResponse) {
        alert("Please wait until the previous response has finished speaking.");
        return;
    }

    const input = document.getElementById("input");
    const chat = document.getElementById("chat");

    let text = input.value.trim();
    if(!text) return;

    chat.innerHTML += `
        <div class="msg user">
            <div class="bubble">${text}</div>
        </div>
    `;

    input.value = "";

    let botMsg = document.createElement("div");
    botMsg.className = "msg bot";
    botMsg.innerHTML = `<div class="bubble"></div>`;
    chat.appendChild(botMsg);

    let bubble = botMsg.querySelector(".bubble");

    try {
        let res = await fetch("/command", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({command: text})
        });

        let data = await res.json();
        let fullText = data.response || "No response from Jarvis.";

        speakResponse(fullText);

        let i = 0;
        function type(){
            if(i < fullText.length){
                bubble.innerHTML += fullText.charAt(i);
                i++;
                setTimeout(type, 15);
            }
        }
        type();

    } catch (error) {
        bubble.innerHTML = "Error connecting to backend.";
    }

    chat.scrollTop = chat.scrollHeight;
}
</script>

</body>
</html>
"""


@app.route("/command", methods=["POST"])
def command():
    try:
        data = request.get_json()
        cmd = data.get("command", "").strip()

        if not cmd:
            return jsonify({"response": "Please enter a command."})

        result = handle_text_command(cmd)
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)