function Unlink_Nodes()
{
	var sNodes = selection.selectedNodes();


	scene.beginUndoRedoAccum( "Unlink Nodes" );


	for( var idx in sNodes )
	{
		// unlink src nodes
		var numInput = node.numberOfInputPorts( sNodes[idx] );
		for( var i = numInput -1; i >= 0 ; i-- )
		{
			node.unlink( sNodes[idx], i )
		}

		// make a list of dst nodes
		var numOutput = node.numberOfOutputPorts( sNodes[idx] );
		var dstNodeList = [];
		for( var i = 0; i < numOutput; i++ )
		{
			var numOutlinks = node.numberOfOutputLinks( sNodes[idx], i );

			for( var ii = 0; ii < numOutlinks; ii++ )
			{
				dstNodeList.push( node.dstNode( sNodes[idx], i, ii ) );
			}
		}

		// unlink dst nodes
		for( var i = 0; i < dstNodeList.length; i++ )
		{
			var numDstInput = node.numberOfInputPorts( dstNodeList[i] );
			for( var ii = numDstInput -1; ii >= 0 ; ii-- )
			{
				var curSrc = node.srcNode( dstNodeList[i], ii );
				if( curSrc == sNodes[idx] )
				{
					node.unlink( dstNodeList[i], ii )
				}
			}
		}
	}


	scene.endUndoRedoAccum();
}
