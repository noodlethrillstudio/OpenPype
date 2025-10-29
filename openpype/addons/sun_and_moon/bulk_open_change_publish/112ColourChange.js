

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

function getColor(palette, id, name){
    return palette.getColorById(id);
    // palette.setCurrentPaletteById(palette.id);
    // for(var i=0; i < palette.nColors; ++i)
    //     var color = palette.getColorByIndex(i);
    //     if(palette.getColorName(i) == colorName)
    //         return color;
}

function changeColor(colour,red, green, blue, alpha ){
    var palette = getPalette("pr_cafe_bin");
    var color = getColor(palette, colour, "DUK_BodyFl");
    color.setColorData({r : red, g : green, b: blue, a : alpha});
}

var CFB_WheelieBinGL = changeColor( 59,  61,  52, 255, "0cbf3404b85024f7");
var CFB_WheelieBinDarkerGL = changeColor(  0,   0,   0, 255, "0cbf3404b8502fd2");
var CFB_WheelieBinFL = changeColor(113, 117, 101, 255, "0cbf3404b8502535");
var CFB_WheelieBinSplatFL = changeColor( 82,  87,  64, 255, "0cbf3404b8502601");
var CFB_WheelieBinSH = changeColor( 85,  88,  77, 255, "0cbf3404b8502568");
