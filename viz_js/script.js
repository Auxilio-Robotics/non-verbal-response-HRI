var canvas = document.getElementById("canvas");
// Get the canvas context, which is used to draw on the canvas
var ctx = canvas.getContext("2d");

// Set the stroke color for the curve
ctx.strokeStyle = "grey";
ctx.fillStyle = "white";
ctx.imageSmoothingEnabled = true;
// Begin a new path
ctx.beginPath();
var x1 = 50;
var y1 = 50;

// Set the starting point for the curve
ctx.moveTo(x1, y1);
// Set the points array
var points = [];
for (var i = 0; i < numPoints; i++) {
    var angle = (Math.PI * 2) / numPoints * i;
    points.push({ x: radius * Math.cos(angle) + xoffset, y: radius * Math.sin(angle) + yoffset });
}
var speed = 0;

var isMouseDown = false;

// Index of the selected point (if any)
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
    if(isMouseDown){
        console.log((points));
    }
    isMouseDown = false;
    selectedPointIndex = -1;
    
  });


var setpoint = circle;
function animate(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.moveTo(points[0].x, points[0].y);
    tension = 1;
    var t = (tension != null) ? tension : 1;
    for (var i = 0; i < points.length; i++) {
        var p0 = (i > 0) ? points[i - 1] : points[points.length - 1];
        var p1 = points[i];
        var p2 = points[(i + 1) % (points.length)];
        var p3 =  points[(i + 2) % (points.length)];
        var cp1x = p1.x + (p2.x - p0.x) / 6 * t;
        var cp1y = p1.y + (p2.y - p0.y) / 6 * t;
        var cp2x = p2.x - (p3.x - p1.x) / 6 * t;
        var cp2y = p2.y - (p3.y - p1.y) / 6 * t;
        ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, p2.x, p2.y);
    }
    // points[Math.floor(Math.random() * points.length)].x += Math.random() * speed;
    // points[Math.floor(Math.random() * points.length)].y += Math.random() * speed;

    
    
    ctx.fill();


    for (var i = 0; i < points.length; i++) {
        var point1 = points[i];
        ctx.beginPath();
        ctx.arc(point1.x, point1.y, 3, 0, Math.PI * 2);     
        ctx.stroke();
    }

    points = controller(points, setpoint);
    requestAnimationFrame(animate);
  
}
var curstate = 1;
// setInterval(function() {
    
//     setpoint = blink;
//     setTimeout(function() {
//         setpoint = states[curstate];
//     }, 100);

// }, 5000);

setInterval(function() {
    
    curstate += 1;
    curstate %= states.length;
    setpoint = states[curstate]['state'];
    
    

}, 2000);

animate();