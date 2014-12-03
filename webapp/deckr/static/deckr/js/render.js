// render.js

function addDiv(parentId, divDict, place) {
    var newDiv = document.createElement('div');

    if (!divDict["id"])
        return logAndReturnMessage("No id attr provided with div.");
    if (document.getElementById(divDict["id"])) {
        return logAndReturnMessage("Duplicate div. Div already exists.");

    _.each(_.pairs(divDict), function(kv) {
        var k = kv[0];
        var v = kv[1];
        $(newDiv).attr(k, v);
    });
}

function removeElementById(id) {
    /* Function to remove element. Currently unused. */
    var element = document.getElementById(id);
    var parent = element.parentElement;
    parent.removeChild(element);
}