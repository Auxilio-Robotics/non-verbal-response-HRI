var bored = [
    {
        "x": 650,
        "y": 350
    },
    {
        "x": 599,
        "y": 476
    },
    {
        "x": 495,
        "y": 536
    },
    {
        "x": 361,
        "y": 554
    },
    {
        "x": 238,
        "y": 542
    },
    {
        "x": 109,
        "y": 475
    },
    {
        "x": 50,
        "y": 350.00000000000006
    },
    {
        "x": 94,
        "y": 316
    },
    {
        "x": 219,
        "y": 304
    },
    {
        "x": 343,
        "y": 302
    },
    {
        "x": 466,
        "y": 303
    },
    {
        "x": 580,
        "y": 314
    }
];
var blink = [
    {
      "x": 682,
      "y": 362
    },
    {
      "x": 613,
      "y": 383
    },
    {
      "x": 442,
      "y": 386
    },
    {
      "x": 353,
      "y": 385
    },
    {
      "x": 232,
      "y": 382
    },
    {
      "x": 112,
      "y": 380
    },
    {
      "x": 25,
      "y": 361
    },
    {
      "x": 57,
      "y": 346
    },
    {
      "x": 200,
      "y": 345
    },
    {
      "x": 306,
      "y": 346
    },
    {
      "x": 416,
      "y": 346
    },
    {
      "x": 604,
      "y": 354
    }
  ];
var happy = [
    {
        "x": 650,
        "y": 355
    },
    {
        "x": 556,
        "y": 307
    },
    {
        "x": 469,
        "y": 260
    },
    {
        "x": 363,
        "y": 242
    },
    {
        "x": 248,
        "y": 259
    },
    {
        "x": 133,
        "y": 313
    },
    {
        "x": 50,
        "y": 350.00000000000006
    },
    {
        "x": 90.19237886466834,
        "y": 200.00000000000009
    },
    {
        "x": 199.99999999999986,
        "y": 90.19237886466846
    },
    {
        "x": 349.99999999999994,
        "y": 50
    },
    {
        "x": 499.9999999999998,
        "y": 90.19237886466829
    },
    {
        "x": 609.8076211353315,
        "y": 199.99999999999986
    }
];

var sad = [
    {
        "x": 650,
        "y": 350
    },
    {
        "x": 609.8076211353316,
        "y": 500
    },
    {
        "x": 500,
        "y": 609.8076211353316
    },
    {
        "x": 350,
        "y": 650
    },
    {
        "x": 200.00000000000006,
        "y": 609.8076211353316
    },
    {
        "x": 90.19237886466846,
        "y": 500.0000000000001
    },
    {
        "x": 50,
        "y": 350.00000000000006
    },
    {
        "x": 163,
        "y": 298
    },
    {
        "x": 348,
        "y": 242
    },
    {
        "x": 466,
        "y": 189
    },
    {
        "x": 572,
        "y": 125
    },
    {
        "x": 629,
        "y": 202
    }
];
var angry = [
    {
      "x": 601,
      "y": 404
    },
    {
      "x": 592,
      "y": 448
    },
    {
      "x": 518,
      "y": 464
    },
    {
      "x": 415,
      "y": 467
    },
    {
      "x": 265,
      "y": 465
    },
    {
      "x": 102,
      "y": 440
    },
    {
      "x": 72,
      "y": 340
    },
    {
      "x": 88,
      "y": 244
    },
    {
      "x": 150,
      "y": 187
    },
    {
      "x": 315,
      "y": 230
    },
    {
      "x": 443,
      "y": 281
    },
    {
      "x": 574,
      "y": 346
    }
  ];
var numPoints = 12;
var radius = 250;
var xoffset = 350;
var yoffset = 350;
var circle = [];
for (var i = 0; i < numPoints; i++) {
    var angle = (Math.PI * 2) / numPoints * i;
    circle.push({ x: radius * Math.cos(angle) + xoffset, y: radius * Math.sin(angle) + yoffset });
}
var dilate = [
    {
      "x": 650,
      "y": 350
    },
    {
      "x": 627,
      "y": 507
    },
    {
      "x": 513,
      "y": 587
    },
    {
      "x": 352,
      "y": 609
    },
    {
      "x": 196,
      "y": 586
    },
    {
      "x": 73,
      "y": 510
    },
    {
      "x": 50,
      "y": 350.00000000000006
    },
    {
      "x": 74,
      "y": 200
    },
    {
      "x": 188,
      "y": 112
    },
    {
      "x": 351,
      "y": 76
    },
    {
      "x": 512,
      "y": 107
    },
    {
      "x": 622,
      "y": 194
    }
  ];
var states = [
    { "state": circle, "gains": [0.2, 0.05], "offsets" : [0, 0]},
    { "state": dilate, "gains": [0.03, 0.0], "offsets" : [0, 0]},
    // { "state": circle, "gains": [0.2, 0.05], "offsets" : [0, 0]},
    // { "state": happy, "gains": [0.3, 0.5], "offsets" : [0, -10]},
    // { "state": angry, "gains": [0.3, 0.3], "offsets" : [50, 30]},
];