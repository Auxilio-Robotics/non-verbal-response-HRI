var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
ctx.strokeStyle = "grey";

ctx.imageSmoothingEnabled = true;
ctx.beginPath();
var setpoint = circle;

var curstate = 0;

var points = [];
for (var i = 0; i < numPoints; i++) {
    var angle = (Math.PI * 2) / numPoints * i;
    points.push({ x: radius * Math.cos(angle) + xoffset, y: radius * Math.sin(angle) + yoffset });
}


ctx.moveTo(points[0].x, points[0].y);

function renderpupil(r, theta, offsets){
    ctx.fillStyle = "#363a3d";
    ctx.beginPath();
    // theta = theta  * Math.PI / 180;
    var eyeLoc = [0, 0];
    var newrad = r / 1.1;
    
    newrad = Math.min(newrad, 160);
    
    console.log(newrad, r);
    eyeLoc[0] = newrad * Math.cos(theta);
    eyeLoc[1] = newrad * Math.sin(theta);
    ctx.arc(xoffset + eyeLoc[0] + offsets[0], yoffset + eyeLoc[1]+ offsets[1], 80, 0, Math.PI * 2);   
    ctx.fill();

    eyeLoc[0] = Math.min(r, 170) * Math.cos(theta);
    eyeLoc[1] = Math.min(r, 170) * Math.sin(theta);

    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.arc(xoffset + eyeLoc[0] + offsets[0], yoffset + eyeLoc[1]+ offsets[1], 60, 0, Math.PI * 2);   
    ctx.fill();

    ctx.beginPath();
    ctx.fillStyle = "white";  
    ctx.arc(xoffset + 30 + eyeLoc[0]+ offsets[0], yoffset - 30 + eyeLoc[1]+ offsets[1], 10, 0, Math.PI * 2);
    ctx.fill();
    
}
var framnum = 0;

function rendersclera(){

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
    ctx.fillStyle = "white";
    ctx.fill();
    for (var i = 0; i < points.length; i++) {
        var point1 = points[i];
        ctx.beginPath();
        ctx.arc(point1.x, point1.y, 3, 0, Math.PI * 2);     
        ctx.stroke();
    }

}
var eyepos = [0, 0];
function animate(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    rendersclera();

    renderpupil(eyepos[0], eyepos[1], [0,0 ]);

    
    framnum += 1;
    // eyeLoc[0] = 100 * Math.sin(framnum/50.0) + 100;
    // eyeLoc[1] = Math.cos(framnum / 50.0)  + 100;
    points = controller(points, setpoint, kp, kd, states[curstate]['offsets']);
    requestAnimationFrame(animate);
  
}

// setInterval(function() {
    
//     setpoint = blink;
//     kp = 0.6;
//     kd = 0; 
//     setTimeout(function() {
//         setpoint = states[curstate]['state'];
//     }, 100);

// }, 1000);

setInterval(function() {
    curstate += 1;
    curstate %= states.length;
    setpoint = states[curstate]['state'];
    kp = states[curstate]['gains'][0];
    kd = states[curstate]['gains'][0];
}, 2000);

animate();