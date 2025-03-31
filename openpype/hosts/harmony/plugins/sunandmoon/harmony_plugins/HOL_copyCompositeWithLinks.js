/*
    HOL_TB_copyCompositeWithLinks
    v0.1
    2023-07-07
    Holly McDowell

Description:
Script to duplicate a comp along with its input links to parent nodes

*/

function copyCompositeWithLinks(){

MessageLog.trace("Holly Script Starting")

//retrieve selected node

var sNode = selection.selectedNode(0);
MessageLog.trace(sNode)

//retrieve number of parent input ports

var wLinksNumber = node.numberOfInputPorts(sNode,frame.current(),"")
MessageLog.trace(wLinksNumber)

//retrieve source nodes plugged into the input ports

//var parents = node.srcNode(sNode,0);
//MessageLog.trace(parents)

//loop to retrieve the nodes plugged into the input ports

var inputNodesArray = []
var x = 0

for (var i = 0; i < wLinksNumber; i++)
	 {
	var inputNode = node.srcNode(sNode,i);

	//MessageLog.trace(inputNode);
	inputNodesArray.push(inputNode);
	}

MessageLog.trace("Nodes connected to the input ports: " + inputNodesArray)

//Add new composite close to original composite
var posX = node.coordX(sNode)
var posY = node.coordY(sNode)

var newComp =  node.add(node.parentNode(selection.selectedNode(0)),node.getName(sNode), "COMPOSITE", posX + (+150), posY + (+50), 0);

//reverse array because for some silly reason its doing it backwards

var revInputNodesArray = inputNodesArray.reverse()

//link new comp to input nodes array

for (var i = 0; i < wLinksNumber; i++)
	 {
	node.link(revInputNodesArray[i],0,newComp,0)
	}

}
