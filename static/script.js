console.log("✅ JS Loaded");

let recorder;
let chunks = [];

/* =========================
   MESSAGE
========================= */
function addMessage(text){
    let msg = document.createElement("div");
    msg.innerText = text;
    document.getElementById("messages").appendChild(msg);
}

/* =========================
   SPEAK
========================= */
function speak(text){
    let speech = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(speech);
}

/* =========================
   CREATE DASHBOARD CARD
========================= */
function addToDashboard(summary, type){

    let card = document.createElement("div");
    card.className = "card";
    card.innerText = summary;

    let t = (type || "").toLowerCase();

    if(t.includes("auto")){
        document.getElementById("auto").appendChild(card);

    } else if(t.includes("health")){
        document.getElementById("health").appendChild(card);

    } else if(t.includes("life")){
        document.getElementById("life").appendChild(card);

    } else {
        document.getElementById("property").appendChild(card);
    }
}

/* =========================
   🎤 START RECORDING
========================= */
async function startRecording(){

    try{
        const stream = await navigator.mediaDevices.getUserMedia({audio:true});

        recorder = new MediaRecorder(stream);
        chunks = [];

        recorder.ondataavailable = e=>{
            if(e.data.size>0) chunks.push(e.data);
        };

        recorder.start();

        addMessage("🎤 Recording started...");

    }catch(err){
        console.error(err);
        addMessage("❌ Mic permission denied");
    }
}

/* =========================
   ⏹ STOP RECORDING
========================= */
function stopRecording(){

    if(!recorder){
        alert("Start recording first");
        return;
    }

    recorder.stop();

    recorder.onstop = async ()=>{

        addMessage("⏳ Processing...");

        let blob = new Blob(chunks,{type:"audio/webm"});

        let form = new FormData();
        form.append("audio",blob,"recording.webm");

        try{
            const response = await fetch("/transcribe",{
                method:"POST",
                body:form
            });

            const data = await response.json();

            console.log("RESPONSE:", data);

            // 🧑 Transcript
            addMessage("🧑 You: " + data.transcript);

            // 📊 Summary
            addMessage("📊 Summary: " + data.summary);

            // 📊 Route to dashboard
            addToDashboard(data.summary, data.type);

            // 🔊 Speak summary
            speak(data.summary);

        }catch(err){
            console.error(err);
            addMessage("❌ Error processing audio");
        }
    };
}

/* =========================
   📁 FILE UPLOAD
========================= */
async function upload(){

    let file = document.getElementById("file").files[0];

    if(!file){
        alert("Select file");
        return;
    }

    let form = new FormData();
    form.append("file",file);

    addMessage("📁 Uploading...");

    try{
        const response = await fetch("/upload",{
            method:"POST",
            body:form
        });

        const data = await response.json();

        console.log("UPLOAD RESPONSE:", data);

        addMessage("📊 Summary: " + data.summary);

        addToDashboard(data.summary, data.type);

        speak(data.summary);

    }catch(err){
        console.error(err);
        addMessage("❌ Upload failed");
    }
}