import xbmc
import xbmcgui
import xbmcaddon

import vera

import controlid 
import controlid.room

__addon__   = xbmcaddon.Addon()
__cwd__     = __addon__.getAddonInfo('path')

class GUI( xbmcgui.WindowXMLDialog ):
    def __init__(self, *args, **kwargs):
        self.buttonIDToRoom = {}

    def onInit(self):
        self.hideRooms()
        self.updateVera()

    def onClick(self, controlID):
        if      controlID == controlid.SETTINGS:
            __addon__.openSettings()
            self.updateVera()
        elif    controlID == controlid.GET_DATA:
            self.vera.getData()
            self.updateRooms()
        elif    controlID == controlid.EXIT:
            self.close()
        elif    controlID in self.buttonIDToRoom.keys():
            room_ = self.buttonIDToRoom[controlID]
            roomUI = RoomUI(
                    'room.xml', __cwd__, 'Default',
                    vera=self.vera, room=room_) 
            roomUI.doModal()
            del roomUI
        elif    controlID == controlid.ROOM_NONE:
            roomUI = RoomUI(
                    'room.xml', __cwd__, 'Default',
                    vera=self.vera, room=None) 
            roomUI.doModal()
            del roomUI


    def updateRooms(self):
        rooms = self.vera.data['rooms']
        
        self.showLabel(controlid.ROOM_NONE, '(other devices and scenes)')

        controlID = controlid.ROOM_FIRST
        for room in rooms:
            self.showLabel(controlID, room['name'])
            self.buttonIDToRoom[controlID] = room
            controlID += 1

        self.hideRooms(controlID)

    def showLabel(self, controlID, label):
        control = self.getControl(controlID)
        control.setVisible(True)
        control.setLabel(label)

    def hideRooms(self, first=controlid.ROOM_FIRST):
        for controlID in range(first, controlid.ROOM_LAST + 1):
            button = self.getControl(controlID)
            button.setVisible(False)

    def updateVera(self):
        self.vera = vera.Controller(__addon__.getSetting('controller_address'))


class RoomUI( xbmcgui.WindowXMLDialog ):
    def __init__(self, *args, **kwargs):
        self.room = kwargs['room']
        self.vera = kwargs['vera']

    def onInit(self):
        self.hideDevices()
        label = self.getControl(10101)
        if self.room:
            label.setLabel(self.room['name'])
        else:
            label.setLabel('Devices not in any room')
        self.updateDevices()

    def onClick(self, controlID):
        pass

    def updateDevices(self):
        devices = self.vera.data['devices']

        controlID = controlid.room.DEVICE_FIRST
        for device in devices:
            if self.room:
                if device['room'] == self.room['id'] :
                    self.showLabel(controlID, device['name'])
                    controlID += 1
            else:
                if device['room'] == 0:
                    self.showLabel(controlID, device['name'])
                    controlID += 1

        #self.hideDevices(controlID)

    def showLabel(self, controlID, label): # TODO: DRY
        control = self.getControl(controlID)
        control.setVisible(True)
        control.setLabel(label)

    def hideDevices(self, first=controlid.room.DEVICE_FIRST):
        for controlID in range(first, controlid.room.DEVICE_LAST + 1):
            button = self.getControl(controlID)
            button.setVisible(False)




