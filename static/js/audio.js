//const dot = document.getElementById("dot");
const record = document.getElementById("record");
const stop = document.getElementById("stop");
//const subm = document.getElementById("submit_button");
const rerecord = document.getElementById("re-record");
//const soundClips = document.getElementById("sound-clips");
const audioCtx = new(window.AudioContext || window.webkitAudioContext)(); // 오디오 컨텍스트 정의
const analyser = audioCtx.createAnalyser();

function makeSound(stream) {
    const source = audioCtx.createMediaStreamSource(stream);

    source.connect(analyser);
    analyser.connect(audioCtx.destination);
}

console.log(navigator.mediaDevices);
if (navigator.mediaDevices) {
    console.log('getUserMedia supported.');

    const constraints = { audio: true };
    let chunks = [];

    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        
        record.onclick = e => {
            e.preventDefault();
            mediaRecorder.start();
            console.log("recorder started", mediaRecorder.state);
            stop.classlist.remove('disabled');
        }

        stop.onclick = e => {
            e.preventDefault();
            mediaRecorder.stop();
            console.log("recorder stopped", mediaRecorder.state);
        }
        
        mediaRecorder.onstop = e => {
            console.log("data available after MediaRecorder.stop() called.");
            const blob = new Blob(chunks, {
                type: 'audio/wav codecs=opus'
            });

            // 오디오 데이터 ajax
            const formData = new FormData();
            formData.append("audio_blob", blob);

            $.ajax({
                type: "POST",
                url: "/module/recog",
                data: formData,
                contentType: false,
                processData: false,
                success: function(result) {
                    console.log("success");
                    location.replace('/module/recog_res');
                },
                error: function(result) {
                    alert("failed");
                }
            })

            /* chunks = [];            // 오디오 데이터 재초기화
            const audioURL = URL.createObjectURL(blob);  // audioURL 이 url로 들어가면 오디오 파일 있음
            audio.src = audioURL; */   // audioURL로 audio객체에 데이터 설정
            
            console.log("recorder stopped");
        }
        mediaRecorder.ondataavailable = e => {
            chunks.push(e.data);
        }
    })
    .catch(err => {
        console.log('The following error occurred: ' + err);
    })
}