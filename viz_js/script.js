var canvas = document.getElementById("canvas");

// Get the canvas context, which is used to draw on the canvas
var ctx = canvas.getContext("2d");

// Set the stroke color for the curve
ctx.strokeStyle = "black";

// Begin a new path
ctx.beginPath();
var x1 = 50;
var y1 = 50;

// Set the starting point for the curve
ctx.moveTo(x1, y1);
// var points = [
//     { x: 50, y: 50 },
//     { x: 100, y: 25 },
//     { x: 150, y: 75 },
//     { x: 200, y: 50 },
//     { x: 250, y: 100 },
//     { x: 300, y: 50 }
//   ];
var radius = 50;
var xoffset = 50;
var yoffset = 50;
// Set the points array
var points = [];
numPoints = 10;
// Use a loop to calculate the coordinates of each point
for (var i = 0; i < numPoints; i++) {
  var angle = (Math.PI * 2) / numPoints * i;
  points.push({ x: radius * Math.cos(angle) + xoffset, y: radius * Math.sin(angle)  + yoffset});
}
var speed = 4;
function animate(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.moveTo(points[0].x, points[0].y);
    tension = 1;
    var t = (tension != null) ? tension : 1;
    for (var i = 0; i < points.length; i++) {
        var p0 = (i > 0) ? points[i - 1] : points[0];
        var p1 = points[i];
        var p2 = points[(i + 1) % (points.length)];
        var p3 = (i != points.length - 2) ? points[(i + 2) % (points.length)] : p2;
        var cp1x = p1.x + (p2.x - p0.x) / 6 * t;
        var cp1y = p1.y + (p2.y - p0.y) / 6 * t;
        var cp2x = p2.x - (p3.x - p1.x) / 6 * t;
        var cp2y = p2.y - (p3.y - p1.y) / 6 * t;
        ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, p2.x, p2.y);
    }
    points[Math.floor(Math.random() * points.length)].x += Math.random() * speed;
    points[Math.floor(Math.random() * points.length)].y += Math.random() * speed;
    

    ctx.stroke();


    for (var i = 0; i < points.length; i++) {
        var point1 = points[i];
        ctx.beginPath();
        ctx.arc(point1.x, point1.y, 5, 0, Math.PI * 2);     
        ctx.stroke();
    }
    requestAnimationFrame(animate);
  

}
animate();