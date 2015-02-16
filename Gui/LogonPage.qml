import QtQuick 2.0
import Material 0.1

Page {
    id: page

    tabs: [
        // Each tab can have text and an icon
        {
            text: "Overview",
            icon: "action/home"
        },

        // You can also leave out the icon
        {
            text:"Projects",
        },

        // Or just simply use a string
        "Inbox"
    ]

    TabView {
        id: tabView
        anchors.fill: parent
        currentIndex: 0
        model: tabs
    }

    VisualItemModel {
        id: tabs
        Rectangle{
            width: tabView.width
            height: tabView.height
            color: "#C3FFAF"
            Column {
                id: tabLogon
                anchors.centerIn: parent
                spacing: units.dp(20)

                TextField {
                    placeholderText: "E-mail"
                    floatingLabel: true
                    helperText: "Enter your e-mail"

                    anchors.horizontalCenter: parent.horizontalCenter
                }

                TextField {
                    placeholderText: "Password"
                    floatingLabel: true

                    input.echoMode: TextInput.Password

                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Button {
                    text: "Connect"
                    elevation: 1
                    anchors.horizontalCenter: parent.horizontalCenter
                    onClicked: tabView.incrementCurrentIndex()
                }
            }
        }
        Rectangle{
            width: tabView.width
            height: tabView.height
            Column {
                id: tabPlayer
                anchors.centerIn: parent
                spacing: units.dp(20)
                Button {
                    width: 144
                    height: 144
                    id: playButton
                    elevation: 1
                    anchors.horizontalCenter: parent.horizontalCenter
                    PlayAnim{
                        id: playAnim
                        anchors.centerIn: parent
                    }
                    onClicked: {
                        tabView.incrementCurrentIndex()
                        playAnim.switchState()
                    }
                }

            }
        }
    }
}
