//by williamsaito@gmail.com
//zerar Drawings v1.01
//2014
//Edited by Holly McDowell 2024

function swapToEmpty(){

	scene.beginUndoRedoAccum("Add ZZ_Blank");

	var firstFrame = Timeline.firstFrameSel;
	var endFrame = firstFrame + Timeline.numFrameSel - 1;
	var numSelLayers = Timeline.numLayerSel;

	var drawingName ="ZZ_Blank";

	for (i =0; i < numSelLayers; i++ ){
		var a = firstFrame;
		while(a<=endFrame){

			if ( Timeline.selIsNode( i ) ){

			var nomeN = Timeline.selToNode(i);


			}

			 if ( Timeline.selIsColumn(i ) ){
			var nomeC = Timeline.selToColumn(i);

			}


			var type = column.type(nomeC);

			if (type == "DRAWING"){
			//Entry = Drawing
			column.setEntry(nomeC, 1, a, drawingName);
			}
		a++;
		}

	}
	//MessageLog.trace("*************************************");
	scene.endUndoRedoAccum();
	}
