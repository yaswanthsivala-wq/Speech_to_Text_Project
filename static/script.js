console.log("Script loaded");
let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.start();

    // 🔥 UI FIX
    document.getElementById("recordBtn").style.display = "none";
    document.getElementById("stopBtn").style.display = "inline-block";
    document.getElementById("statusText").innerText = "🔴 Recording...";
}

function stopRecording() {
    mediaRecorder.stop();

    // 🔥 UI FIX
    document.getElementById("stopBtn").style.display = "none";
    document.getElementById("statusText").innerText = "⏳ Processing...";

    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' });

        const formData = new FormData();
        formData.append("audio", blob, "recording.webm");

        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log("Response:", data); // 🔥 debug
        document.getElementById("transcriptText").innerText = data.transcript;
        document.getElementById("transcriptBox").style.display = "block";

        // 🔥 Reset UI
        document.getElementById("recordBtn").style.display = "inline-block";
        document.getElementById("statusText").innerText = "✅ Done. Record again.";
    };
}