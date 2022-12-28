var kp = 0.2;
var kd = 0.05;
var stateChanging = false;
var previousError = []
for(var i = 0; i < circle.length; i++){
    previousError.push({'x' : 0, 'y' : 0});
}
function controller(curpoints, setpoint, kp, kd, offsets){
    var xerrorsum = 0;
    var yerrorsum = 0;

    // kp = ;
    // kd = states[curstate]['gains'][1];

    for(var i = 0; i < curpoints.length; i++){
        xerror = setpoint[i].x - curpoints[i].x + offsets[0];
        yerror = setpoint[i].y - curpoints[i].y + offsets[1];
        xerrorsum += xerror;
        yerrorsum += yerror;
        xderror = setpoint[i].x - curpoints[i].x
        yderror = setpoint[i].y - curpoints[i].y
        curpoints[i].x += kp*xerror  + kd*(previousError[i].x - xderror);
        curpoints[i].y += kp*yerror  + kd*(previousError[i].y - yderror);

        previousError[i] = {"x" : xerror, "y" : yerror};
        
    }
    stateChanging = false;
    if(xerrorsum < 10 && yerrorsum < 10){
        stateChanging = true;
    }
    
    return curpoints;
    
}