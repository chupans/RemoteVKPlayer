import QtQuick 2.4
import Material 0.1

ApplicationWindow {
    id: main
    width: 500
    height: 500
    visible: true

    property var pages: ["LogonPage.qml", "PlayerPage.qml"]
    property string selectedPage: pages[0]

    function connected(){}
    signal disconnected(string reason)
    onDisconnected: { abr.info = reason}

    property alias abr: page.item

    Loader {
        id: page
        anchors.centerIn: parent
        source: Qt.resolvedUrl(selectedPage)
        asynchronous: true
    }
    Connections {
        target: page.item
        onConnected: { selectedPage = pages[1]}
    }
    Component.onCompleted: { disconnected("asdasd")}
}
