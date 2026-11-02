import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Layouts 1.15


Button {
    id: button  // ID
    objectName: "button"  // Object name
    property string className: "Button"  // Class name
    property string baseClass: "Element"  // Base class
    property string styleClass: "Button"  // Style class
    property string baseStyle: "Button"  // Base style
    
    property color borderColor: "#555"
    property color backgroundColor: "#444"
    property alias iconSource: icon.source
    property bool isHovered: false
    property bool hasIcon: iconSource !== ""

    hoverEnabled: true
    checkable: false
    checked: false

    contentItem: Item {
        anchors.fill: parent

        Row {
            id: row
            spacing: 8
            anchors.centerIn: parent  // Center content

            Image {
                id: icon
                objectName: "icon"
                source: ""
                visible: icon.source !== ""
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                id: text
                objectName: "text"
                text: button.text
                color: "#ccc"
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    background: Rectangle {
        id: background
        objectName: "background"

        property color backgroundColor: "#444"
        color: background.backgroundColor

        property color borderColor: "#444"
        border.color: background.borderColor

        border.width: 1
        radius: 6
    }

}
