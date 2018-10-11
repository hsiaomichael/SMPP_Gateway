import sys,string
import PCA_GenLib
import struct

######################################################## 
## SMPP PDU Message Reader
##  
########################################################
class SMPP_PDU_Reader:
    def __init__(self,command_length,Message):    
        try:    
            
            Msg = "Init SMPP_PDU_Reader ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            self.SMPP_command_length = command_length
            self.command_id = Message[0:4]    
            self.command_status = Message[4:8]    
            self.sequence_number = struct.unpack("!i",Message[8:12])[0]
            self.Message = Message    
    
        except :
            Msg = "SMPP_PDU_Reader Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise
            
    def CheckStatus(self):
        try:            
            Msg = "CheckStatus ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            Status = struct.unpack("!i",self.command_status)[0]
            
            if (Status == 0):
                Msg = "**Command Success**"
                PCA_GenLib.WriteLog(Msg,2)
            else:
                Msg = "**Command Error** .. <%s>" % Status
                PCA_GenLib.WriteLog(Msg,2)
            
            Msg = "CheckStatus Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            return Status
        except :
            Msg = "CheckStatus error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise
            
    def GetCommandID(self):
        try:        
            Msg = "GetCommandID ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            
            Msg = "GetCommandID Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            return self.command_id
        except :
            Msg = "GetCommandID error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise    
    

########################################################    
## SMPP PDU Message Writer    ##
##    ##
########################################################
class SMPP_PDU_Writer:
    
    
    def __init__(self,sequence_number):        
        try:        
            Msg = "Init SMPP_PDU_Writer ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            self.command_length = struct.pack('!i',0)
            self.sequence_number = sequence_number
            self.command_status = struct.pack('!i',0)
            
            Msg = "Init SMPP_PDU_Writer Ok"
            PCA_GenLib.WriteLog(Msg,9)
        except :
            Msg = "SMPP_PDU_Writer Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)        
            raise
            
    def GetNextSequenceNo(self):
        try:        
            Msg = "GetNextSequenceNo .."
            PCA_GenLib.WriteLog(Msg,9)        
            
            self.sequence_number = self.sequence_number + 1
            
            Msg = "GetNextSequenceNo Ok"
            PCA_GenLib.WriteLog(Msg,9)    
        except :
            Msg = "GetNextSequenceNo Error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise
            
    def ConstructHeader(self,command_id):
        try:    
            Msg = "Init ConstructHeader ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            self.command_id = command_id
            #self.GetNextSequenceNo()
            self.sequence_no = struct.pack("!I",self.sequence_number)
            
            # [command id][command status][sequence number][Reserved field]
            #   ineger 4       4                4              4
            
            self.Message = self.command_id + self.command_status + self.sequence_no
            
            Msg = "ConstructHeader Ok"
            PCA_GenLib.WriteLog(Msg,9)
        except :
            Msg = "ConstructHeader  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)            
            raise
            
        
    def ConstructStatus(self,command_status):
        try:    
            Msg = "Init ConstructStatus ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            self.command_status = command_status
           
            
            Msg = "ConstructStatus Ok"
            PCA_GenLib.WriteLog(Msg,9)
        except :
            Msg = "ConstructStatus  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)            
            raise          
    def ConstructParameter(self,*Parms):
        try:    
            Msg = "ConstructParameter ..."
            PCA_GenLib.WriteLog(Msg,9)
    
            #self.Message = self.Message + Parameter
    
            for parameter in Parms:
                self.Message = self.Message + parameter
    
            MessageLen = len(self.Message) + 4    
    
            self.SMPP_command_length = struct.pack('!i',MessageLen)
            SMPP_PDU = self.SMPP_command_length + self.Message
            
            Msg = "ConstructParameter Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
    
            return SMPP_PDU
        except :
            Msg = "ConstructUNBIND error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise    
    
