// Use this script to determine output format

// Following code will be called at the end of Write Node rendering
// operations to create a movie file from rendered images.

// ...


/*

Full cmd: ffmpeg -framerate 25 -i %04d.png -c:v libx264  -qp 0 -f mp4 -pix_fmt yuv444p output.mp4


*/


try
{
  var images = WriteNode.imageFiles();
  for (var i = 0; i < images.length; i++)
  {
    MessageLog.trace("generated image : " + images[i]);
  }
  var ext = ".mov"
  var outputFile = WriteNode.movieDir() + "/" + WriteNode.movieName() + ext;
//   var soundFile;
//   if ( WriteNode.hasSound() )
//   {
//     soundFile = WriteNode.exportSound(16, 2, 22050);
//   }
  // Use ffmpeg to generate movie from rendered images.
  var ffmpeg = "ffmpeg";
  if (about.isMacArch()) {
    ffmpeg = System.getenv("HOME") + "/ffmpeg";
  }
  else if (about.isWindowsArch()) {
    ffmpeg = "C:/ffmpeg/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe";
  }

  var args = [
    ffmpeg,
    "-y",
    "-start_number",
    WriteNode.startFrame(),
    "-i",
    WriteNode.imageFilesPattern()
  ];
//   if (soundFile)
//   {
//     args = args.concat([
//       "-i",
//       soundFile,
//       "-c:a",
//       "copy"
//     ]);
//   }
  args = args.concat([
    "-vframes",
    WriteNode.stopFrame() - WriteNode.startFrame() + 1,
    "-r",
    WriteNode.frameRate(),
    "-pix_fmt",
    "rgba64be",
    "-c:v",
    "png",
    outputFile
  ]);
  MessageLog.trace("execute : " + args.join(" "));
  var process = new Process2(args.join(" "));
  var retCode = process.launch();
  if (retCode != 0)
  {
    MessageLog.trace("Process return code: " + retCode);
    if (process.errorMessage())
    {
      MessageLog.trace("Error: " + process.errorMessage());
    }
    MessageLog.error("Movie generation script error");
  }
  if (retCode == 0){
    MessageLog.trace("successfully rendered " + outputFile)
  }
}
catch(err)
{
  MessageBox.information("Movie generation script error: " + err);
}
