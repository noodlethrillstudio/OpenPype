
function checkNode(){
    doc = $.scn;
    currentNode = doc.getSelectedNodes();
    nodeName = currentNode[0].name;
    return nodeName;
}

function selectParent() {
Action.perform("onActionNaviSelectParent()", "Node View");
}

function selectParentIgnore(){
selectParent();
checkSkipParent();
return;
}

function checkSkipParent(){
nodeName = checkNode();

if (nodeName.indexOf("IGN_") === 0) {
    MessageLog.trace("'IGN_' found as prefix to node name, skipping node");
    selectParent();
    checkSkipParent();
} else {
    return;
}
return;
}

function selectChild(){
Action.perform("onActionNaviSelectChild()", "Node View");
}

function selectChildIgnore(){
selectChild();
checkSkipChild();
return;
}

function checkSkipChild(){
nodeName = checkNode();

if (nodeName.indexOf("IGN_") === 0) {
    MessageLog.trace("'IGN_' found as prefix to node name, skipping node");
    selectChild();
    checkSkipChild();
} else {
    return;
}
return;
}

function rigIgnoreSelectParent(){
if (selection.numberOfNodesSelected() == 0){return}
selectParent();
checkSkipParent();
}

function rigIgnoreSelectChild(){
if (selection.numberOfNodesSelected() == 0){return}
selectChild();
checkSkipChild();
}
