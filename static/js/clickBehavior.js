var initialChoiceMade = false;
var initialChoiceXpath = "";
var similarElementsXpath = "";
var unchosen = [];
var initialChoice;
var similarElements = [];
var YELLOW = "#FDFF47";
var GREEN = "#BDFF44";
var UPARROW = 38;
var DOWNARROW = 40;
var RIGHTARROW = 39;
var broadenBy = 2;
var lastScrollLevel = 0;

/*var getXPathButton= document.createElement('input');
getXPathButton.setAttribute('type','button');
getXPathButton.onClick = function(){
    console.log("clicked");
    alert(similarElementsXpath);
 document.getElementById('getXPathButton').appendChild(getXPathButton);

 }*/

clear = function(){
    document.getElementById("subscribeButton").disabled = true;
    highLight(similarElements,"transparent");
    initialChoiceMade = false;
    initialChoiceXpath = "";
    similarElementsXpath = "";
    unchosen = [];
    initialChoice = undefined;
    similarElements = [];
}

broadenSimilarNodes = function(amountToBroaden){
    console.log("It is");
    console.log(similarElementsXpath);
    similarElementsXpath = broadenXPath(similarElementsXpath,amountToBroaden);
    console.log("now is");
    console.log(similarElementsXpath);
    similarElements = getElementsByXPath(initialChoice.ownerDocument, similarElementsXpath);
    highLight(similarElements,YELLOW);
}

overRideScroll = function(){
    console.log("In overRideScroll");
    if (initialChoiceMade==true){
        var newScrollLevel = $(this).scrollTop();
        var delta = 0;
        // but what happens if the make isn't big enough to scroll on?
        if (newScrollLevel>lastScrollLevel){
            //broaden
            delta = 1;
        } else {
            if (newScrollLevel < lastScrollLevel) {
                delta = -1;
            }
        }
        broadenSimilarNodes(delta);
        lastScrollLevel = newScrollLevel;
    }
}


restrictXPath = function(broadXPath,chosenXPath,removedXPath){
    console.log("In Restrict xpath");
    console.log(broadXPath);
    console.log(chosenXPath);
    console.log(removedXPath);
    var broadList = broadXPath.split('/');
    var chosenList = chosenXPath.split('/');
    var removedList = removedXPath.split('/');
    for (var i = chosenList.length - 1; i> -1; i--){
        if (removedList[i] != chosenList[i]){
            broadList[i]= chosenList[i];
            console.log("outputing...");
            console.log(broadList.join('/'));
            return broadList.join('/');
        }
    }
    console.log("No difference found in restrict xpath?");
}

isAlreadyBroadened = function(xpath){
    // if the xpath before the last element is *, then we say the xpath has been broadened
    // if the last element is * then the xpath has been broadened
    var lastSlashIndex = xpath.lastIndexOf("/");
    var secondToLastSlashIndex = xpath.substr(0, lastSlashIndex).lastIndexOf("/");
    console.log(xpath.slice(secondToLastSlashIndex+1,lastSlashIndex));
    if (xpath.slice(secondToLastSlashIndex+1,lastSlashIndex)=="*" || xpath.slice(-1) == "*" || xpath.slice(-2)=="*/"){
        return true;
    } else{
        console.log("not broadened:");
        console.log(xpath);
        return false;
    }
}

countHowBroadened = function(xpath){
    var howBroadened = 0;
    var index = xpath.length-1;
    var lastSlashIndex;
    var secondToLastSlashIndex;
    while (xpath.length > 1){
        if (isAlreadyBroadened(xpath)===false){
            console.log(xpath);
            return howBroadened;
        }else{
            lastSlashIndex =  xpath.lastIndexOf("/");
            if (lastSlashIndex>-1) {
                xpath = xpath.slice(0, lastSlashIndex);
                howBroadened+=1;
                console.log("blarge");
                console.log(xpath)
            } else{
                return false;
            }
        }
    }
}

broadenXPath = function(xpath,amountToBroaden) {
    // grab the last part of the xpath and subtract it from the working xpath before starting
    // we do this beacuse we don't want to replace the last part with an asterisk
    console.log(xpath);
   // var partAfterLastSlash = xpath.slice(xpath.lastIndexOf('/'),xpath.length+1);
    var secondToLastSlashIndex = xpath.slice(0,xpath.lastIndexOf('/')).lastIndexOf('/');
    var partAfterSecondToLastSlash = xpath.slice(secondToLastSlashIndex,xpath.length+1);
    console.log("part after second to last slash");
    console.log(partAfterSecondToLastSlash);
    xpath = xpath.slice(0, secondToLastSlashIndex);

    // /html/body/center/table/tbody/tr[3]/td/table/tbody/tr[10]/td[3]/a to
    // /html/body/center/table/tbody/tr[3]/td/table/tbody/tr[10]/*/a
    if (amountToBroaden > 0) {
        if (isAlreadyBroadened(xpath)){
            var howBroadened = countHowBroadened(xpath);
            if (howBroadened==false){
            } else {
                amountToBroaden+=howBroadened;
            }
        }

        // iteratively replace the path with asterisks
        var asterisks = "";
        for (var i = 0; i < amountToBroaden; i++) {
            xpath = xpath.slice(0, xpath.lastIndexOf('/'));
            asterisks +="/*";
        }
        xpath = xpath + asterisks + partAfterSecondToLastSlash;
    }
    return xpath;
}

      /*  var lastSlashIndex = xpath.lastIndexOf('/');
        if (lastSlashIndex != -1) {
            var secondToLastSlashIndex = xpath.substr(0, lastSlashIndex).lastIndexOf(('/'));
            console.log(xpath.substr(0,lastSlashIndex));
            if (secondToLastSlashIndex != -1) {
                return broadenXPath(xpath.substr(0, secondToLastSlashIndex + 1), amountToBroaden - 1) + "*" + xpath.substr(lastSlashIndex);
		}
		}
    return xpath;
    }*/
    // var p2 = p1.substr(0,p1.lastIndexOf('/'));
    //alert(p2);

/*
getParent = function(xpath){
    var parentXpath = getXpathParent(xpath);
    var parents = [];

    while (parentXpath!= '' && parents.length==0 ){
    console.log("parent xpath is "+parentXpath);
    parentXpath = getXpathParent(parentXpath);
    console.log("now trying "+parentXpath);
    parents = getElementsByXPath(parentXpath+'/*');
    console.log("number of parents "+parents.length);
    }
    return parents;
    }
*/
highLight = function(nodes,color){
    for (var nodeIndex = 0; nodeIndex < similarElements.length; nodeIndex++) {
        nodes[nodeIndex].style.backgroundColor = color;
    }
}
getElementsByXPath = function(doc, xpath) {
    console.log("In getElementsByXPath, with " +xpath);
    var nodes = [];

    try {
	var result = doc.evaluate(xpath, doc, null, XPathResult.ANY_TYPE, null);
	for (var item = result.iterateNext(); item; item = result.iterateNext())
	    nodes.push(item);
    }
    catch (exc)
    {
	console.log("no elements found on path " + xpath);
    // Invalid xpath expressions make their way here sometimes.  If that happens,
    // we still want to return an empty set without an exception.
    }
    return nodes;
};

clickBehavior = function(){
    try {
    // if this is the first time they select something, make it main selection
	if (initialChoiceMade === false) {
	    initialChoice = this;
	    initialChoiceMade = true;
	    console.log("is the button enabled?");
            document.getElementById("subscribeButton").disabled = false;
	    console.log(document.getElementById("subscribeButton").disabled);

    //this.style.backgroundColor = "#FDFF47";
    //var similarElements = [].slice.call(this.parentNode.childNodes);
	    initialChoiceXpath = getElementTreeXPath(this);
	    console.log("Initial choice xpath: ", initialChoiceXpath);
    //var similarElements = getParent(initialChoiceXpath);
	    console.log(getElementTreeXPath(this));
	    similarElementsXpath = broadenXPath(getElementTreeXPath(this),broadenBy);
	    console.log(similarElementsXpath);
	    similarElements = getElementsByXPath(initialChoice.ownerDocument, similarElementsXpath);
    //var similarElements = getElementsByXPath(initialChoice.ownerDocument, getElementTreeXPath(this));
	    highLight(similarElements,YELLOW);
    //  for (var similarElementsIndex = 0; similarElementsIndex < similarElements.length; similarElementsIndex++) {
    //      similarElements[similarElementsIndex].style.backgroundColor = "#FDFF47";
    //  }
	} else {
        // if they reselect their initial selection, reset everything
            if (this === initialChoice) {
		clear()
        // otherwise, add their new choice to the list of unchosen things and highlight it in green (for now, later we'll be unhighlighting them)
            } else {
		similarElementsXpath = restrictXPath(similarElementsXpath,initialChoiceXpath, getElementTreeXPath(this));
		highLight(similarElements,"transparent");
            //this.style.backgroundColor = GREEN;
		similarElements = getElementsByXPath(initialChoice.ownerDocument,similarElementsXpath);
		highLight(similarElements,YELLOW);
		unchosen.push(this);
	    }
	}
	return false;
    } catch(e) {
        console.log(e.message);
    }finally {
        return false;
    }
};

getElementTreeXPath = function(element)
{
    var paths = [];

            // Use nodeName (instead of localName) so namespace prefix is included (if any).
    for (; element && element.nodeType == 1; element = element.parentNode)
    {
        var index = 0;
        for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling)
        {
            // Ignore document type declaration.
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
		continue;

            if (sibling.nodeName == element.nodeName)
		++index;
        }

        var tagName = element.nodeName.toLowerCase();
        var pathIndex = "[" + (index+1) + "]";
            //var pathIndex = (index ? "[" + (index+1) + "]" : "");
        paths.splice(0, 0, tagName + pathIndex);
    }

    return paths.length ? "/" + paths.join("/") : null;
};

window.onload =  function() {
  //  $(window).scroll(overRideScroll);
 /*   $(window).scroll(function() {
        $(this).scrollTop(0);
	})*/
    var anchors = document.getElementsByTagName("a");
    for (var linkIndex = 0; linkIndex < anchors.length; linkIndex++) {
        anchors[linkIndex].onclick = clickBehavior;
    }
};

window.addEventListener("keydown", function(e) {
    console.log("key down");
    console.log(e.keyCode);
    console.log(initialChoiceMade);
    // space and arrow keys
    if(initialChoiceMade && [39,38, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
        if (e.keyCode==UPARROW){
            console.log("up");
            broadenSimilarNodes(1);
        } else if (e.keyCode == DOWNARROW){
            console.log("down");
            broadenSimilarNodes(-1)
        } else if (e.keyCode == RIGHTARROW){
	    console.log("right arrow")
            var http = new XMLHttpRequest();
            var url = "/subscribe/save";
	        http.open("POST",url,true);
            http.setRequestHeader("X-CSRFToken", "{{csrf_token}}");

            var parameters = {
               "url": "{{url}}",
               "xpath": similarElementsXpath,
               "data":"blarg"
            };
            console.log(JSON.stringify(parameters));
	        http.send(JSON.stringify(parameters))
        
	    }
    }


}, false);


