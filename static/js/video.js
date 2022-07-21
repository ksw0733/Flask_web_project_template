const record = document.getElementById("record");
const stop = document.getElementById("stop");
const cam = document.getElementById("cam");
const td1 = document.getElementById("td1");
const td2 = document.getElementById("td2");
const audioCtx = new(window.AudioContext || window.webkitAudioContext)(); // 오디오 컨텍스트 정의
const analyser = audioCtx.createAnalyser();
const video = document.createElement('video');

function tableData() {
    video.setAttribute('controls', '');
    td1.append(video);

    let input = document.createElement("input");
    input.classList.add("btn", "btn-primary", "mr-2");
    input.setAttribute('type', 'submit');
    input.setAttribute('value', '제출');
    td2.append(input);
    input = document.createElement("input");
    input.classList.add("btn", "btn-secondary");
    input.setAttribute('type', 'reset');
    input.setAttribute('value', '취소');
    td2.append(input);
}

console.log(navigator.mediaDevices);
if (navigator.mediaDevices) {
    console.log('getUserMedia supported.');

    const constraints = { video:true, audio:true };
    let chunks = [];

    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        const mediaRecorder = new MediaRecorder(stream);

        record.onclick = e => {
            e.preventDefault();
            mediaRecorder.start();
            console.log("recorder started", mediaRecorder.state);
            record.classList.replace('btn-danger', 'btn-secondary')
            cam.classList.add('mr-2')
            cam.innerHTML = '<i class="fa fa-video"></i>'
            stop.classList.replace('btn-dark', 'btn-danger')
            stop.classList.remove('disabled');
        }

        stop.onclick = e => {
            e.preventDefault();
            tableData();
            mediaRecorder.stop();
            console.log("recorder stopped", mediaRecorder.state);
        }
        
        mediaRecorder.onstop = e => {
            console.log("data available after MediaRecorder.stop() called.");
            const blob = new Blob(chunks, {
                type: 'video/mp4'
            });

            // 비디오 데이터 ajax
            const formData = new FormData();
            formData.append("video_blob", blob);

            $.ajax({
                type: "POST",
                url: "/module/video",
                data: formData,
                contentType: false,
                processData: false,
                success: function(result) {
                    console.log("success");
                },
                error: function(result) {
                    alert("failed");
                }
            })
            const videoURL = URL.createObjectURL(blob);
            video.src = videoURL
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