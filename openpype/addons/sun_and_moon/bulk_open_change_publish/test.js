var sceneName = scene.currentScene();
var message = "The file \"" + sceneName + "\" exists."
MessageBox.information(message);

function getPalette(paletteName)
{
  // Find the first element palette list that owns a palette named "MyPalette"
    var paletteList = PaletteObjectManager.getScenePaletteList();

    for(var j=0; j < paletteList.numPalettes; ++j)
    {
      var palette = paletteList.getPaletteByIndex(j);
      if(palette.getName() == paletteName)
        return palette;
    }
}

function getColor(palette, colorName){
    return palette.getColorById("0c8daca61701357c");
    // palette.setCurrentPaletteById(palette.id);
    // for(var i=0; i < palette.nColors; ++i)
    //     var color = palette.getColorByIndex(i);
    //     if(palette.getColorName(i) == colorName)
    //         return color;
}

function changeColor(red, green, blue, alpha){
    var palette = getPalette("ch_0_Duck");
    MessageBox.information("Palette found: " + palette.getName());
    var color = getColor(palette, "DUK_BodyFl");
    color.setColorData({r : red, g : green, b: blue, a : alpha});
}

changeColor(180, 239, 80, 180);



MessageBox.information("Color changed.");
