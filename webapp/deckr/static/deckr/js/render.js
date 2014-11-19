function addDiv(parentId, divDict, place) {
    var parent = document.getElementById(parentId);
    var newDiv = document.createElement('div');
    var siblings = parent.childNodes;

    if (!divDict["id"]) {
        var err = "No id attr provided with div.";
        console.log(err);
        return err;
    } else if (document.getElementById(divDict["id"])) {
        var err = "Duplicate div. Div already exists.";
        console.log(err);
        return err;
    }
    for (key in divDict) {
        $(newDiv).attr(key,divDict[key]);
    }

    if (!place) {
        $('.selected').removeClass('selected');
        parent.appendChild(newDiv);
    } else {
        if (place < siblings.length) {
                $('.selected').removeClass('selected');
                toZone.insertBefore(newDiv, siblings[place]);
        } else {
            var err = "Place does not exist."
            console.log(err);
            return err;
        }
    }

}

function removeElementById(id) {
    /* Function to remove element. Currently unused. */
    element = document.getElementById(id);
    parent = element.parentElement;
    parent.removeChild(element);
}