var kp = 0.2;
var kd = 0.05;
var stateChanging = false;
var previousError = 0;
function controller(curpoints, setpoint, kp, kd, offsets){
    xerror = setpoint - curpoints + offsets[0];

    xderror = previousError - xerror;
    curpoints +=  kp*xerror  + kd*(xderror);
    previousError = xerror;
    return curpoints;
}