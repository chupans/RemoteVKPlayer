import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2

ApplicationWindow {
    title: qsTr("Sudoku")
    width: 500
    height: 500
    visible: true
    style: ApplicationWindowStyle {
            background: Rectangle {
                color: "#eeeeee"
            }
    }

    Item{
        width: parent.width
        height: parent.height
        anchors.centerIn: parent
        id: controls

        Column{
            anchors.centerIn: parent
            spacing: 10
            Text{
                anchors.centerIn: parent.center
                clip: true
                id: login_info
                text: "E-mail"
                color: "black"
                font {
                    family: "Segoe UI"
                    pixelSize: 20
                }
            }

            FlatTextField {
                id: username
                //placeholderText: login_info.text
            }

            Text{
                anchors.centerIn: parent.center
                id: pass_info
                text: "Password"
                color: "black"
                font {
                    family: "Segoe UI"
                    pixelSize: 20
                }
            }
            FlatTextField {
                id: pass
                //placeholderText: "Password"
                Keys.onReturnPressed: {
                    controls.state = "run"
                }
            }
            FlatButton {
                id: go
                width: 200
                height: 40
                anchors.centerIn: parent.center
                Text {
                    anchors.centerIn: parent
                    text: "Go"
                    color: "white"
                    font {
                        family: "Segoe UI"
                        pixelSize: 20
                    }
                }
                color_: "#20aeff"
                onClick: controls.state = "run"
            }

        }
        FlatButton {
            id: playButton
            color_: "#20aeff"
            anchors.centerIn: parent
            PlayAnim {
                id: playAnim
                anchors.centerIn: parent
            }
            Connections{
                target: playButton.mouseArea
                onClick: playAnim.switchState()
            }

        }
        state: "log"
        states: [
            State {
                name: "log"
                PropertyChanges {target: username; visible: true}
                PropertyChanges {target: pass; visible: true}
                PropertyChanges {target: login_info; visible: true}
                PropertyChanges {target: pass_info; visible: true}
                PropertyChanges {target: playButton; visible: false}
            },
            State {
                name: "run"
                PropertyChanges {target: username; visible: false}
                PropertyChanges {target: pass; visible: false}
                PropertyChanges {target: login_info; visible: false}
                PropertyChanges {target: pass_info; visible: false}
                PropertyChanges {target: playButton; visible: true}
            }
        ]
    }
}
