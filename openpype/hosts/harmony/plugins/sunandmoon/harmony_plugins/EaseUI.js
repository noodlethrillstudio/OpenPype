/*

Version: 1.0

by Felipe Zanfelice (zanfelice.felipe@gmail.com)

Date: 18/01/2023

This script provides an easy to use UI for adjusting ease on selected keyframes. It allows animators to quickly reset or apply predefined ease values to their animation curves, improving workflow efficiency :).

*/

function TB_HandleEaseUI() {
    if (typeof TB_HandleEaseDialog !== "undefined") {
        TB_HandleEaseDialog.close();
    }

    TB_HandleEaseDialog = new QDialog();
    TB_HandleEaseDialog.setWindowTitle("Handle & Ease Control");

    var layout = new QVBoxLayout(TB_HandleEaseDialog);
    TB_HandleEaseDialog.setLayout(layout);

    function createButton(label, leftEase, rightEase) {
        var button = new QPushButton(label, TB_HandleEaseDialog);
        layout.addWidget(button, 0, 0); // Added missing parameters to prevent error
        button.clicked.connect(function () {
            applyBezierEase(leftEase, rightEase);
        });
    }

    function applyBezierEase(leftEase, rightEase) {
        var firstFrame = Timeline.firstFrameSel;
        var numFrames = Timeline.numFrameSel;
        var selectedFrames = [];

        if (numFrames > 0) {
            for (var i = 0; i < numFrames; i++) {
                selectedFrames.push(firstFrame + i);
            }
        } else {
            selectedFrames.push(firstFrame);
        }

        var columns = new Array();
        for (var i = 0; i < Timeline.numLayerSel; i++) {
            columns.push(Timeline.selToColumn(i));
        }

        if (columns.length === 0) {
            MessageLog.trace(" No function curves selected!");
            return;
        }

        scene.beginUndoRedoAccum("Apply Bezier Ease");

        for (var c = 0; c < columns.length; c++) {
            var col = columns[c];
            var numPoints = func.numberOfPoints(col);

            for (var j = 0; j < selectedFrames.length; j++) {
                var targetFrame = selectedFrames[j];

                for (var k = 0; k < numPoints; k++) {
                    if (func.pointX(col, k) === targetFrame) {
                        var v = func.pointY(col, k);
                        var prevFrame = k > 0 ? func.pointX(col, k - 1) : null;
                        var nextFrame = k < numPoints - 1 ? func.pointX(col, k + 1) : null;

                        var lx = func.pointHandleLeftX(col, k);
                        var ly = func.pointHandleLeftY(col, k);
                        var rx = func.pointHandleRightX(col, k);
                        var ry = func.pointHandleRightY(col, k);

                        // If it's the last keyframe, estimate the next frame
                        if (nextFrame === null && prevFrame !== null) {
                            nextFrame = targetFrame + (targetFrame - prevFrame);
                        }

                        // Apply left ease
                        if (leftEase !== null && prevFrame !== null) {
                            lx = targetFrame - ((targetFrame - prevFrame) * (leftEase / 100));
                            ly = v;
                        }

                        // Apply right ease
                        if (rightEase !== null && nextFrame !== null) {
                            rx = targetFrame + ((nextFrame - targetFrame) * (rightEase / 100));
                            ry = v;
                        }

                        func.setBezierPoint(col, targetFrame, v, lx, ly, rx, ry, false, "CORNER");

                        MessageLog.trace(" Frame " + targetFrame + ": Ease In: " + leftEase + "%, Ease Out: " + rightEase + "%");
                    }
                }
            }
        }

        scene.endUndoRedoAccum();
        MessageLog.trace(" Bezier adjustments applied.");
    }

    // Create UI buttons
    createButton("Reset Both Handles", 0, 0);
    createButton("Reset Left Handle", 0, null);
    createButton("Reset Right Handle", null, 0);
    createButton("Ease 25 (Left)", 25, null);
    createButton("Ease 25 (Right)", null, 25);
    createButton("Ease 50 (Left)", 50, null);
    createButton("Ease 50 (Right)", null, 50);
    createButton("Ease 75 (Left)", 75, null);
    createButton("Ease 75 (Right)", null, 75);

    TB_HandleEaseDialog.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint);
    TB_HandleEaseDialog.show();
}

// Run the UI
TB_HandleEaseUI();
