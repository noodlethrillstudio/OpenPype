const harmonyFileName = scene.currentScene()
var match = harmonyFileName.match(/ep\d+/);
var epPath = "C:/SynologyDrive/Duck_and_Frog/out/20251022_bulk_render"
var outPath = epPath+ "/"+match+"/"+harmonyFileName+"/"+harmonyFileName

function disableWriteNodes(){
    var writeNodes = node.getNodes(["WRITE"]);
    for (i = 0; i<writeNodes.length; ++i){
        node.setEnable(writeNodes[i], false);
    }
}

function createRenderNode(){
    var allNodes = node.getNodes(["COMPOSITE"])
    var compNode = "Top/SSU_Master-CMP"
    for(i=0; i < allNodes.length; i++){
        if (node.getName(allNodes[i]) == "SSU_Master-CMP_1"){
            compNode = "Top/SSU_Master-CMP_1"
        }
    }

    var writeNode = node.add("Top", "renderCompositeMain_batch", "WRITE",0,0,0)
    var x = node.coordX(compNode)
    var y = node.coordY(compNode)

    node.setCoord(writeNode, x, y)

    node.setTextAttr(writeNode, 'DRAWING_TYPE', 1, 'PNGDP4');
    node.setTextAttr(writeNode, 'DRAWING_NAME', 1, outPath);
    node.link(compNode, 0, writeNode, 0, true, true)
return
}

function main(){
    disableWriteNodes()
    createRenderNode()
}

main()
