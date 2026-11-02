import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Popup {
    id: panel  // ID
    objectName: "panel"  // Object name
    property string className: "Panel"  // Class name
    property string baseClass: "Layout"  // Base class
    property string styleClass: "Panel"  // Style class
    property string baseStyle: "Panel"  // Base style

    Canvas {
        id: canvas
        objectName: "canvas"
    }
}
