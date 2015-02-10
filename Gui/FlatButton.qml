import QtQuick 2.3

Rectangle {
    id: root
    width: 144
    height: 144
    rotation: 0

    property int animationDuration: 100
    property string color_: "#9c27b0"
    property string caption_: "text"

    color: color_

    signal click()

    state: ""
    states: [
        State {
            name: "pushed"; when: mouseArea.pressed
            PropertyChanges { target: root; scale: 0.95; color: Qt.lighter(root.color_, 1.1) }
        },

        State {
            name: ""
            PropertyChanges { target: root; color: root.color_ }
        },

        State {
            name: "hover"; when:mouseArea.containsMouse
            PropertyChanges { target: root; color: Qt.lighter(root.color_, 1.1) }

        }

    ]

    transitions: [
        Transition {
            PropertyAnimation { target: root; properties: "color, rotation, scale, x, y"; duration: animationDuration; easing.type: Easing.InOutQuad; }
        }
    ]

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onClicked: click()
    }
}
