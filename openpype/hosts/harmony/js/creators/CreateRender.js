/* global PypeHarmony:writable, include */
// ***************************************************************************
// *                             CreateRender                                *
// ***************************************************************************


// check if PypeHarmony is defined and if not, load it.
if (typeof PypeHarmony === 'undefined') {
    var OPENPYPE_HARMONY_JS = System.getenv('OPENPYPE_HARMONY_JS') + '/PypeHarmony.js';
    include(OPENPYPE_HARMONY_JS.replace(/\\/g, "/"));
}


/**
 * @namespace
 * @classdesc Code creating render containers in Harmony.
 */
var CreateRender = function() {};


/**
 * Create render instance.
 * @function
 * @param {array} args Arguments for instance.
 */
CreateRender.prototype.create = function(args) {

    if (args[2] == 1){
        node.setTextAttr(args[0], 'DRAWING_TYPE', 1, 'PNGDP4');
        node.setTextAttr(args[0], 'DRAWING_NAME', 1, args[1]);
        node.setTextAttr(args[0], 'MOVIE_PATH', 1, args[1]);
        node.setTextAttr(args[0], 'MOVIE_FORMAT', 1, "com.toonboom.mp4.1.0");

    }
    else{
    node.setTextAttr(args[0], 'DRAWING_TYPE', 1, 'PNG4');
    node.setTextAttr(args[0], 'DRAWING_NAME', 1, args[1]);
    node.setTextAttr(args[0], 'MOVIE_PATH', 1, args[1]);
    node.setTextAttr(args[0], 'EXPORT_TO_MOVIE', 1, "true")
    node.setTextAttr(args[0], 'MOVIE_FORMAT', 1, "com.toonboom.mp4.1.0");
    }
};

// add self to Pype Loaders
PypeHarmony.Creators.CreateRender = new CreateRender();
