import QtQuick 2.0
import Material 0.1

Item {
    id: root
    property alias info: infoLabel.text
    Column {
        id: tabLogon
        anchors.centerIn: parent
        spacing: units.dp(20)

        TextField {
            id: loginField
            placeholderText: "E-mail"
            floatingLabel: true

            anchors.horizontalCenter: parent.horizontalCenter
        }

        TextField {
            id: passwordField
            placeholderText: "Password"
            floatingLabel: true

            input.echoMode: TextInput.Password

            anchors.horizontalCenter: parent.horizontalCenter
        }

        function switchState()
        {
            state = state === "connecting" ? "" : "connecting";
            connectButton.visible = !connectButton.visible
        }

        Button {
            id: connectButton
            text: "Connect"
            elevation: 1
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {guiController.connect(loginField.text, passwordField.text); infoLabel.text = ""; tabLogon.switchState();}
        }
        Label {
            id: infoLabel
            text: ""
            color: Theme.light.textColor
        }
        states: [
            State {
                name: "connecting"
                PropertyChanges{ target: loginField; enabled: false }
                PropertyChanges{ target: passwordField; enabled: false }
                PropertyChanges{ target: connectButton; enabled: false }
            }

        ]
    }
    Connections {
        target: guiController
        onDisc: { info = reason; tabLogon.switchState(); }
    }
}
