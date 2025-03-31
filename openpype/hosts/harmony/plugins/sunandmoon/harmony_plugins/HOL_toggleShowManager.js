/*
    HOL_TB_toggleShowManger
    v0.1
    2024-03-08
    Holly McDowell

Description: check/uncheck all options in timeline's "show manager". This hides/shows all effects, comps, groups, and sounds.
Purpose for easy copy and pasting between _n and _f nodes

*/


function toggleShowManager(){

MessageLog.trace(" Script Starting")

Action.perform("onActionShowSoundLayers()", "timelineView")
Action.perform("onActionShowEffectLayers()", "timelineView")
Action.perform("onActionShowGroupLayers()", "timelineView")
Action.perform("onActionShowCompositeLayers()", "timelineView")

}
