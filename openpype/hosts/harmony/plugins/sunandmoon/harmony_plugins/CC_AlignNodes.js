/*
    CC_AlignNodes
    v2.0
    2018-12-15
    Chris Carter - chrishcarter@gmail.com
*/

function CC_AlignNodes_Horizontal()
{
	AlignNodes("horizontal")
}

function CC_AlignNodes_Vertical()
{
	AlignNodes("vertical")
}

// static variables
var functionName        = "AlignNodes"
var spacing_X           = 8
var spacing_Y           = 5
var nodeExpandedHeight  = 69
var nodeCollasedExpandedDifference  = 44

this.AlignNodes = function( direction )
{

    // ------------ contained functions ---------------------
    // they are located here to keep user script loading process simpler

    this.print = function( msg ){	MessageLog.trace( msg )}

    this.nodeWrapper = function(nodeName, nodeX, nodeY, nodeWidth, nodeHeight)
    {
        this.nodeName = nodeName
        this.nodeX = nodeX
        this.nodeY = nodeY
        this.nodeWidth = nodeWidth
        this.nodeHeight = nodeHeight
    }

    this.get_selectionArray = function()
    {
        var selectedNodes = selection.selectedNodes()
        var selectionArray =[]
        for(var i in selectedNodes)
        {
            selNode         = selectedNodes[i]
            selNodeX        = node.coordX(selNode)
            selNodeY        = node.coordY(selNode)
            selNodeWidth    = node.width(selNode)
            selNodeHeight   = node.height(selNode)

            selectionArray[i] = new nodeWrapper(selNode,selNodeX,selNodeY,selNodeWidth,selNodeHeight)
        }
        //print(selectionArray[i].nodeName + " = " +  selectionArray[i].nodeX + "     "  + selectionArray[i].nodeY)
        return(selectionArray)
    }

    this.get_attributeAverage_X = function(selectionArray)
    {
        var sum =0;
        for (var i in selectionArray)
        {
            sum += selectionArray[i].nodeX;
        }
        averageValue = sum/selectionArray.length;
        return(averageValue);
    }

    this.get_attributeAverage_Y = function(selectionArray)
    {
        var sum =0;
        for (var i in selectionArray)
        {
            sum += selectionArray[i].nodeY;

            if(selectionArray[i].nodeHeight == nodeExpandedHeight)
            {
                sum += nodeCollasedExpandedDifference
            }
        }
        averageValue = sum/selectionArray.length;
        return(averageValue);
    }

    this.sort_byAttribute_descending = function(selectionArray, nodeAttribute)
    {
        function compare(a,b)
        {
            var x = a[nodeAttribute]
            var y = b[nodeAttribute]

            if (x < y)	return -1
            if (y > x)	return 1
            return 0
        }

        selectionArray.sort(compare)
        return selectionArray
    }


    this.noOverlap_X = function( selectionArray)
    {
        for (var i in selectionArray)
        {
            var j =Number(i)+1
            if (j == selectionArray.length) return;

            var n0 			= selectionArray[i].nodeName
            var n0_W		= node.width( n0 )
            var n0_X_L 		= node.coordX( n0 )
            var n0_X_R 		= (n0_X_L + n0_W + spacing_X)

            var n1 			= selectionArray[j].nodeName
            var n1_W		= node.width( n1 )
            var n1_X_L		= node.coordX( n1 )
            var n1_X_R 		= ( n1_X_L + n1_W + spacing_X)

            if (n1_X_L <= n0_X_R)
            {
                node.setCoord( n1 , n0_X_R , node.coordY( n1 ))
            }
        }
    }

    this.noOverlap_Y = function( selectionArray)
    {
        for (var i in selectionArray)
        {
            var j =Number(i)+1
            if (j == selectionArray.length)
            {
                return;
            }

            var n0 			    = selectionArray[i].nodeName
            var n0_H			= ( node.height( n0 ) + spacing_Y )
            var n0_Y_top 		= node.coordY( n0)
            var n0_Y_bottom 	= ( n0_Y_top + n0_H )
            var n1		 	    = selectionArray[j].nodeName

            var n1_H			= ( node.height( n1 ) + spacing_Y)
            var n1_Y_top		=   node.coordY( n1)
            var n1_Y_bottom	    = ( n1_Y_top + n1_H)

            if (n1_Y_top <= n0_Y_bottom )
            {
                node.setCoord( n1, node.coordX( n1 ) , n0_Y_bottom)
            }
        }
    }

	// ----- end of contained functions, this is now the main function

    scene.beginUndoRedoAccum("alignNodes_" + direction)
	var selNodesTotal = selection.numberOfNodesSelected()
	if (selNodesTotal <= 0) return
	var selectionArray = get_selectionArray()

	//----- left to Right ------

	if (direction == "horizontal")
	{
		var selectionArray = sort_byAttribute_descending(selectionArray, "nodeX")
		var average_y = get_attributeAverage_Y( selectionArray )

        	for (var j in selectionArray)
        	{
                newX = selectionArray[j].nodeX
                newY = average_y;

                if ( selectionArray[ j ].nodeHeight == nodeExpandedHeight)
                {
                    newY = average_y - nodeCollasedExpandedDifference
                }

                node.setCoord(selectionArray[j].nodeName,  newX , newY )
        	}
		noOverlap_X(selectionArray)
	}

	// ----- Top to Bottom -----

	else if (direction == "vertical")
	{
		var selectionArray 	= sort_byAttribute_descending(selectionArray, "nodeY")
		var average_x 		= get_attributeAverage_X( selectionArray );
		var widthSum 		= 0;

		for (var i in selectionArray)
		{
			widthSum += selectionArray[i].nodeWidth;
		}

		var widthAverage =widthSum/ selectionArray.length;

		for (var j in selectionArray)
		{
			var compensatedWidth        = selectionArray[j].nodeWidth - widthAverage;
			selectionArray[j].nodeX     = average_x -  ( compensatedWidth / 2 )
			newX                        = selectionArray[j].nodeX
			newY                        = selectionArray[j].nodeY

			node.setCoord(selectionArray[j].nodeName, newX , newY);
		}

		noOverlap_Y(selectionArray)
	}
    print( functionName + " : Success ")

    scene.endUndoRedoAccum();
}
