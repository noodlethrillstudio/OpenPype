/*
    HOL_TB_linkToHndsComp
    v0.1
    2024-05-09
    Holly McDowell

Description:
Script to link a selected drawing node to the handles comp
Identifies the handles comp by a required specific name
"HND_CMP"
*/

function linkToHndsComp(){

	MessageLog.trace("Holly Script Starting")

	//retrieve selected nodes


	var sNodes = selection.selectedNodes()
	MessageLog.trace(sNodes)


	//find hnds comp

	var nType = ["COMPOSITE"];
	var allComps = node.getNodes(nType);
	//MessageLog.trace(allComps)
	var hndComp = []


	for (var i = 0; i < allComps.length; i++) {
		var comp = allComps[i]

	//change the name here if you'd prefer your handles comp to be called something else

			if (comp.indexOf("HND_CMP") > -1){
			MessageLog.trace("\n")
			MessageLog.trace(comp)
			 MessageLog.trace("hnds comp found = " + comp)
			hndComp.push(comp);
			} else {

			}
		}

	//message box for error saying they need to make sure the hnds comp is name appropriately

	if (hndComp == 0){
	MessageLog.trace("handles comp not found")
	MessageBox.information("No handles composite found, please rename to \"HND-CMP\"")
	}

	//link nodes to comp

	MessageLog.trace("ready to link " + hndComp)

	for (var i = 0; i < sNodes.length; i++){
		selNode = sNodes[i]

		MessageLog.trace("Ready to link to " + selNode);
		node.link(selNode,0,hndComp,0);

		}

	}
