console.log("Voice agent FINAL full-record mode");

let mediaRecorder;
let audioChunks = [];

// 🎤 START RECORDING (FULL MODE)
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.start();

        // UI
        document.getElementById("recordBtn").style.display = "none";
        document.getElementById("stopBtn").style.display = "inline-block";
        document.getElementById("statusText").innerText = "🎤 Recording... Speak freely";
        document.getElementById("pulseRing").classList.add("recording");

    } catch (err) {
        console.error("Mic error:", err);
        document.getElementById("statusText").innerText = "❌ Mic access denied";
    }
}

// ⏹ STOP RECORDING (PROCESS FULL AUDIO)
function stopRecording() {
    if (!mediaRecorder) return;

    mediaRecorder.stop();

    document.getElementById("statusText").innerText = "⏳ Processing...";

    mediaRecorder.onstop = async () => {
        try {
            const blob = new Blob(audioChunks, { type: 'audio/webm' });

            const formData = new FormData();
            formData.append("audio", blob, "recording.webm");

            console.log("Sending full audio...");

            const response = await fetch("/transcribe", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            console.log("Response:", data);

            // 📝 FULL TRANSCRIPT
            document.getElementById("transcriptText").innerText = data.transcript;
            document.getElementById("transcriptBox").style.display = "block";

            // 🤖 AI RESPONSE
            document.getElementById("aiText").innerText = data.ai_response;
            document.getElementById("aiBox").style.display = "block";

            // 🔁 RESET UI
            document.getElementById("recordBtn").style.display = "inline-block";
            document.getElementById("stopBtn").style.display = "none";
            document.getElementById("statusText").innerText = "✅ Done. Click Start again";
            document.getElementById("pulseRing").classList.remove("recording");

        } catch (err) {
            console.error("Error:", err);
            document.getElementById("statusText").innerText = "❌ Error processing audio";

            document.getElementById("recordBtn").style.display = "inline-block";
            document.getElementById("stopBtn").style.display = "none";
        }
    };
}