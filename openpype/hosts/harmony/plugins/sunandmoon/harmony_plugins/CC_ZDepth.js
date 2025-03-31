/*
    CC_ZDepth
    v2.0
    2018-12-15
    Chris Carter - chrishcarter@gmail.com
*/

function CC_ZDepth_Forward()
{
	ZDepth(FW)
}

function CC_ZDepth_Backward()
{
	ZDepth(BW)
}

// static variables

var functionName    = "ZDepth"
var fNow            = frame.current();
var increment       = 0.001
var FW		        = "+"
var BW		        = "-"

function ZDepth( direction )
{
	this.print = function( msg ){	MessageLog.trace( msg )}


	msg = functionName
	var selectedNodes = selection.selectedNodes()

	if (selectedNodes[1])
	{
        print( msg + " : ERROR : select one node only")
        return
	}
	if  (selectedNodes[0] == null)
	{
        print( msg + " : ERROR : no node selected")
        return
	}

	var originalSelection = selection.selectedNode(0);

	function findPegAbove(thisNode)
    {
        var inputPorts = node.numberOfInputPorts(thisNode);
        if (inputPorts == 0)
        {
            print( msg +  " : ERROR : no PEG above this node");
				return false;
        }
        else
        {
            var nodeAbove = node.flatSrcNode(thisNode, 0);
            if (node.type(nodeAbove) == "PEG")
            {
                selection.clearSelection();
                selection.addNodeToSelection(nodeAbove);
            }
            else
            {
                selection.clearSelection();
                selection.addNodeToSelection(nodeAbove);
                findPegAbove(nodeAbove);
            }
				return true;
        }
    }

	if (node.type(originalSelection) != "PEG")
	{
		findPegAbove(originalSelection)
	}

	var selPeg = selection.selectedNode(0)

	zDepth_original 	= node.getTextAttr(selPeg, fNow, "POSITION.Z");


	msg +=  ' ' + direction + ' ' + increment
	if (direction == FW)
	{
        zDepth_new			        = parseFloat(zDepth_original) + parseFloat(increment)
        node.setTextAttr(selPeg, "POSITION.Z", fNow, zDepth_new)
        msg 						+=  '\t: ' + selPeg  +'\t '+ zDepth_original + ' \t--> ' + zDepth_new
        print(msg)
    }

	else
	{
        zDepth_new			        = parseFloat(zDepth_original) - parseFloat(increment)
        node.setTextAttr(selPeg, "POSITION.Z", fNow, zDepth_new)
        msg 						+=  '\t: ' + selPeg  +'\t '+ zDepth_original + ' \t--> ' + zDepth_new
        print(msg)
	}

	selection.clearSelection();
    selection.addNodeToSelection(originalSelection);
}
