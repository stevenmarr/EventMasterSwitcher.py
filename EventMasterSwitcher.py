# EventMasterSwitcher Library for E2/S3

# Example:
#
#    import EventMasterSwitcher
#    d = EventMasterSwitcher.EventMasterSwitcher(ip="1.2.3.4")
#
#    r = d.listPresets()
#    if "err" in r: return r["humanized"]
#
#    print(r)

import requests
import json
from threading import Timer
from time import sleep
import socket
import xmltodict

class EventMasterSwitcher:

    global TESTPATTERNMODE_OFF
    global TESTPATTERNMODE_HRAMP
    global TESTPATTERNMODE_VRAMP
    global TESTPATTERNMODE_CBAR100
    global TESTPATTERNMODE_GRID16
    global TESTPATTERNMODE_GRID32
    global TESTPATTERNMODE_BURST
    global TESTPATTERNMODE_CBAR75
    global TESTPATTERNMODE_GRAY50
    global TESTPATTERNMODE_HSTEPS
    global TESTPATTERNMODE_VSTEPS
    global TESTPATTERNMODE_WHITE
    global TESTPATTERNMODE_BLACK
    global TESTPATTERNMODE_SMPTE
    global TESTPATTERNMODE_HALIGN
    global TESTPATTERNMODE_VALIGN
    global TESTPATTERNMODE_HVALIGN
    TESTPATTERNMODE_OFF = 0
    TESTPATTERNMODE_HRAMP = 1
    TESTPATTERNMODE_VRAMP = 2
    TESTPATTERNMODE_CBAR100 = 3
    TESTPATTERNMODE_GRID16 = 4
    TESTPATTERNMODE_GRID32 = 5
    TESTPATTERNMODE_BURST = 6
    TESTPATTERNMODE_CBAR75 = 7
    TESTPATTERNMODE_GRAY50 = 8
    TESTPATTERNMODE_HSTEPS = 9
    TESTPATTERNMODE_VSTEPS = 10
    TESTPATTERNMODE_WHITE = 11
    TESTPATTERNMODE_BLACK = 12
    TESTPATTERNMODE_SMPTE = 13
    TESTPATTERNMODE_HALIGN = 14
    TESTPATTERNMODE_VALIGN = 15
    TESTPATTERNMODE_HVALIGN = 16
    
    global VF_LIST
    VF_LIST = [{"Name": "1280x720p @50"},
               {"Name": "1280x720p @59.94"},
               {"Name": "1280x720p @60"},
               {"Name": "1920x1080p @50"},
               {"Name": "1920x1080p @59.94"},
               {"Name": "1920x1080p @60"}]
               
    ip = False
    discovered = {}
    sock_discovery = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fake_data = False


    ''' Internal Methods '''
    
    def __init__(self, ip=False):
        self.ip = ip
        self.discovered = {}
        self.version = None
        self.sock_discovery = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._netSendDiscoveryPacket()

    def _returnFakeDataForJSON(self, method, params={}):
        
        if method is "getFrameSettings":
            return {"jsonrpc":"2.0",
                    "result":{
                        "success":0,
                        "result":{
                            "System":{
                                "id":0,
                                "Name":"Demo_S3",
                                "FrameCollection":{
                                    "id":0,
                                    "Frame":
                                       {"id":"ff:ff:ff:ff:ff:ff",
                                       "Name":"Demo_S3",
                                       "Contact":"",
                                       "Version":"3.2.861",
                                       "OSVersion":"0.4.6",
                                       "FrameType":1,
                                       "FrameTypeName":"S3",
                                       "Enet":{"IP":"192.168.0.175","MacAddress":"ff:ff:ff:ff:ff:ff"},
                                       "SysCard":{
                                           "SlotState":2,
                                           "CardStatusID":2,
                                           "CardStatusLabel":"Ready",
                                           "CardTypeID":80,
                                           "CardTypeLabel":"System",
                                           "CardID":0},
                                       "Slot":[
                                           {"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":70,"CardTypeLabel":"Expansion","CardID":"Card0"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":50,"CardTypeLabel":"VPU Scaler","CardID":"Card1"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":50,"CardTypeLabel":"VPU Scaler","CardID":"Card2"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":1,"CardTypeLabel":"SDI Input","CardID":"Card3"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":2,"CardTypeLabel":"HDMI\/DP Input","CardID":"Card4"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":2,"CardTypeLabel":"HDMI\/DP Input","CardID":"Card5"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":21,"CardTypeLabel":"SDI Output","CardID":"Card6"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":22,"CardTypeLabel":"HDMI Output","CardID":"Card7"}},{"Card":{"CardStatusID":2,"CardStatusLabel":"Ready","CardTypeID":40,"CardTypeLabel":"MVR","CardID":"Card8"}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}},{"Card":{"CardStatusID":0,"CardStatusLabel":"Not Installed","CardTypeID":255,"CardTypeLabel":"Unknown","CardID":{}}}]}}}}},"id":0}
        
        if method is "listDestinations":
            return {"jsonrpc":"2.0","result":{"success":0,"response":{"ScreenDestination":[{"id":0,"Name":"LED","HSize":2160,"VSize":720,"Layers":6,"DestOutMapCol":{"DestOutMap":[{"id":0,"Name":"LED 1","HPos":0,"VPos":0,"HSize":1920,"VSize":1080,"FrzMode":0},{"id":1,"Name":"LED 2","HPos":1152,"VPos":0,"HSize":1920,"VSize":1080,"FrzMode":0}]}},{"id":1,"Name":"Content Submix","HSize":1920,"VSize":1080,"Layers":2,"DestOutMapCol":{"DestOutMap":[{"id":0,"Name":"Content Submix","HPos":0,"VPos":0,"HSize":1920,"VSize":1080,"FrzMode":0}]}}],"AuxDestination":[{"id":0,"AuxStreamMode":1,"Name":"FB CAM L"},{"id":1,"AuxStreamMode":1,"Name":"FB CAM R"},{"id":2,"AuxStreamMode":1,"Name":"PVW Mon Content"},{"id":3,"AuxStreamMode":1,"Name":"TIMER"}]}},"id":0}
 
        if method is "listContent" and params['id'] is 0:
            return {"jsonrpc":"2.0","result":{"success":0,"response":{"id":0,"Name":"LED","BGLyr":[{"id":0,"LastBGSourceIndex":11,"BGShowMatte":0,"BGColor":{"id":0,"Red":1023,"Green":131,"Blue":0}},{"id":1,"LastBGSourceIndex":11,"BGShowMatte":0,"BGColor":{"id":0,"Red":1023,"Green":131,"Blue":0}}],"Layers":[{"id":0,"LastSrcIdx":13,"PvwMode":1,"PgmMode":0,"Capacity":1,"PvwZOrder":0,"PgmZOrder":0,"Freeze":0,"Window":[{"HPos":39,"VPos":30,"HSize":850,"VSize":478},{"HPos":-194,"VPos":0,"HSize":889,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]},{"id":1,"LastSrcIdx":13,"PvwMode":0,"PgmMode":1,"Capacity":1,"PvwZOrder":0,"PgmZOrder":0,"Freeze":0,"Window":[{"HPos":39,"VPos":30,"HSize":850,"VSize":478},{"HPos":-194,"VPos":0,"HSize":889,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]},{"id":2,"LastSrcIdx":13,"PvwMode":1,"PgmMode":0,"Capacity":1,"PvwZOrder":2,"PgmZOrder":2,"Freeze":0,"Window":[{"HPos":1267,"VPos":30,"HSize":850,"VSize":478},{"HPos":-194,"VPos":0,"HSize":889,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]},{"id":3,"LastSrcIdx":13,"PvwMode":0,"PgmMode":1,"Capacity":1,"PvwZOrder":2,"PgmZOrder":2,"Freeze":0,"Window":[{"HPos":1267,"VPos":30,"HSize":850,"VSize":478},{"HPos":-194,"VPos":0,"HSize":889,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]},{"id":4,"LastSrcIdx":-1,"PvwMode":0,"PgmMode":0,"Capacity":1,"PvwZOrder":4,"PgmZOrder":4,"Freeze":0,"Window":[{"HPos":0,"VPos":0,"HSize":500,"VSize":500},{"HPos":0,"VPos":0,"HSize":500,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]},{"id":5,"LastSrcIdx":-1,"PvwMode":0,"PgmMode":0,"Capacity":1,"PvwZOrder":4,"PgmZOrder":4,"Freeze":0,"Window":[{"HPos":0,"VPos":0,"HSize":500,"VSize":500},{"HPos":0,"VPos":0,"HSize":500,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]}],"Transition":[{"id":0,"TransTime":30,"TransPos":0},{"id":1,"TransTime":30,"TransPos":0}]}},"id":0}
 
        if method is "listContent" and params['id'] is 1:
            return {"jsonrpc":"2.0","result":{"success":0,"response":{"id":1,"Name":"Content Submix","BGLyr":[{"id":0,"LastBGSourceIndex":-1,"BGShowMatte":1,"BGColor":{"id":0,"Red":0,"Green":0,"Blue":0}},{"id":1,"LastBGSourceIndex":-1,"BGShowMatte":1,"BGColor":{"id":0,"Red":0,"Green":0,"Blue":0}}],"Layers":[{"id":0,"LastSrcIdx":8,"PvwMode":0,"PgmMode":1,"Capacity":1,"PvwZOrder":0,"PgmZOrder":0,"Freeze":0,"Window":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":-194,"VPos":0,"HSize":889,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]},{"id":1,"LastSrcIdx":8,"PvwMode":1,"PgmMode":0,"Capacity":1,"PvwZOrder":0,"PgmZOrder":0,"Freeze":0,"Window":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":-194,"VPos":0,"HSize":889,"VSize":500}],"Source":[{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080},{"HPos":0,"VPos":0,"HSize":1920,"VSize":1080}],"Mask":[{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0},{"id":0,"Top":0,"Left":0,"Right":0,"Bottom":0}]}],"Transition":[{"id":0,"TransTime":30,"TransPos":0},{"id":1,"TransTime":30,"TransPos":0}]}},"id":0}
 
        if method is "listPresets":
            return {"jsonrpc":"2.0","result":{"success":0,"response":[{"id":0,"Name":"LED: PIP Content Mix","presetSno":1,"LockMode":0},{"id":1,"Name":"LED: Logo FS","presetSno":2,"LockMode":0},{"id":2,"Name":"Content: ATV","presetSno":3,"LockMode":0},{"id":3,"Name":"Content: PBP1","presetSno":4,"LockMode":0},{"id":4,"Name":"Content: PBP2","presetSno":5,"LockMode":0},{"id":5,"Name":"Content: Keynote1","presetSno":6,"LockMode":0},{"id":6,"Name":"Content: Keynote2","presetSno":7,"LockMode":0},{"id":7,"Name":"Content: Demo1","presetSno":8,"LockMode":0},{"id":8,"Name":"Content: Demo2","presetSno":9,"LockMode":0},{"id":9,"Name":"Content: PPT1","presetSno":10,"LockMode":0},{"id":10,"Name":"Content: PPT2","presetSno":11,"LockMode":0},{"id":11,"Name":"FB Right: Content","presetSno":12,"LockMode":0},{"id":12,"Name":"FB Right: Keynote 1 Notes","presetSno":13,"LockMode":0},{"id":13,"Name":"FB Right: Keynote 2 Notes","presetSno":14,"LockMode":0},{"id":14,"Name":"FB Right: Demo 2","presetSno":15,"LockMode":0},{"id":15,"Name":"FB Left: Content","presetSno":16,"LockMode":0},{"id":16,"Name":"FB Left: Keynote 1 Note","presetSno":17,"LockMode":0},{"id":17,"Name":"Timer: Timer","presetSno":18,"LockMode":0},{"id":18,"Name":"FB Left: Keynote 2 Note","presetSno":19,"LockMode":0},{"id":19,"Name":"FB Left: Demo 2","presetSno":20,"LockMode":0},{"id":20,"Name":"FB Left: Demo 1","presetSno":21,"LockMode":0},{"id":21,"Name":"FB Left: LOGO","presetSno":22,"LockMode":0},{"id":22,"Name":"FB Right: LOGO","presetSno":23,"LockMode":0},{"id":23,"Name":"FB Right: Demo 1","presetSno":24,"LockMode":0},{"id":24,"Name":"LED: Fullscreen","presetSno":25,"LockMode":0},{"id":25,"Name":"Preset26.00","presetSno":26,"LockMode":0},{"id":26,"Name":"FB: Content&amp;Notes","presetSno":27,"LockMode":0},{"id":27,"Name":"FB: Content Both","presetSno":28,"LockMode":0}]},"id":0}
 
        if method is "showPresetFile":
            return {"jsonrpc":"2.0","result":{"success":1,"response":{"PresetMgr":{"id":0,"ConflictMode":1,"ConflictPref":1,"TransTime":30,"LastRecall":-1,"Preset":{"id":1,"Name":"LED: Logo FS","LockMode":0,"presetSno":2,"ScreenDestCol":{"id":0,"ScreenDest":{"id":0,"IsActive":1,"FrameType":0,"CanvasOpMode":1,"CurrBGLyr":0,"Name":"LED","ToggleMode":0,"Live":0,"LockProgram":0,"HdcpMode":0,"CanvasMode":0,"CanvasInCfg":-1,"HSize":2160,"VSize":720,"HDimension":2,"VDimension":1,"BGLyr":{"id":1,"LastBGSourceIndex":11,"BGShowMatte":0,"Name":"BGStill-6","BGColor":{"id":0,"Red":1023,"Green":131,"Blue":0}},"Transition":[{"id":0,"TransTime":30,"TransPos":0,"TransCurve":1,"TransDelay":0,"ArmMode":1},{"id":1,"TransTime":30,"TransPos":0,"TransCurve":1,"TransDelay":0,"ArmMode":0}],"VideoFormat":{"id":0,"Name":"1920x1080p @50","HFreq":56250,"HSync":88,"HActive":1920,"HFP":528,"HTotal":2640,"VFreq":50,"VSync":5,"VActive":1080,"VFP":4,"VTotal":1125,"PixelClk":148.5,"HSP":80,"VSP":80,"AR":1.77778,"Interlaced":80,"VFType":8,"VFEnum":2706,"VFStdFrom":4,"VFStdNum":31},"DestOutMapCol":{"id":0,"DestOutMap":[{"id":0,"OutCfgIndex":0,"CanvasIndex":0,"HPos":0,"VPos":0,"Group":0},{"id":1,"OutCfgIndex":1,"CanvasIndex":0,"HPos":1152,"VPos":0,"Group":0}]},"LayerCollection":{"id":0,"Layer":[{"id":0,"PvwMode":0},{"id":1,"PvwMode":0},{"id":2,"PvwMode":0},{"id":3,"PvwMode":0},{"id":4,"PvwMode":0},{"id":5,"PvwMode":0}]},"MixerCollection":{"id":0,"Mixer":[{"id":0,"LayerAIndex":0,"SplitMode":0,"JoinMode":0,"ToggleMode":0,"linkLayers":0},{"id":1,"LayerAIndex":2,"SplitMode":0,"JoinMode":0,"ToggleMode":0,"linkLayers":0},{"id":2,"LayerAIndex":4,"SplitMode":0,"JoinMode":0,"ToggleMode":0,"linkLayers":0}]}}}}}}},"id":0}
 
        if method is "listDestinationsForPreset":
            return {"jsonrpc":"2.0","result":{"success":0,"response":{"id":params['id'],"Name":"LED: PIP Content Mix","LockMode":0,"presetSno":1,"ScreenDest":[{"id":0}],"AuxDest":[]}},"id":0}
 
        if method is "listSources":
            return {"jsonrpc":"2.0","result":{"success":0,"response":[{"id":0,"Name":"SDI1 PBP-1","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":0,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":1,"Name":"SDI2 ATV-2","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":1,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":4,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":2,"Name":"SDI3 TIMER-3","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":2,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":3,"Name":"SDI4-4","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":3,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":4,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":4,"Name":"Keynote 1-5","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":4,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":5,"Name":"Keynote 2-6","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":5,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":6,"Name":"Stage Demo 1-7","HSize":1280,"VSize":720,"SrcType":0,"InputCfgIndex":6,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":4,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":7,"Name":"Stage Demo 2-8","HSize":1280,"VSize":720,"SrcType":0,"InputCfgIndex":7,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":4,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":8,"Name":"PPT 1-9","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":8,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":9,"Name":"PPT 2-10","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":9,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":10,"Name":"Keynote 1 Notes-11","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":10,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":11,"Name":"Keynote 2 Notes-12","HSize":1920,"VSize":1080,"SrcType":0,"InputCfgIndex":11,"StillIndex":-1,"DestIndex":-1,"UserKeyIndex":-1,"InputCfgVideoStatus":1,"Mode3D":"No","Freeze":0,"Capacity":1},{"id":12,"Name":"LED","HSize":2160,"VSize":720,"SrcType":2,"InputCfgIndex":-1,"StillIndex":-1,"DestIndex":0,"UserKeyIndex":-1,"Freeze":0,"Capacity":2},{"id":13,"Name":"Content Submix","HSize":1920,"VSize":1080,"SrcType":2,"InputCfgIndex":-1,"StillIndex":-1,"DestIndex":1,"UserKeyIndex":-1,"Freeze":0,"Capacity":1},{"id":14,"Name":"LED Test Pattern-15","HSize":2160,"VSize":720,"SrcType":1,"InputCfgIndex":-1,"StillIndex":0,"DestIndex":-1,"UserKeyIndex":-1,"Freeze":0,"Capacity":2},{"id":15,"Name":"16x9 Logo-16","HSize":1920,"VSize":1080,"SrcType":1,"InputCfgIndex":-1,"StillIndex":1,"DestIndex":-1,"UserKeyIndex":-1,"Freeze":0,"Capacity":1},{"id":16,"Name":"FB Cam L Test Pattern-17","HSize":1920,"VSize":1080,"SrcType":1,"InputCfgIndex":-1,"StillIndex":2,"DestIndex":-1,"UserKeyIndex":-1,"Freeze":0,"Capacity":1},{"id":17,"Name":"FB Cam R Test Pattern-18","HSize":1920,"VSize":1080,"SrcType":1,"InputCfgIndex":-1,"StillIndex":3,"DestIndex":-1,"UserKeyIndex":-1,"Freeze":0,"Capacity":1}]},"id":0}
 
        if method is "listStill":
            return {"jsonrpc":"2.0","result":{"success":0,"response":[{"id":0,"Name":"LED Test Pattern","LockMode":0,"HSize":{"Min":0,"Max":99999,"$t":2160},"VSize":{"Min":0,"Max":99999,"$t":720},"StillState":{"Min":0,"Max":4,"$t":3},"PngState":{"Min":0,"Max":2,"$t":0},"FileSize":{"Min":0,"Max":100000,"$t":6998.4}},{"id":1,"Name":"16x9 Logo","LockMode":0,"HSize":{"Min":0,"Max":99999,"$t":1920},"VSize":{"Min":0,"Max":99999,"$t":1080},"StillState":{"Min":0,"Max":4,"$t":3},"PngState":{"Min":0,"Max":2,"$t":0},"FileSize":{"Min":0,"Max":100000,"$t":9331.2}},{"id":2,"Name":"FB Cam L Test Pattern","LockMode":0,"HSize":{"Min":0,"Max":99999,"$t":1920},"VSize":{"Min":0,"Max":99999,"$t":1080},"StillState":{"Min":0,"Max":4,"$t":3},"PngState":{"Min":0,"Max":2,"$t":0},"FileSize":{"Min":0,"Max":100000,"$t":9331.2}},{"id":3,"Name":"FB Cam R Test Pattern","LockMode":0,"HSize":{"Min":0,"Max":99999,"$t":1920},"VSize":{"Min":0,"Max":99999,"$t":1080},"StillState":{"Min":0,"Max":4,"$t":3},"PngState":{"Min":0,"Max":2,"$t":0},"FileSize":{"Min":0,"Max":100000,"$t":9331.2}}]},"id":0}
 
 
    def _net9999Request(self, method, params={}):
        if(self.fake_data):
            return self._returnFakeDataForJSON(method, params)
                    
        url = "http://{0!s}:9999/jsonrpc".format(self.ip)
        headers = {'content-type': 'application/json'}
        payload = {"method": method,
                   "params": params,
                   "jsonrpc": "2.0",
                   "id": 0}
        addr = (self.ip, 9999)
                    
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect(addr)
            
        except socket.error as msg:
            return {"error": "JSONRPC Connectivity Error: {0!s}".format(str(msg))}

        response = requests.post(url,
                                 data=json.dumps(payload),
                                 headers=headers)
        return_json = response.json()
        
        return return_json
        
    def _net9878Request(self, command):
        command_with_crlf = command + "\r\n"
        encoded_command = command_with_crlf.encode('utf-8')
        addr = (self.ip, 9878)
        sock_9878 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            sock_9878.connect(addr)
            
        except socket.error as msg:
            return {"err": True,
                    "humanized": "Error connecting to switcher {0!s}:{1!s}- {2!s}".format(addr[0], addr[1], msg)}
            
        try:
            sock_9878.send(encoded_command)
            print(encoded_command)
            print('sent')
        except socket.error as msg:
            print('err2')
            return {"error": "Error sending command to {0!s}:{1!s}- {2!s}".format(msg)}
            
        data = sock_9878.recv(1024)
        recieve_buffer = data.decode('utf-8')
            
        sock_9878.close()

        return recieve_buffer

    def _net9878Node(self, path, set=None):
        if set is None:
            request = "NODE -p {0!s}".format(path)
            print("Node Request Get")
        else:
            request = "NODE -p {0!s} -v {1!s}".format(path, set)
            print("Node Request Set")
        
        
        try:
            return_xml = self._net9878Request(request)
            return_json = xmltodict.parse(return_xml)
            return return_json
            
        except:
            return False

    def _net9876Request(self, xml):
        encoded_command = xml.encode('utf-8')
        addr = (self.ip, 9876)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(addr)
        except socket.error as msg:
            return {"error": "Error connecting to switcher {0!s}:{1!s}- {2!s}".format(addr[0], addr[1], msg)}

        try:
            sock.sendall(xml_full.encode('utf-8'))
        except socket.error as msg:
            return {"error": "Error sending command to {0!s}:{1!s}- {2!s}".format(msg)}

        # TODO: This should return the full buffer, not only 1024 bytes
        recieve_buffer = sock.recv(1024)
        sock.close()
        return recieve_buffer
        
    def _netSendDiscoveryPacket(self):
        encoded_command = "?\0".encode('UTF-8')
        addr = ('255.255.255.255', 40961)
        
        try:
            self.sock_discovery.setsockopt(socket.SOL_SOCKET,
                                           socket.SO_BROADCAST,
                                           1)
            self.sock_discovery.sendto(encoded_command, addr)
            Timer(1, self._netRecieveDiscovery).start()
        except socket.error as msg:
            return {"error": "Socket error during discovery: {0!s}".format(msg)}

    def _netRecieveDiscovery(self):
        """Loop to recieve and process incoming discovery messages"""
        while True:
            data, addr = self.sock_discovery.recvfrom(1024)
            if(data):
                decoded_data = data.decode('UTF-8')
                discovered_list = {}
                return_list = {}
                decoded_data_list = decoded_data.split("\0")
                
                for item in decoded_data_list:
                    if "=" in item:
                        key, value = item.split("=")
                        discovered_list[key] = value

                if("hostname" in discovered_list):
                    hostname_split = discovered_list["hostname"].split(":")
                    return_list['Name'] = hostname_split[0]
                    return_list['Port'] = hostname_split[1]
                    return_list['SystemName'] = hostname_split[2]
                    return_list['MACAddress'] = hostname_split[5]
                    return_list['OSVersion'] = hostname_split[6]

                if("type" in discovered_list):
                    return_list['Type'] = discovered_list['type']

                number_of_items = 0
                return_list['IP'] = addr[0]
                
                for key, value in self.discovered.items():
                    number_of_items += 1
                    if value['IP'] == return_list['IP']:
                        self.discovered[key] = return_list
                        return True

                self.discovered[number_of_items] = return_list
                return True


    ''' System Methods '''
    
    def getDiscoveredDevices(self):
        """ Get a dict of currently discovered devices """
        discovered_devices = self.discovered
        return discovered_devices
        
    def setFakeDataModeOn(self):
        self.fake_data = True

    def getFrameSettings(self):
        method = "getFrameSettings"
        return_json = self._net9999Request(method)
        print("{0!s}".format(return_json))
        if "error" not in return_json:
            self.version = return_json['result']['result']['System']['FrameCollection']['Frame']['Version']
        return return_json
        
    def getNativeRate(self):
        node = "/System/NativeRate"
        return_json = self._net9878Node(node)
        return return_json['System']['NativeRate']['#text']
        
    def setNativeRate(self, new_rate):
        node = "/System/NativeRate"
        self._net9878Node(node, set=new_rate)
        
    def doSave(self):
        command = "SAVE"
        self._net9878Request(command)
        
    def getInputEDID(self):
        
        edid_results = []
        i=0
        fs = self.getFrameSettings()
        for slot in fs['result']['result']['System']['FrameCollection']['Frame']['Slot']:
            if(slot['Card']['CardTypeID']==2):
                for j in range(0,3):
                    edid_results.append({"Slot": int(i+1), "Col": j, "EDID": "EDIDIN -s {0!s} -c {1!s}".format(int(i+1), j)})
            i+= 1
                
                
        #return self._net9878Request("EDIDIN -s {0!s} -c {1!s}".format(int(slot), int(col)))

    def setInputEDID(self, slot, col, edid_string):
        print("EDIDIN -s {0!s} -c {1!s} -f \"{2!s}\"".format(int(slot), int(col), edid_string))
        #return self._net9878Request("EDIDIN -s {0!s} -c {1!s}".format(int(slot), int(col)))

    def getOutputEDID(self, slot, col, edid_string):
        print("EDIDOUT -s {0!s} -c {1!s}".format(int(slot), int(col)))
        #return self._net9878Request("EDIDIN -s {0!s} -c {1!s}".format(int(slot), int(col)))

    ''' Stills Methods '''
    
    def getStills(self):
        method = "listStill"
        return_json = self._net9999Request(method)
        return return_json

    def doStillTake(self, source_id=None, still_id=None):
        method = "takeStill"
        params = {"type": 0,
                  "id": source_id}
        
        if still_id is not None:
            params["file"] = still_id
              
        if source_is is None: return False  
        return_json = self._net9999Request(method, params)
        return return_json

    def doStillDelete(self, still_id=None):
        method = "deleteStill"
        params = {"type": 0,
                  "id": still_id}
        
        if source_is is None: return False  
        return_json = self._net9999Request(method, params)
        return return_json


    ''' Destination Methods '''
    
    def doAuxDestinationChangeSourceOnPgm(self, aux_id=None, source_id=None):
        ''' Change Source $source_id onto AUX $aux_id on Program '''
        method = "changeAuxContent"
        params = {"id": aux_id,
                  "PgmLastSrcIndex": source_id}
                  
        if aux_id is None or source_id is None: return False

        return_json = self._net9999Request(method, params)
        print(return_json)
        return return_json
        
    def doAuxDestinationChangeSourceOnPvw(self, aux_id=None, source_id=None):
        ''' Change Source $source_id onto AUX $aux_id on Preview '''
        method = "changeAuxContent"
        params = {"id": aux_id,
                  "PvwLastSrcIndex": source_id}
                  
        if aux_id is None or source_id is None: return False

        return_json = self._net9999Request(method, params)
        print(return_json)
        return return_json      
        
    def getAuxDestinationSource(self, aux_id=None):
        ''' Get current source on AUX $aux_id on PVW and PGM '''
        method = "listAuxContent"
        params = {"id": aux_id}
                  
        if aux_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json  
        
    def doScreenDestinationChangeBackgroundSource(self, screen_id=None, source_id=None, matte=None):
        ''' Change Background $source_id onto Screen $screen_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        method = "changeContent"
        params = {"id": screen_id,
                  "BGLyr": [{"id": 0}, {"id": 1}]}
                         
        if matte is True:
            params["BGLyr"][0]["BGShowMatte"] = 1
            params["BGLyr"][1]["BGShowMatte"] = 1
         
        if matte is False:
            params["BGLyr"][0]["BGShowMatte"] = 0
            params["BGLyr"][1]["BGShowMatte"] = 0
             
        if source_id is not None:
            params["BGLyr"][0]["LastBGSourceIndex"] = source_id
            params["BGLyr"][1]["LastBGSourceIndex"] = source_id
             
        if screen_id is None or (source_id is None and matte is None): return False
        return_json = self._net9999Request(method, params)
        return return_json        
                
    def doScreenDestinationChangeBackgroundMatte(self, red=None, green=None, blue=None):
        ''' Change Background Matte Color $red $green $blue onto Screen $screen_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        method = "changeContent"
        params = {"id": screen_id,
                  "BGLyr": [{"id": 0,
                             "BGColor": source_id},
                            {"id": 1,
                             "LastBGSourceIndex": source_id}]}
         
        if screen_id is None or red is None or green is None or blue is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doScreenDestinationChangeLayerSource(self, screen_id=None, layer_id=None, source_id=None):
        ''' Change Layer $layer_id for Screen $screen_id to Source $source_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        # Does not support Split Mode. Should Check if in split mode
        # and not use absolute_layer_id!
        
        absolute_layer_id = layer_id * 2
        
        method = "changeContent"
        params = {"id": screen_id,
                  "Layers": [{"id": absolute_layer_id,
                              "LastSrcIdx": source_id},
                              {"id": absolute_layer_id+1,
                              "LastSrcIdx": source_id}]}
         
        if screen_id is None or layer_id is None or source_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json     
           
    def doScreenDestinationChangeLayerOuterWindow(self, screen_id=None, layer_id=None, 
                                                  hpos=None, vpos=None, hsize=None, 
                                                  vsize=None):
        ''' Change Layer OWIN $hpos $vpos $hsize $vsize for Screen $screen_id Layer $layer_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        # Does not support Split Mode. Should Check if in split mode
        # and not use absolute_layer_id!
        
        absolute_layer_id = layer_id * 2
        
        method = "changeContent"
        params = {"id": screen_id,
                  "Layers": [{"id": absolute_layer_id,
                              "Window": {}}, 
                             {"id": absolute_layer_id+1,
                              "Window": {}}]}
         
        if hpos is not None:
            params["Layers"][0]["Window"]["HPos"] = source_id
            params["Layers"][1]["Window"]["HPos"] = source_id
        
        if vpos is not None:
            params["Layers"][0]["Window"]["VPos"] = source_id
            params["Layers"][1]["Window"]["VPos"] = source_id
        
        if hsize is not None:
            params["Layers"][0]["Window"]["HSize"] = source_id
            params["Layers"][1]["Window"]["HSize"] = source_id
        
        if vsize is not None:
            params["Layers"][0]["Window"]["VSize"] = source_id
            params["Layers"][1]["Window"]["VSize"] = source_id
         
        if screen_id is None or layer_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json                           

    def doScreenDestinationChangeLayerInnerWindow(self, screen_id=None, layer_id=None, 
                                                  hpos=None, vpos=None, hsize=None, 
                                                  vsize=None):
        ''' Change Layer IWIN $hpos $vpos $hsize $vsize for Screen $screen_id Layer $layer_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        # Does not support Split Mode. Should Check if in split mode
        # and not use absolute_layer_id!
        
        absolute_layer_id = layer_id * 2
        
        method = "changeContent"
        params = {"id": screen_id,
                  "Layers": [{"id": absolute_layer_id,
                              "Source": {}}, 
                             {"id": absolute_layer_id+1,
                              "Source": {}}]}
         
        if hpos is not None:
            params["Layers"][0]["Source"]["HPos"] = source_id
            params["Layers"][1]["Source"]["HPos"] = source_id
        
        if vpos is not None:
            params["Layers"][0]["Source"]["VPos"] = source_id
            params["Layers"][1]["Source"]["VPos"] = source_id
        
        if hsize is not None:
            params["Layers"][0]["Source"]["HSizeI"] = source_id
            params["Layers"][1]["Source"]["HSize"] = source_id
        
        if vsize is not None:
            params["Layers"][0]["Source"]["VSize"] = source_id
            params["Layers"][1]["Source"]["VSize"] = source_id
         
        if screen_id is None or layer_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json                   
        
    def doScreenDestinationChangeLayerMask(self, screen_id=None, layer_id=None, 
                                                  left=None, right=None, top=None, 
                                                  bottom=None):
        ''' Change Layer Mask $left $right $top $bottom for Screen $screen_id Layer $layer_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        # Does not support Split Mode. Should Check if in split mode
        # and not use absolute_layer_id!
        
        absolute_layer_id = layer_id * 2
        
        method = "changeContent"
        params = {"id": screen_id,
                  "Layers": [{"id": absolute_layer_id,
                              "Mask": {}}, 
                             {"id": absolute_layer_id+1,
                              "Mask": {}}]}
         
        if top is not None:
            params["Layers"][0]["Mask"]["Top"] = source_id
            params["Layers"][1]["Mask"]["Top"] = source_id
        
        if bottom is not None:
            params["Layers"][0]["Mask"]["Bottom"] = source_id
            params["Layers"][1]["Mask"]["Bottom"] = source_id
        
        if left is not None:
            params["Layers"][0]["Mask"]["Left"] = source_id
            params["Layers"][1]["Mask"]["Left"] = source_id
        
        if right is not None:
            params["Layers"][0]["Mask"]["Right"] = source_id
            params["Layers"][1]["Mask"]["Right"] = source_id
         
        if screen_id is None or layer_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json      

    def doScreenDestinationLayerFreeze(self, screen_id=None, layer_id=None):
        ''' Enable Freeze for Screen $screen_id Layer $layer_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        # Does not support Split Mode. Should Check if in split mode
        # and not use absolute_layer_id!
        
        absolute_layer_id = layer_id * 2
        
        method = "changeContent"
        params = {"id": screen_id,
                  "Layers": [{"id": absolute_layer_id,
                              "Freeze": 1}, 
                             {"id": absolute_layer_id+1,
                              "Freeze": 1}]}
 
        if screen_id is None or layer_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json                                                                   

    def doScreenDestinationLayerUnfreeze(self, screen_id=None, layer_id=None):
        ''' Disable Freeze for Screen $screen_id Layer $layer_id '''
        # Switches on both PGM and PVW... change to check which layer is on PVW/PGM and
        # switch approprately.
        # Does not support Split Mode. Should Check if in split mode
        # and not use absolute_layer_id!
        
        absolute_layer_id = layer_id * 2
        
        method = "changeContent"
        params = {"id": screen_id,
                  "Layers": [{"id": absolute_layer_id,
                              "Freeze": 0}, 
                             {"id": absolute_layer_id+1,
                              "Freeze": 0}]}
 
        if screen_id is None or layer_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def getDestinations(self):
        ''' Get a list of all Screen Destinations '''
        method = "listDestinations"
        #params = {"type": 1}
        
        return_json = self._net9999Request(method)
        return return_json
        
    def doAuxDestinationFreeze(self, aux_id=None):
        ''' Enable Freeze on Aux Destination $aux_id '''
        method = "freezeDestSource"
        params = {"type": 3,
                  "id": aux_id,
                  "mode": 1}
                  
        if aux_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doAuxDestinationUnfreeze(self, aux_id=None):
        ''' Disable Freeze on Aux Destination $aux_id '''
        method = "freezeDestSource"
        params = {"type": 3,
                  "id": aux_id,
                  "mode": 0}
        if aux_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json
        
    def doScreenDestinationFreeze(self, screen_id=None):
        ''' Enable Freeze on Screen Destination $screen_id '''
        method = "freezeDestSource"
        params = {"type": 2,
                  "id": screen_id,
                  "screengroup": 0,
                  "mode": 1}
        
        if screen_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doScreenDestinationUnfreeze(self, screen_id=None):
        ''' Disable Freeze on Screen Destination $screen_id '''
        method = "freezeDestSource"
        params = {"type": 2,
                  "id": id,
                  "screengroup": 0,
                  "mode": 0}
        
        if screen_id is None: return False          
        return_json = self._net9999Request(method, params)
        return return_json
        
        
    ''' Source Methods '''
    
    def getInputs(self):
        ''' Get all Input Sources '''
        method = "listSources"
        params = {"type": 0}
        return_json = self._net9999Request(method, params)
        return return_json

    def getBackgrounds(self):
        ''' Get all Background Sources '''
        method = "listSources"
        params = {"type": 1}
        return_json = self._net9999Request(method, params)
        return return_json        

    def getAllSources(self):
        ''' Get all Sources '''
        method = "listSources"
        return_json = self._net9999Request(method)
        return return_json        

    def doInputFreezeToggle(self, input_id=None):
        inputs = self.getInputs()
        if "error" in inputs:
            return inputs
        
        if inputs['result']['response'] is not list:
            return {}
            
        for input in inputs['result']['response']:
            if input['id'] is input_id:
                if input['Freeze']:
                    return self.doInputUnfreeze(input_id)
                else:
                    return self.doInputFreeze(input_id)

    def doInputFreeze(self, input_id=None):
        ''' Enable Freeze on Input Source $input_id '''
        method = "freezeDestSource"
        params = {"type": 0,
                  "id": input_id,
                  "mode": 1}
       
        if input_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doInputUnfreeze(self, input_id=None):
        ''' Disable Freeze On Input Source $input_id '''
        method = "freezeDestSource"
        params = {"type": 0,
                  "id": input_id,
                  "mode": 0}
                  
        if input_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json
        
    def doBackgroundFreezeToggle(self, background_id=None):
    
        if background_id is None:
            return
        
        backgrounds = self.getBackgrounds()
        if "error" in backgrounds:
            return backgrounds
        
        if backgrounds['result']['response'] is not list:
            return {}
            
        for background in backgrounds['result']['response']:
            if background['id'] is background_id:
                if background['Freeze']:
                    return self.doBackgroundUnfreeze(background_id)
                else:
                    return self.doBackgroundFreeze(background_id)

    def doBackgroundFreeze(self, background_id=None):
        ''' Enable Freeze On Background Source $background_id '''
        method = "freezeDestSource"
        params = {"type": 1,
                  "id": background_id,
                  "mode": 1}
 
        if background_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doBackgroundUnfreeze(self, background_id=None):
        ''' Disable Freeze On Background Source $background_id '''
        method = "freezeDestSource"
        params = {"type": 1,
                  "id": background_id,
                  "mode": 0}
                  
        if background_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json


    ''' Transition Methods '''
    
    def doTransitionAuto(self, frames=None):
        '''Do a transition at the currently set transition time.'''
        # TODO: If unit firmware is v4 or later, use JSONRPC command for this.
        cmd = "ATRN"
        if frames is not None:
            cmd += " {0!s}".format(frames)
            
        print(cmd)
            
        return_cmd = self._net9878Request(cmd)
        return return_cmd

    def doTransitionCut(self):
        '''Do a transition for 0 seconds (cut)'''
        # TODO: If unit firmware is v4 or later, use JSONRPC command for this.
        cmd = "ATRN 0"
        return_cmd = self._net9878Request(cmd)
        return return_cmd


    ''' Preset Methods '''
    
    def getPresets(self):
        method = "listPresets"
        ''' Return a list of all Presets '''
        return_json = self._net9999Request(method)
        return return_json
        
    def getPresetsForAuxDest(self, aux_id=None):
        ''' Return a list of all presets on Aux Destination $aux_dest_id '''
        method = "listPresets"
        params = {"AuxDest": aux_id}
        if aux_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def getPresetsForScreenDest(self, screen_id=None):
        ''' Return a list of all presets on Screen Destination $screen_dest_id '''
        method = "listPresets"
        params = {"ScreenDest": screen_id}
        if screen_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doPresetRename(self, preset_id=None, name=None):
        ''' Rename Preset $preset_id to $new_preset_name '''
        method = "renamePreset"
        params = {"id": preset_id,
                  "Name": name}
        if preset_id is None or name is None: return False
        return_cmd = self._net9999Request(method, params)
        return return_cmd
        
    def doPresetDelete(self, preset_id=None):
        ''' Delete Preset $preset_id '''
        method = "deletePreset"
        params = {"id": preset_id}
        
        if preset_id is None: return False
        return_cmd = self._net9999Request(method, params)
        return return_cmd
         
    def doPresetActivateToPVW(self, preset_id=None):
        method = "activatePreset"
        params = {"id": preset_id,
                  "type": 0}
                  
        if preset_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json

    def doPresetActivateToPGM(self, preset_id=None):
        method = "activatePreset"
        params = {"id": preset_id,
                  "type": 1}
                  
        if preset_id is None: return False
        return_json = self._net9999Request(method, params)
        return return_json
        
        
    ''' Console Layout Methods '''

    '''def getConsoleLayout(self, layout_id=None):
        # TODO: Convert XML node to JSON and return
        node = "/System/ConsoleLayoutMgr/ConsoleLayout[@id={0!s}]/*".format(layout_id)
        if layout_id is None: return False
        return_node = self._net9878Node(node)
        
        return return_node

    def getPresetMgrNode(self):
        node = "System[@id=0]/PresetMgr[@id=0]/"
        return_node = self._net9878Node(node)
        for 
        return return_node'''
        

    ''' Output Methods '''
    
    def setScreenDestTestPattern(self, destination_id=None, testpattern_id=99):
        # Step 1: Get OutputCfg ids for the destination
        
        if destination_id is None:
            return False
            
        outputcfg_ids = []

        for i in range(0,99):
            node = "/System/DestMgr/ScreenDestCol/ScreenDest[@id={0!s}]/DestOutMapCol/DestOutMap[@id={1!s}]/OutCfgIndex".format(destination_id, i)
            return_json = self._net9878Node(node)
            if return_json is False:
                break
            else:
                outputcfg_ids.append(return_json['System']['DestMgr']['ScreenDestCol']['ScreenDest']['DestOutMapCol']['DestOutMap']['OutCfgIndex']['#text'])
            
        if testpattern_id is 99: 
            return False
            
        for outputcfg_id in outputcfg_ids:
            node = "/System/OutCfgMgr/OutputCfg[@id={0!s}]/OutputAOI/TestPattern/TestPatternMode".format(outputcfg_id)
            self._net9878Node(node, set=testpattern_id)
            
        return True
        
    def setAuxDestTestPattern(self, destination_id=None, testpattern_id=99):
        # Step 1: Get OutputCfg ids for the destination
        
        if destination_id is None:
            return False
            
        outputcfg_id = None

        node = "/System/DestMgr/AuxDestCol/AuxDest[@id={0!s}]/OutCfgIndex".format(destination_id)
        return_json = self._net9878Node(node)
        
        if return_json is False:
            return
            
        outputcfg_id = return_json['System']['DestMgr']['AuxDestCol']['AuxDest']['OutCfgIndex']['#text']
            
        if testpattern_id is 99: 
            return False
            
        node = "/System/OutCfgMgr/OutputCfg[@id={0!s}]/OutputAOI/TestPattern/TestPatternMode".format(outputcfg_id)
        self._net9878Node(node, set=testpattern_id)
            
        return True
     
        
                
    #def setOutputDiagMotion(self, output_id=None, diagmotion=None):
    #    ''' Set a test pattern with ID $testpattern_id for output $output_id '''""
    #    node = "System/OutCfgMgr/OutputCfg[@id={0!s}]/TestPattern/TestPattern".format(output_id)
    ##    
    #    if output_id is None or diagmotion is None: return False
    #    return_node = self._net9878Node(node, diagmotion)
    #    return return_node
        
    def getHelp(self):
        return self._net9878Request("HELP")
        

