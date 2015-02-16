import QtQuick 2.4
import Material 0.1

ApplicationWindow {
    title: qsTr("VK Remote Server")
    width: 500
    height: 500
    visible: true

    theme {
        accentColor: "#009688"
    }

    LogonPage{
        id: abr
        anchors.centerIn: parent
    }
    Component.onCompleted: {
         pageStack.push(Qt.resolvedUrl("LogonPage.qml"))
     }
}
