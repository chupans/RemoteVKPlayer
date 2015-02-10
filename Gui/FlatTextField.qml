import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

TextField {
    id: root
    width: 200
    height: 30

    style: TextFieldStyle {
        textColor: "black"
        font {
            family: "Segoe UI"
            pixelSize: 16
        }
        background: Rectangle {
            radius: 0
            border.width: 0
        }
    }
}

