//var node = document.getElementById("item_card");
function addItem() {
    let insert;
    for (var i = 0; i < 5; i++) {
        //insert = document.createElement("div");
        insert = '<div class = "product_card"> args[0] </div>';
        $('#item_card').append(insert);
    }

}