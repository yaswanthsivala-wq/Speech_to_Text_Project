console.log("Voice agent final version loaded");

let mediaRecorder;
let audioChunks = [];
let isActive = false;

// 🎤 START
async function startRecording() {
    isActive = true;
    loop();
}

// 🔁 LOOP (runs only once effectively)
async function loop() {
    if (!isActive) return;

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
        document.getElementById("statusText").innerText = "🎤 Listening...";
        document.getElementById("pulseRing").classList.add("recording");

        // ⏱️ Record for 3 sec
        setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state !== "inactive") {
                mediaRecorder.stop();
            }
        }, 3000);

        mediaRecorder.onstop = async () => {
            try {
                const blob = new Blob(audioChunks, { type: 'audio/webm' });

                const formData = new FormData();
                formData.append("audio", blob, "recording.webm");

                const response = await fetch("/transcribe", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();

                // 📝 Show transcript + STOP LOOP
                if (data.transcript && data.transcript.length > 3 &&
                    data.transcript !== "⚠️ Could not recognize speech") {

                    document.getElementById("transcriptText").innerText = data.transcript;
                    document.getElementById("transcriptBox").style.display = "block";

                    document.getElementById("aiText").innerText = data.ai_response;
                    document.getElementById("aiBox").style.display = "block";

                    // 🔥 STOP AFTER SUCCESS
                    console.log("✅ Got response → stopping");

                    isActive = false;

                    document.getElementById("recordBtn").style.display = "inline-block";
                    document.getElementById("stopBtn").style.display = "none";
                    document.getElementById("statusText").innerText = "✅ Done. Click Start again";
                    document.getElementById("pulseRing").classList.remove("recording");

                    return; // ❗ STOP EVERYTHING
                }

                // ❌ DO NOT LOOP AGAIN (important)

            } catch (err) {
                console.error("Error:", err);
                isActive = false;
            }
        };

    } catch (err) {
        console.error("Mic error:", err);
        document.getElementById("statusText").innerText = "❌ Mic error";
    }
}

// ⏹ STOP BUTTON
function stopRecording() {
    isActive = false;

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }

    document.getElementById("recordBtn").style.display = "inline-block";
    document.getElementById("stopBtn").style.display = "none";
    document.getElementById("statusText").innerText = "⏹ Stopped";
    document.getElementById("pulseRing").classList.remove("recording");

    console.log("🛑 Stopped manually");
}