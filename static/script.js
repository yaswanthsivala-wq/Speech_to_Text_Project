let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // ✅ FIX: Do NOT force audio/wav here.
        // Let the browser use its native format (webm/ogg).
        // We will detect and convert it properly on the Python side.
        const options = {};
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
            options.mimeType = 'audio/webm;codecs=opus';
        } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
            options.mimeType = 'audio/ogg;codecs=opus';
        }
        // If neither is supported, let the browser decide (it will pick a valid one)

        mediaRecorder = new MediaRecorder(stream, options);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) audioChunks.push(event.data);
        };

        mediaRecorder.start(250); // Collect audio every 250ms

        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'inline-block';
        document.getElementById('statusText').textContent = '🔴 Recording... Speak now';
        document.getElementById('pulseRing').classList.add('recording');

    } catch (err) {
        document.getElementById('statusText').textContent = 
            '❌ Microphone access denied. Allow mic in browser settings.';
    }
}

async function stopRecording() {
    document.getElementById('stopBtn').style.display = 'none';
    document.getElementById('statusText').textContent = '⏳ Processing your audio...';
    document.getElementById('pulseRing').classList.remove('recording');
    document.getElementById('pulseRing').textContent = '⏳';

    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {
        // ✅ FIX: Use the actual MIME type the browser recorded in.
        //    This is what the blob really is — webm or ogg, not wav.
        const mimeType = mediaRecorder.mimeType || 'audio/webm';
        const audioBlob = new Blob(audioChunks, { type: mimeType });

        // Pick the right file extension to match the real format
        let extension = 'webm';
        if (mimeType.includes('ogg')) extension = 'ogg';

        const formData = new FormData();
        // ✅ FIX: Send the real filename with the correct extension
        formData.append('audio', audioBlob, `recording.${extension}`);
        // Also send the mime type so Python knows what it received
        formData.append('mime_type', mimeType);

        try {
            const response = await fetch('/transcribe', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('transcriptText').textContent = data.transcript;
                document.getElementById('transcriptBox').style.display = 'block';
                document.getElementById('aiText').textContent = data.ai_response;
                document.getElementById('aiBox').style.display = 'block';
                document.getElementById('statusText').textContent = 
                    '✅ Done! Press record to speak again.';
            } else {
                document.getElementById('statusText').textContent = 
                    '❌ Error: ' + data.error;
                console.error('Server error:', data.error);
            }
        } catch (err) {
            document.getElementById('statusText').textContent = 
                '❌ Network error: ' + err.message;
        }

        document.getElementById('recordBtn').style.display = 'inline-block';
        document.getElementById('pulseRing').textContent = '🎙';
    };
}