
//Script developed by Marta Valleggi
function Reorder_Colors(){

scene.beginUndoRedoAccum("Reorder_Colors");

PaletteL = PaletteObjectManager.getScenePaletteList();

	var paletteToTidy = PaletteL.getPaletteById(PaletteManager.getCurrentPaletteId());


	var n = paletteToTidy.nColors;

	for (var i = n; i >0; i--)
	{
		for  (var j = 0; j < i; j++)
		{
			if (paletteToTidy.getColorByIndex(j).name >  	paletteToTidy.getColorByIndex(i).name)
			{
	paletteToTidy.moveColor(i,j);
			}
  		}
	}
scene.endUndoRedoAccum();

}
