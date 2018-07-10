let localStream;
let recorder;
let recordChunk
const { remote: { dialog } } = require('electron');
const fs = require('fs');

console.log("xxx0");
navigator.mediaDevices.getUserMedia({
    video: true
}).then(stream => {
    localStream = stream;
    
    preview.srcObject = stream;
});

function streamOn() {
    document.getElementById("control").style = "display:none";
    document.getElementById("stream").style = "display:";

    recorder = new MediaRecorder(localStream);
    recorder.ondataavailable = e => {
        recordChunk.push(e.data);
    };
    recordChunk = [];
    recorder.start();
};
function streamOff() {
    recorder.stop();
    let blob = new Blob(recordChunk);
    let dlURL = URL.createObjectURL(blob);
    dlLink.href = dlURL;
    let dt = new Date();
    dlLink.download = `rec_${[dt.getFullYear(), dt.getMonth() + 1, dt.getDate(), dt.getHours(), dt.getMinutes(), dt.getSeconds(), dt.getMilliseconds()].map(val => ('0' + val).slice(-2))}.webm`;

    let fr = new FileReader();
    fr.onload = _ => {
        showSaveDialog(fr.result);
    }
    fr.readAsArrayBuffer(blob);


};


function showSaveDialog(arrayBuffer) {
    document.getElementById("control").style = "display:";
    document.getElementById("stream").style = "display:none";

    let buffer = new Buffer(arrayBuffer);
    let dt = new Date();
    dialog.showSaveDialog({
        filters: [{
            name: `webm file`,
            extensions: ['webm']
        }]
    }, fileName => {
        if (fileName) {
            fs.writeFile(fileName, buffer, function (err) {
                if (err) {
                    alert("An error ocurred creating the file " + err.message);
                }
            });
        }
    });
}