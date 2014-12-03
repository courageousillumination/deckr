// render.js

function addDiv(parentId, divDict, place) {
    var newDiv = document.createElement('div');
    var parent = document.getElementById(parentId);
    var siblings = parent.childNodes;

    if (!divDict["id"])
        return logAndReturnMessage("No id attr provided with div.");
    if (document.getElementById(divDict["id"]))
        return logAndReturnMessage("Duplicate div. Div already exists.");

    _.each(_.pairs(divDict), function(kv) {
        var k = kv[0];
        var v = kv[1];
        $(newDiv).attr(k, v);
    });

    if (!place) {
        unselectAll();
        parent.appendChild(newDiv);
    } else {
        if (place < siblings.length) {
            unselectAll();
            toZone.insertBefore(newDiv, siblings[place]);
        } else {
            return logAndReturnMessage("Place does not exist.");
        }
    }
}

function removeElementById(id) {
    /* Function to remove element. Currently unused. */
    var element = document.getElementById(id);
    var parent = element.parentElement;
    parent.removeChild(element);
}