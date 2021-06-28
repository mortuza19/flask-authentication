function ShowCam() {
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 100
    });
    Webcam.attach('#my_camera');
}
window.onload= ShowCam;

function snap() {
    Webcam.snap( function(data_uri) {
        document.getElementsByClassName('d-none')[0].innerHTML =
        '<img id="image" src="'+data_uri+'"/>';
        document.getElementById('image').value = data_uri.split(',')[1];
        document.getElementsByClassName('d-none')[0].classList.add('results');
    });
}