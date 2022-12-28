function update() {
    $("tensionvalue").innerHTML = "(" + $("tension").value + ")";
    drawSplines();
}
$("showPoints").onchange = $("showControlLines").onchange = $("tension").onchange = update;

// utility function
function $(id) { return document.getElementById(id); }
var canvas = $("canvas"), ctx = canvas.getContext("2d");

function setCanvasSize() {
    canvas.width = parseInt(window.getComputedStyle(document.body).width);
    canvas.height = parseInt(window.getComputedStyle(document.body).height);
}
window.onload = window.onresize = setCanvasSize();

function mousePositionOnCanvas(e) {
    var el = e.target, c = el;
    var scaleX = c.width / c.offsetWidth || 1;
    var scaleY = c.height / c.offsetHeight || 1;

    if (!isNaN(e.offsetX))
        return { x: e.offsetX * scaleX, y: e.offsetY * scaleY };

    var x = e.pageX, y = e.pageY;
    do {
        x -= el.offsetLeft;
        y -= el.offsetTop;
        el = el.offsetParent;
    } while (el);
    return { x: x * scaleX, y: y * scaleY };
}

canvas.onclick = function (e) {
    var p = mousePositionOnCanvas(e);
    addSplinePoint(p.x, p.y);
};

function drawPoint(x, y, color) {
    ctx.save();
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, 2 * Math.PI);
    ctx.fill()
    ctx.restore();
}
canvas.onmousemove = function (e) {
    var p = mousePositionOnCanvas(e);
    $("mouse").innerHTML = p.x + "," + p.y;
};

var pts = []; // a list of x and ys

// given an array of x,y's, return distance between any two,
// note that i and j are indexes to the points, not directly into the array.
function dista(arr, i, j) {
    return Math.sqrt(Math.pow(arr[2 * i] - arr[2 * j], 2) + Math.pow(arr[2 * i + 1] - arr[2 * j + 1], 2));
}

// return vector from i to j where i and j are indexes pointing into an array of points.
function va(arr, i, j) {
    return [arr[2 * j] - arr[2 * i], arr[2 * j + 1] - arr[2 * i + 1]]
}

function ctlpts(x1, y1, x2, y2, x3, y3) {
    var t = $("tension").value;
    var v = va(arguments, 0, 2);
    var d01 = dista(arguments, 0, 1);
    var d12 = dista(arguments, 1, 2);
    var d012 = d01 + d12;
    return [x2 - v[0] * t * d01 / d012, y2 - v[1] * t * d01 / d012,
    x2 + v[0] * t * d12 / d012, y2 + v[1] * t * d12 / d012];
}

function addSplinePoint(x, y) {
    pts.push(x); pts.push(y);
    drawSplines();
}
function drawSplines() {
    clear();
    cps = []; // There will be two control points for each "middle" point, 1 ... len-2e
    for (var i = 0; i < pts.length - 2; i += 1) {
        cps = cps.concat(ctlpts(pts[2 * i], pts[2 * i + 1],
            pts[2 * i + 2], pts[2 * i + 3],
            pts[2 * i + 4], pts[2 * i + 5]));
    }
    if ($("showControlLines").checked) drawControlPoints(cps);
    if ($("showPoints").checked) drawPoints(pts);

    drawCurvedPath(cps, pts);

}
function drawControlPoints(cps) {
    for (var i = 0; i < cps.length; i += 4) {
        showPt(cps[i], cps[i + 1], "pink");
        showPt(cps[i + 2], cps[i + 3], "pink");
        drawLine(cps[i], cps[i + 1], cps[i + 2], cps[i + 3], "pink");
    }
}

function drawPoints(pts) {
    for (var i = 0; i < pts.length; i += 2) {
        showPt(pts[i], pts[i + 1], "black");
    }
}

function drawCurvedPath(cps, pts) {
    var len = pts.length / 2; // number of points
    if (len < 2) return;
    if (len == 2) {
        ctx.beginPath();
        ctx.moveTo(pts[0], pts[1]);
        ctx.lineTo(pts[2], pts[3]);
        ctx.stroke();
    }
    else {
        ctx.beginPath();
        ctx.moveTo(pts[0], pts[1]);
        // from point 0 to point 1 is a quadratic
        ctx.quadraticCurveTo(cps[0], cps[1], pts[2], pts[3]);
        // for all middle points, connect with bezier
        for (var i = 2; i < len - 1; i += 1) {
            // console.log("to", pts[2*i], pts[2*i+1]);
            ctx.bezierCurveTo(
                cps[(2 * (i - 1) - 1) * 2], cps[(2 * (i - 1) - 1) * 2 + 1],
                cps[(2 * (i - 1)) * 2], cps[(2 * (i - 1)) * 2 + 1],
                pts[i * 2], pts[i * 2 + 1]);
        }
        ctx.quadraticCurveTo(
            cps[(2 * (i - 1) - 1) * 2], cps[(2 * (i - 1) - 1) * 2 + 1],
            pts[i * 2], pts[i * 2 + 1]);
        ctx.stroke();
    }
}
function clear() {
    ctx.save();
    // use alpha to fade out
    ctx.fillStyle = "rgba(255,255,255,.7)"; // clear screen
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.restore();
}

function showPt(x, y, fillStyle) {
    ctx.save();
    ctx.beginPath();
    if (fillStyle) {
        ctx.fillStyle = fillStyle;
    }
    ctx.arc(x, y, 5, 0, 2 * Math.PI);
    ctx.fill();
    ctx.restore();
}

function drawLine(x1, y1, x2, y2, strokeStyle) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    if (strokeStyle) {
        ctx.save();
        ctx.strokeStyle = strokeStyle;
        ctx.stroke();
        ctx.restore();
    }
    else {
        ctx.save();
        ctx.strokeStyle = "pink";
        ctx.stroke();
        ctx.restore();
    }
}
