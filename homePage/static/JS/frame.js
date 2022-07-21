let fileInput = document.getElementById('fileUpload');
let preview = document.getElementById('image-preview');
let info = document.getElementById('info');

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
    // read file
    let reader = new FileReader();
    reader.onload = function(e) {
        let data = e.target.result; // base64
        console.log(preview);
        preview.src = data;
    };
    // read files as .scv:
    reader.readAsDataURL(file);

});


function saveNewItem(form) {

    var url = preview.src; // current source of photo


    //let name = document.getElementById('title');
    let name = form.title.value;
    let details = form.description.value;
    let quantity = form.quantity.value;
    let price = form.price.value;
    let visibility = form.visibility.value; // 1: public; 0: private.
    let expire = form.expireDate.value;
    let location = form.postcode.value;


    // Judge if the input values are as expected
    if(name === ''){
        form.title.focus();
        return false;
    } else if(details === '') {
        form.description.focus();
        return false;
    }
    //.......

    // All enters meet requirement, back to submit form to homepage
    else {
        document.itemForm.submit();
    }

}

