var rig_ignore = {

    checkNode: function () {
        doc = $.scn;
        currentNode = doc.getSelectedNodes();
        nodeName = currentNode[0].name;
        return nodeName;
    },

    selectParent: function () {
        // change this to be selectParentSkipEffects
        Action.perform("onActionNaviSelectParent()", "Node View");
    },

    selectParentIgnore: function () {
        rig_ignore.selectParent();
        rig_ignore.checkSkipParent();
        return;
    },

    checkSkipParent: function () {
        nodeName = rig_ignore.checkNode();

        if (nodeName.indexOf("IGN_") === 0) {
            // defaultCommand
            MessageLog.trace("'IGN_' found in node name, skipping node");
            rig_ignore.selectParent();
            rig_ignore.checkSkipParent();
        } else {
            return;
        }
        return;
    },

    selectChild: function () {
        // change this to be selectParentSkipEffects
        Action.perform("onActionNaviSelectChild()", "Node View");
    },

    selectChildIgnore: function () {
        rig_ignore.selectChild();
        rig_ignore.checkSkipChild();
        return;
    },

    checkSkipChild: function () {
        nodeName = rig_ignore.checkNode();

        if (nodeName.indexOf("IGN_") === 0) {
            // defaultCommand
            MessageLog.trace("'IGN_' found in node name, skipping node");
            rig_ignore.selectChild();
            rig_ignore.checkSkipChild();
        } else {
            return;
        }
        return;
    },

    parentAction: function(){
        rig_ignore.selectParent();
        rig_ignore.checkSkipParent();
    },

    childAction: function(){
        rig_ignore.selectChild();
        rig_ignore.checkSkipChild();
    },

    launchScript: function () {

        var selectParentIgnoreAction = {
            id: "com.sunandmoon.selectParentIgnore",
            text: "Select Parent, ignoring unwanted nodes",
            onTrigger: function () {
                rig_ignore.parentAction();
                return;
            }
        };

        var selectChildIgnoreAction = {
            id: "com.sunandmoon.selectChildIgnore",
            text: "Select Child, ignoring unwanted nodes",
            onTrigger: function () {
                rig_ignore.childAction();
                return;
            }
        };

        var selectParentIgnoreShortcut = {
            id           : "com.sunandmoon.selectParentIgnore",
            text         : "Select Parent, ignoring unwanted nodes",
            action       : "parentAction in C:\\Users\\will_sunandmoonstudi\\AppData\\Local\\pypeclub\\openpype\\3.18\\openpype-v3.18.12-sunandmoon.6\\openpype\\hosts\\harmony\\plugins\\sunandmoon\\rig_ignore.js",
            order        : "256",
            longDesc     : "acts as a replacment to 'select parent, skipping effects', but also skips 'IGN_' nodes",
            categoryId   : "Sun And Moon Scripts",
            categoryText : "Sun And Moon Scripts",
            value        : "B"};

        var selectChildIgnoreShortcut = {
            id           : "com.sunandmoon.selectChildIgnore",
            text         : "Select Child, ignoring unwanted nodes",
            action       : "childAction in C:\\Users\\will_sunandmoonstudi\\AppData\\Local\\pypeclub\\openpype\\3.18\\openpype-v3.18.12-sunandmoon.6\\openpype\\hosts\\harmony\\plugins\\sunandmoon\\rig_ignore.js",
            order        : "256",
            longDesc     : "acts as a replacment to 'select child, skipping effects', but also skips 'IGN_' nodes",
            categoryId   : "Sun And Moon Scripts",
            categoryText : "Sun And Moon Scripts",
            value        : "Shift + B"};



        ScriptManager.addAction(selectParentIgnoreAction);
        ScriptManager.addAction(selectChildIgnoreAction);

        ScriptManager.addShortcut(selectParentIgnoreShortcut);
        ScriptManager.addShortcut(selectChildIgnoreShortcut);


        ScriptManager.addMenuItem({
            targetMenuId: "Animation",
            id: selectParentIgnoreAction.id,
            text: selectParentIgnoreAction.text,
            action: selectParentIgnoreAction.id
        });

        ScriptManager.addMenuItem({
            targetMenuId: "Animation",
            id: selectChildIgnoreAction.id,
            text: selectChildIgnoreAction.text,
            action: selectChildIgnoreAction.id
        });

    }
};
function parentAction(){
    rig_ignore.parentAction()
}
function childAction(){
    rig_ignore.childAction()
}
