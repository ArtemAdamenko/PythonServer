# -*- coding: utf-8 -*-

import time
import datetime
#-------------------------------------------------------------------------------
global PKG_ANSWER_TYPE


PKG_UNKNOWN                 =   -1
PKG_PUT_COORD               =   0
PKG_PUT_MESSAGE             =   1
PKG_PUT_MSG_ANSWER          =   2
PKG_COUNT_SUPPORT_TYPES     =   3

PKG_ANSWER_TYPE = PKG_UNKNOWN;

TemplatePackageAnswer = list(range(PKG_COUNT_SUPPORT_TYPES))

#-------------------------------------------------------------------------------
AnswerHeader  = "HTTP/1.1 200 OK\r\n"
AnswerHeader += "Server: CDS\r\n"
AnswerHeader += "Content-Type: text/xml\r\n"
#-------------------------------------------------------------------------------
TemplatePackageAnswer[PKG_PUT_COORD] = "<?xml version=\"1.0\" encoding=\"windows-1251\"?>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "<soapenv:Envelope xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope\">\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "<soapenv:Header/>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "<soapenv:Body>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "<ws:PutCoordResponse>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "<ObjectID>%s</ObjectID>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "</ws:PutCoordResponse>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "</soapenv:Body>\r\n"
TemplatePackageAnswer[PKG_PUT_COORD] += "</soapenv:Envelope>\r"
#-------------------------------------------------------------------------------
TemplatePackageAnswer[PKG_PUT_MESSAGE] = '<?xml version="1.0" encoding="windows-1251"?>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='<soapenv:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope">\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='<soapenv:Header/>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='<soapenv:Body>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='<ws:PutMessageResponse>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='<ObjectID>%d</ObjectID>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='</ws:PutMessageResponse>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='</soapenv:Body>\r\n'
TemplatePackageAnswer[PKG_PUT_MESSAGE] +='</soapenv:Envelope>\r'
#-------------------------------------------------------------------------------
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] = '<?xml version="1.0" encoding="windows-1251"?>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='<soapenv:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope">\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='<soapenv:Header/>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='<soapenv:Body>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='<ws:PutMsgAnswerResponse>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='<ObjectID>%d</ObjectID>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='<MessageID>0</MessageID>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='</ws:PutMsgAnswerResponse>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='</soapenv:Body>\r\n'
TemplatePackageAnswer[PKG_PUT_MSG_ANSWER] +='</soapenv:Envelope>\r'
#-------------------------------------------------------------------------------

class TNBlock():
    
    Number = None
    LastTime = None
    LastPoint = None
    Speed  = 0.0
    CountRecivedPackaged = 0
    CountCommitErrors = 0
    state = False
    
    LastUpdateTime = datetime.datetime.fromtimestamp(time.mktime(time.strptime("2012-01-01 0:0:0","%Y-%m-%d %H:%M:%S")))
    LastCommitTime = datetime.datetime.fromtimestamp(time.mktime(time.strptime("2012-01-01 0:0:0","%Y-%m-%d %H:%M:%S")))
    
    def __init__(self, _Number, _LastTime = None, _LastLon = None, _LastLat = None, _LastSpeed = None):
        self.Number = _Number
        self.LastPoint = TGeoCoors()
        if _LastTime    != None and _LastLon != None and _LastLat != None:
            self.Update(_LastTime, _LastLon, _LastLat, _LastSpeed)
              
        CountRecivedPackaged = 0
        
    def Update(self, _LastTime, _LastLon, _LastLat, _LastSpeed):
        self.LastTime = _LastTime
        self.LastPoint.LON = _LastLon
        self.LastPoint.LAT = _LastLat
        self.Speed = _LastSpeed
        self.CountRecivedPackaged+=1
        self.LastUpdateTime = datetime.datetime.now()
        self.state = True


#-------------------------------------------------------------------------------


