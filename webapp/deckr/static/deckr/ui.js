var selected = null;

function changeSelected(element) {
    if (selected != element) {
        $(selected).removeClass("selected");
        $(element).addClass("selected");
        selected = element;
    } else {
        $(element).removeClass("selected");
        selected = null;
    }
}

function cardMouseClick(e) {
    var element = e.toElement;
    changeSelected(element);
    console.log(selected);
}

/*
$(document).ready(function() {
    $(".card").on("click", cardMouseClick);
});
*/