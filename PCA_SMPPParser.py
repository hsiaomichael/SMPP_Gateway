
import sys,struct,time
import PCA_GenLib
import PCA_Parser
import PCA_SMPP_Parameter_Tag
import PCA_DLL

##############################################################################
###    Message Handler 
##############################################################################
class Handler(PCA_Parser.ContentHandler): 
    Message = None
    command_desc = None
    seq_no = 0
    command_status = 0
    def __init__(self):
        PCA_Parser.ContentHandler.__init__(self)        
        
    def startDocument(self):
        self.Message = None
        self.command_name = None
        self.command_desc = None
        self.seq_no = 0
        self.command_status = 0
    
    
    def startElement(self, name, attrs):
        self.TID = ''
        self.SOURCD_ID = "HeartBeat"
        self.command_name = name
        
        
    def characters(self, content):       
        if self.command_name == "command_id":
            self.command_desc = content  
        elif self.command_name == "sequence_number":
            self.seq_no = content      
        elif self.command_name == "command_status":
            self.command_status = content      
            
        
    def endDocument(self,debugstr,TID,SOURCD_ID,response_message ):
        self.DebugStr = debugstr
        self.TID = TID
        self.SOURCD_ID = SOURCD_ID
    
    def getSOURCD_ID(self):	
        return self.SOURCD_ID
        
    def getHandlerResponse(self):
        return self.Message 
    def get_smpp_seq_no(self):
        return self.seq_no
        
    def get_smpp_command_desc(self):
         return self.command_desc   
    def get_smpp_command_status(self):
         return self.command_status   
#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
    
    
    
    DebugStr = 'na'
    SMS_TYPE='na'    
    TID = 'na'    
    Service_Type = 'na'
    SOURCD_ID = 'HeartBeat'    

    def __init__(self):
        try:
            Msg = "parser __init__"
            PCA_GenLib.WriteLog(Msg,9)
            
            PCA_Parser.Parser.__init__(self)
            
            Msg = "parser __init__ ok"
            PCA_GenLib.WriteLog(Msg,9)
        except:
            Msg = "parser __init__  :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)
            raise
        
    def set_handler(self,name,attrs,content):
        
        self._cont_handler.startElement(name, attrs)        
        self._cont_handler.characters(content)
        self._cont_handler.endElement(name)       
        
        
    def parse(self, source):
        try:
            Msg = "parser init"
            PCA_GenLib.WriteLog(Msg,9)            
            self.SOURCD_ID = 'HeartBeat'
            self.DebugStr = 'na'
            orig_data = source
            name = 'none'            
            self.StartParsing = 0
            
            if (source != None) and len(source) > 0: 
                self._cont_handler.startDocument()
                self.StartParsing = 1
            
                name = "command_length"
                attrs = source[0:4]
                content = struct.unpack("!i",attrs)[0]
                command_length = content
                self.set_handler(name,attrs,content)
            
                source = source[4:]
                name = "command_id"
                attrs = source[0:4]            
                content = struct.unpack("!i",attrs)[0]
                try:
                    command_id = PCA_SMPP_Parameter_Tag.command_id_dict[attrs]
                except:
                    command_id  = 'undef'
            
                content = command_id
                self.set_handler(name,attrs,content)
                
                source = source[4:]
                name = "command_status"
                attrs = source[0:4]            
                content = struct.unpack("!i",attrs)[0]
                command_status = content
                self.set_handler(name,attrs,content)
            
                source = source[4:]
                name = "sequence_number"
                attrs = source[0:4]            
                content = struct.unpack("!I",attrs)[0]
                self.TID = content
                sequence_number = content
                self.set_handler(name,attrs,content)
            
            
                Msg = "REQ_TID=<%s>,command_length=<%s>,command_id=<%s>,command_status=<%s>,sequence_number=<%s>" % (self.TID,command_length,command_id,command_status,sequence_number)
                PCA_GenLib.WriteLog(Msg,2)
                
                self.DebugStr = Msg
                
            
            if self.StartParsing == 1:
                self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID,source)
            
            Msg = "parser OK"
            PCA_GenLib.WriteLog(Msg,9)
        except:
            Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
            PCA_GenLib.WriteLog(Msg,0)
            
            Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
            PCA_GenLib.WriteLog(Msg,0)
            
            Msg = "rest data =\n%s" % PCA_GenLib.HexDump(source)
            PCA_GenLib.WriteLog(Msg,0)
            if self.StartParsing == 1:
                self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID,'undef')
            raise
            
