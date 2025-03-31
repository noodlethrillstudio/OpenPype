/*
    HOL_ChangeNodeOpacity
    v0.1
    2023-07-04
    Holly McDowell

Description:
Shortcut to change the opacity of a drawing from 100% to a specific amount and back again.

*/

function changeNodeOpacity(){

MessageLog.trace("Holly Script Starting")

//retrieve selected node

var sNode = selection.selectedNode(0);
MessageLog.trace(sNode)

//retrieve opacity value

var wAttr = node.getAttr(sNode, frame.current(), "opacity");

var myAttributeValue = wAttr.doubleValue();

MessageLog.trace(myAttributeValue);

//change value to 100, 40 if value = 100, then deselect and selct again to push change

if (myAttributeValue == 100) {
    wAttr.setValue(40);
	selection.clearSelection(sNode);
	selection.addNodeToSelection(sNode);
	MessageLog.trace("Opacity changed to 40");
} else {
    wAttr.setValue(100);
	selection.clearSelection(sNode);
	selection.addNodeToSelection(sNode);
	MessageLog.trace("Opacity changed to 100");
}

}
