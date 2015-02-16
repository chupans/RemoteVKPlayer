import QtQuick 2.0


Item {
  id: root
  width: 72
  height: 72
  property int default_width:24

  Rectangle {
    id: bar1
    color: "black"
    transformOrigin: Item.Center
    antialiasing: true
  }

  Rectangle {
    id: bar2
    color: "black"
    antialiasing: true
  }
  Canvas {
      id:canvas
      width:72
      height:72
      antialiasing: true

      property string strokeStyle:"black"
      property string fillStyle:"black"
      property int lineWidth:1
      property bool fill:true
      property bool stroke:true
      property real alpha:1.0

      onPaint: {
          var ctx = canvas.getContext('2d');
          ctx.save();
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.globalAlpha = canvas.alpha;
          ctx.strokeStyle = canvas.strokeStyle;
          ctx.fillStyle = canvas.fillStyle;
          ctx.lineWidth = canvas.lineWidth;
          ctx.scale(1, 1);
          ctx.rotate(canvas.rotate);
          ctx.beginPath();
          ctx.moveTo(0,0);
          ctx.lineTo(root.width,root.width/2)
          ctx.lineTo(0,root.height)
          ctx.lineTo(0,0)
          ctx.closePath();
          if (canvas.fill)
             ctx.fill();
          if (canvas.stroke)
             ctx.stroke();
          ctx.restore();
          }
   }
  onScaleChanged: { canvas.requestPaint() }

  property int animationDuration: 350

  function switchState()
  {
      state = state === "play" ? "pause" : "play"
  }

  state: "play"
  states: [
      State {
          name: "play"

      PropertyChanges {
          target: bar1
          x: 24
          y: -5
          width: 12
          height: 60
          rotation: -60
      }

      PropertyChanges {
          target: bar2
          x: 24
          y: 18
          width: 12
          height: 60
          rotation: 60
      }

      PropertyChanges {
          target: canvas
          x: 0
          y: 0
      }
      },

    State {
      name: "pause"
      PropertyChanges { target: root; rotation: 180}
      PropertyChanges { target: bar1; rotation: 0; x: 18; y: 9; width: 12; height: 54 }
      PropertyChanges { target: bar2; rotation: 0; x: 42; y: 9; width: 12; height: 54 }
      PropertyChanges { target: canvas; opacity: 0.0 }
      }
  ]

  transitions: [
    Transition {
      RotationAnimation { target: root; direction: RotationAnimation.Clockwise; duration: animationDuration; easing.type: Easing.InOutQuad }
      PropertyAnimation { target: bar1; properties: "rotation, width, height, x, y"; duration: animationDuration; easing.type: Easing.InOutQuad }
      PropertyAnimation { target: bar2; properties: "rotation, width, height, x, y"; duration: animationDuration; easing.type: Easing.InOutQuad }
      PropertyAnimation { target: canvas; properties: "opacity, width, height, x, y"; duration: animationDuration; easing.type: Easing.InOutExpo }
    }
  ]
}
