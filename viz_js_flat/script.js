var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
ctx.strokeStyle = "grey";

ctx.imageSmoothingEnabled = true;
ctx.beginPath();
var setpoint = 250;

var curstate = 0;

function renderpupil(r, theta, offsets){
    ctx.fillStyle = "white";
    ctx.beginPath();
    var eyeLoc = [0, 0];
    var newrad = r /1.1;
    
    
    eyeLoc[0] = newrad * Math.cos(theta);
    eyeLoc[1] = newrad * Math.sin(theta);
    ctx.arc(xoffset + eyeLoc[0] + offsets[0], yoffset + eyeLoc[1]+ offsets[1], 120, 0, Math.PI * 2);   
    ctx.fill();

    eyeLoc[0] = r * Math.cos(theta);
    eyeLoc[1] = r * Math.sin(theta);

    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.arc(xoffset + eyeLoc[0] + offsets[0], yoffset + eyeLoc[1]+ offsets[1], 70, 0, Math.PI * 2);   
    ctx.fill();
}

function renderEyelid(height, offsets){
    ctx.beginPath();
    ctx.fillStyle = '#6C8593';
    ctx.roundRect(xoffset - 250 + offsets[0], yoffset - 250+ offsets[1], 500, height, [40, 40, 0, 0]);
    ctx.fill();

}

var framnum = 0;

function rendersclera(clip, offsets){
    ctx.fillStyle = '#2B74BA';
    ctx.beginPath();
    ctx.roundRect(xoffset - 250 + offsets[0], yoffset - 250 + offsets[1], 500, 500, 40);
    if(clip){
        ctx.save();
        ctx.clip();
    }
    else{
        ctx.fill();
    }

}

function rendereye(eyeposa, offsets){
    rendersclera(false, offsets);
    rendersclera(true, offsets);
    renderpupil(eyeposa[0], eyeposa[1], offsets);
    renderEyelid(lidheight, offsets);
    ctx.restore();

}

var lidheight = 0;
function animate(){
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    rendereye(eyepos, [0,0]);
    rendereye(eyepos, [550, 0]);
    
   

    
    framnum += 1;
    lidheight = controller(lidheight, setpoint, kp, kd, [0, 0]);
    
    requestAnimationFrame(animate);
  
}

setInterval(function() {
    
    setpoint = 500;
    kp = 0.3;
    kd = 0; 
    setTimeout(function() {
        setpoint = 250;
    }, 150);

}, 3000);

// setInterval(function() {
//     curstate += 1;
//     curstate %= states.length;
//     setpoint = states[curstate]['state'];
//     kp = states[curstate]['gains'][0];
//     kd = states[curstate]['gains'][1];
// }, 2000);

animate();