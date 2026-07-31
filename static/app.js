const video = document.getElementById('videoElement');
const canvas = document.getElementById('canvasElement');

const ctx = canvas.getContext('2d', { willReadFrequently: true });
const outputImage = document.getElementById('outputImage');

const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${wsProtocol}//${window.location.host}/ws/video`;
const ws = new WebSocket(wsUrl);

const FPS = 10;
const captureWidth = 640;
const captureHeight = 480;

canvas.width = captureWidth;
canvas.height = captureHeight;

navigator.mediaDevices.getUserMedia({ 
    video: { width: captureWidth, height: captureHeight, facingMode: "environment" }, 
    audio: false 
})
.then(stream => {
    video.srcObject = stream;
})
.catch(err => {
    console.error("Error accediendo a la cámara: ", err);
    alert("Revisá los permisos de la cámara o asegurate de estar por HTTPS/Localhost.");
});

ws.onopen = () => {
    console.log("WebSocket Conectado");
    
    setInterval(() => {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            const frameData = canvas.toDataURL('image/jpeg', 0.6);
            
            ws.send(frameData);
        }
    }, 1000 / FPS);
};

ws.onmessage = (event) => {
    outputImage.src = event.data;
};

ws.onclose = () => {
    console.log("WebSocket Desconectado");
};