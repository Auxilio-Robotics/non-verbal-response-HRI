var isMouseDown = false;
var selectedPointIndex = -1;
function getMousePos(canvas, e) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  };
}

function distance(p1, p2) {
  var dx = p1.x - p2.x;
  var dy = p1.y - p2.y;
  return Math.sqrt(dx * dx + dy * dy);
}

// Handle mousedown event
canvas.addEventListener("mousedown", function (e) {
  // Get the mouse position relative to the canvas
  var mousePos = getMousePos(canvas, e);

  // Check if the mouse is over any of the points
  for (var i = 0; i < points.length; i++) {
    if (distance(mousePos, points[i]) < 10) {
      // Mouse is over a point, set the flag and selected point index
      isMouseDown = true;
      selectedPointIndex = i;
      break;
    }
  }
});


// Handle mousemove event
canvas.addEventListener("mousemove", function (e) {
  // Get the mouse position relative to the canvas
  var mousePos = getMousePos(canvas, e);
  eyepos[1] = Math.atan2((mousePos.y - yoffset),  (mousePos.x - xoffset));
  eyepos[0] = Math.sqrt((mousePos.y - yoffset) ** 2 +   (mousePos.x - xoffset) ** 2);
  // Check if the mouse is down and over a point
  if (isMouseDown && selectedPointIndex >= 0) {
    // Update the position of the selected point
    points[selectedPointIndex] = mousePos;

    // Redraw the curve

  }
});

// Handle mouseup event
canvas.addEventListener("mouseup", function (e) {
  // Reset the flag and selected point index
  if (isMouseDown) {
    console.log((points));
  }
  isMouseDown = false;
  selectedPointIndex = -1;

});
