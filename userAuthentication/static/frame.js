let fileInput = document.getElementById('fileUpload');
let preview = document.getElementById('image-preview');


// listen event of changing:
fileInput.addEventListener('change', function() {
    // clear preview area of photo
    preview.style.backgroundImage = '';
    if (!fileInput.value) {
        alert('You did not choose a photo!');
        return;
    }
    let file = fileInput.files[0];
    let size = file.size;
    if (size >= 1024 * 1024) {
        alert('The size of photo exists limit.');
        return false;
    }

    if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
        alert('It is not an image!');
        return;
    }
    // 读取文件:
    let reader = new FileReader();
    reader.onload = function(e) {
        let data = e.target.result; // base64
        console.log(preview);
        preview.src = data;
    };
    // 以DataURL的形式读取文件:
    reader.readAsDataURL(file);

});




