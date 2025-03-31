function exposeDrawings(){

scene.beginUndoRedoAccum("Expose Drawings");

var curFrame = frame.current();

var numSelLayers = Timeline.numLayerSel;


 for ( var i = 0; i < numSelLayers; i++ )
{

 if ( Timeline.selIsColumn(i ) ){
var nomeC = Timeline.selToColumn(i);

}

var tipo = column.type(nomeC);


if (tipo == "DRAWING"){

//LISTA DE TODOS OS DRAWINGS ****************************
var lista = column.getDrawingTimings(nomeC);

lista.sort(function(a, b){return a-b});
var k = 0;

var limite = curFrame + lista.length;
//MessageLog.trace("Tamanho da lista: " + lista.length);
for (j=curFrame;j<limite; j++){
	//MessageLog.trace("Frame:" + j);

	column.setEntry(nomeC, 1, j, lista[k]);
	//MessageLog.trace("Trocando para Desenho: " + k);
	k++;


}


}

}

//MessageLog.trace("*************************************");
scene.endUndoRedoAccum();
}

//by williamsaito@gmail.com
//2014
