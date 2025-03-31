/*
    HOL_TB_lockPeg
    v0.1
    2024-03-11
    Holly McDowell

Description: make a peg a lock peg by assigning all values to an expression column named "lock" and changed the peg colour to yellow

*/

function lockPeg(){

MessageLog.trace("Holly Script Starting")

var sNodes = selection.selectedNodes()
	MessageLog.trace("Selected Pegs: " + sNodes)

//find the LOCK Expression Column

var columnList = column.getColumnListOfType("EXPR");

for (var i = 0; i < columnList.length; i++) {


	var nName = column.getDisplayName(columnList[i])

	if (nName == "LOCK"){
	MessageLog.trace(nName + " Peg Found")
	var columnFound = "Lock EXPR found"
	}
}

// if needed, create a LOCK Expression Collumn

if (columnFound == "Lock EXPR found"){
MessageLog.trace(" No need to create new Lock Peg")
}else{
MessageLog.trace("Creating new Lock Peg")
column.add("LOCK", "EXPR")
}



for (var i = 0; i < sNodes.length; i++) {

var sNode = sNodes[i]

MessageLog.trace("starting script for: " + sNode)

// link selected peg values to Lock EXPR Column

node.unlinkAttr(sNode, "POSITION.X");
node.linkAttr(sNode, "POSITION.X", "LOCK");

node.unlinkAttr(sNode, "POSITION.Y");
node.linkAttr(sNode, "POSITION.Y", "LOCK");

node.unlinkAttr(sNode, "SCALE.X");
node.linkAttr(sNode, "SCALE.X", "LOCK");

node.unlinkAttr(sNode, "SCALE.Y");
node.linkAttr(sNode, "SCALE.Y", "LOCK");

node.unlinkAttr(sNode, "ROTATION.ANGLEZ");
node.linkAttr(sNode, "ROTATION.ANGLEZ", "LOCK");

node.unlinkAttr(sNode, "SKEW");
node.linkAttr(sNode, "SKEW", "LOCK");

//change peg colour

var newColor = new ColorRGBA(255, 250 , 0, 224);
node.setColor(sNode, newColor);

}



}
