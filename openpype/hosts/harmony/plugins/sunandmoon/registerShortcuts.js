var usersScriptFolder = specialFolders.userScripts;
MessageLog.trace(usersScriptFolder)

function addSunandmoonShortcut(category, script, functionName) {
    var shortcutID = category + "_" + functionName;
    var scriptPath = usersScriptFolder + "/" + script
    var functionLaunch = functionName + ' in ' + scriptPath;
    var scriptName = script.split("/").pop().split("\\").pop();

    var shortcut = {
        id: shortcutID,
        text: scriptName.replace(".js", "") + " : " + functionName,
        action: functionLaunch,
        longDesc: "Runs function " + functionName + " of script " + script,
        categoryId: category,
        categoryText: category
    };
    MessageLog.trace(shortcut["action"])

    ScriptManager.addShortcut(shortcut);
}

function register_script_library_plugins() {
    //If you want to add or remove shortcuts, put them in this dictionary
    var shortcutDict = {
        "ANM_Set_Layer_Pivots_At_Center_Of_Drawings.js": ["ANM_Set_Layer_Pivots_At_Center_Of_Drawings"],
        "USR_Unlink_Nodes.js": ["Unlink_Nodes"],
        "swapToZero.js": ["swapToZero"],
        "CC_ZDepth.js": ["CC_ZDepth_Forward", "CC_ZDepth_Backwards"],
        "rig_ignore.js": ["rigIgnoreSelectParent", "rigIgnoreSelectChild"],
        "NC_FindAndReplace.js": ["NC_FindAndReplace"],
        "MC_CreateColoredBackdrop.js": ["createColoredBackdrop"],
        "CC_AlignNodes.js": ["CC_AlignNodes_Horizontal", "CC_AlignNodes_Vertical"]
    };

    for (var script in shortcutDict) {
        var functionNames = shortcutDict[script];

        if (Array.isArray(functionNames)) {
            functionNames.forEach(function(functionName) {
                addSunandmoonShortcut("Script Shortcuts", script, functionName);
            });
        }
    }
}

MessageLog.trace("Registering script library plugins.");
register_script_library_plugins();
MessageLog.trace("Registration finished.");
