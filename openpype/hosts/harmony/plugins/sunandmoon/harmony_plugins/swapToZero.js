//by williamsaito@gmail.com
//zerar Drawings v1.01
//2014

function swapToZero(){

scene.beginUndoRedoAccum("Zerar Drawings");

var firstFrame = Timeline.firstFrameSel;
var endFrame = firstFrame + Timeline.numFrameSel - 1;
var numSelLayers = Timeline.numLayerSel;

//numero do drawing que vai ser colocado
var drawingName = "ZZ_Blank";

for (i = 0; i < numSelLayers; i++ ){
	var a = firstFrame;
	while(a<=endFrame){

		if ( Timeline.selIsNode( i ) ){

		var nomeN = Timeline.selToNode(i);


		}

		 if ( Timeline.selIsColumn(i ) ){
		var nomeC = Timeline.selToColumn(i);

		}


		var tipo = column.type(nomeC);

		if (tipo == "DRAWING"){
		//Entry = Drawing,
		//bool setEntry (String columnName, int subColumn, double atFrame, String value)
		column.setEntry(nomeC, 1, a, drawingName);
		}
	a++;
	}

}
//MessageLog.trace("*************************************");
scene.endUndoRedoAccum();
}
