import QtQuick 2.4
import Material 0.1

Item {
    Column {
        id: tabLogon
        anchors.centerIn: parent
        spacing: units.dp(20)


        MySlider {
            id: songSlider
            manualText: true
            width: units.dp(400)
            numericValueLabel: true
            stepSize: 1
            minimumValue: 0
            maximumValue: 360

            onValueChanged: {
                songSlider.knobText = ((value - value%60) / 60) + ":" + (value%60)
            }

            MouseArea{
                id: mouseArea
                propagateComposedEvents: true
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {songSlider.forceActiveFocus(); }
                onExited: {songSlider.focus = false; }
                onClicked: {mouse.accepted = false}
                onPositionChanged: {mouse.accepted = false}
                onPressAndHold: {mouse.accepted = false}
                onPressed: {mouse.accepted = false}
                onReleased: {mouse.accepted = false}
            }
            Component.onCompleted: {songSlider.knobText = "0:0"}
        }

        Button {
            id: playButton
            width: units.dp(85)
            height: width
            elevation: 1
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: { playAnim.switchState() }
            PlayAnim{
                id: playAnim
                anchors.centerIn: playButton
                scale: 0.5
            }

        }
        Connections {
            target: guiController
            onNewSong: { info = reason; tabLogon.switchState(); }
        }
    }
}
