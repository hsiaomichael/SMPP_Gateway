
import sys, string,time
import socket,select
import PCA_GenLib
import PCA_XMLParser
import PCA_ClientSocket
import PCA_SMPP_Parameter_Tag
import PCA_SMPPMessage
import PCA_SMPPParser

#######################################################################################	

class Connector(PCA_ClientSocket.Connector):
    
    
    ########################################################    
    ## Init Socket Environment and set socket option      ##
    ##    ##
    ########################################################
    def __init__(self,XMLCFG):    
        try:    
            Msg = "PCA_SMPPClientSocket init ..."
            PCA_GenLib.WriteLog(Msg,9)
           
            
            Msg = "Connector init ..."
            PCA_GenLib.WriteLog(Msg,1)
            
            self.parser = PCA_SMPPParser.Parser()
            self.handler = PCA_SMPPParser.Handler()
            self.parser.setContentHandler(self.handler)
           
            self.XMLCFG = XMLCFG            
            Tag = "REMOTE_HOST"
            host = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
            
            Tag = "CONNECT_PORT"
            connect_port = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
            
            self.host = host
            self.connect_port = string.atoi(connect_port)
            
            Msg = "Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
            PCA_GenLib.WriteLog(Msg,7)
            
            
            Msg = "Call Socket..."
            PCA_GenLib.WriteLog(Msg,7)
            # make a TCP/IP spocket object
            self.SocketDescriptor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            
            #  /* Set SO_REUSEADDR socket option to allow socket reuse */
            self.SocketDescriptor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            Msg = "setsockopt..SO_REUSEADDR."
            PCA_GenLib.WriteLog(Msg,8)
            
            #   /* Set SO_KEEPALIVE socket option */
            self.SocketDescriptor.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE,1 )
            Msg = "setsockopt...SO_KEEPALIVE"
            PCA_GenLib.WriteLog(Msg,8)
                
            try:                
                
                Tag = "BIND_PORT"
                bind_port = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
                self.bind_port = string.atoi(bind_port)
                
                Msg = "bind port number = <%s>" %  self.bind_port
                PCA_GenLib.WriteLog(Msg,7)
                
                self.SocketDescriptor.bind(('', self.bind_port))      # bind it to server port number
            except:
                Msg = "bind error..."
                PCA_GenLib.WriteLog(Msg,8)       
                 
            
            Tag = "SYSTEM_ID"
            self.UID = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
            
            Tag = "SYSTEM_TYPE"
            self.TYPE = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
             
            Tag = "PASSWD"
            self.PASSWD = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
            
            Msg = "Connector OK."
            PCA_GenLib.WriteLog(Msg,9)                    
                    
                    
            Msg = "PCA_SMPPClientSocket OK."
            PCA_GenLib.WriteLog(Msg,9)
        except :
            Msg = "PCA_SMPPClientSocket Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0) 
            raise
    ########################################################    
    ## Connect To Server 
    ########################################################
    def connect(self):
        try:
            Msg = "connect"
            PCA_GenLib.WriteLog(Msg,9)
            
            
            while 1:
                try:
                    Msg = "Connect to Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
                    PCA_GenLib.WriteLog(Msg,1)
                    
                    self.SocketDescriptor.connect((self.host,self.connect_port))
                    
                    
                    Msg = "Connect to server - connection created "
                    PCA_GenLib.WriteLog(Msg,1)
                    
                    
                    system_id = self.UID+chr(0x00)
                    password = self.PASSWD+chr(0x00)                    
                    system_type = self.TYPE+chr(0x00)                    
                    interface_version = chr(0x34)                    
                    addr_ton = chr(0x01)
                    addr_npi = chr(0x01)
                    
                    address_range = chr(0x01)+chr(0x00)
                    
            
                    self.SMPPWriter = PCA_SMPPMessage.SMPP_PDU_Writer(100)
                    self.SMPPWriter.ConstructHeader(PCA_SMPP_Parameter_Tag.bind_transceiver)
                    SMPP_PDU = self.SMPPWriter.ConstructParameter(system_id,password,system_type,interface_version,addr_ton,addr_npi,address_range)
                    
                    result = self.sendDataToSocket(SMPP_PDU,5.0,1)
                    if result != None:
                        Msg = "send bind receiver to server ok"
                        PCA_GenLib.WriteLog(Msg,1)
                     
                        Message = self.readDataFromSocket(Length=1024,TimeOut = 5.0,ReadAttempts = 1)
                        if Message == None:
            
                            Msg = "read bind response from server timeout , close socket"
                            PCA_GenLib.WriteLog(Msg,1)
                            self.Close()
                            raise socket.error
                    
                        else:
                            self.parser.parse(Message)
                            command_id = self.handler.get_smpp_command_desc()
                            if command_id == "bind_transceiver_resp":
                                Msg = "recv from Client =*%s* , check command status" % command_id
                                PCA_GenLib.WriteLog(Msg,1) 
                                command_status = self.handler.get_smpp_command_status()
                               
                                if command_status != 0:
                                    Msg = "command status = <%d> , smpp bind error" % command_status 
                                    PCA_GenLib.WriteLog(Msg,1)
                                    raise socket.error
                                else:
                                    Msg = "command status = <%d>, bind successful" % command_status 
                                    PCA_GenLib.WriteLog(Msg,1) 
                                break
                            else:
                                Msg = "recv from Client but not a bind_receiver_resposne"
                                PCA_GenLib.WriteLog(Msg,1) 
                                raise socket.error
                            
                               
                    else:
                        Msg = "send bind receiver to server error"
                        PCA_GenLib.WriteLog(Msg,1)
                        raise socket.error
                
                    
                    
                
                except socket.error:
                    Msg = "connect socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                    PCA_GenLib.WriteLog(Msg,0)
                    
                    
                    
                    Msg = "sleep 2 seconds before retry !"
                    PCA_GenLib.WriteLog(Msg,0)
                    
                    time.sleep(2)
                    self.__init__(self.XMLCFG)   
            
            
        except :
            Msg = "ConnectToServer error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)            
            
            raise
                        
    
    ########################################################    
    ## Non-Block I/O Read Socket Data    ##
    ##    ##
    ########################################################
    def readDataFromSocket(self,Length=1024,TimeOut = 2.0,ReadAttempts = 1):
        try:
            Msg = "readDataFromSocket "
            PCA_GenLib.WriteLog(Msg,9)
            
            self.ReadSet = []            
            self.ReadSet.append(self.SocketDescriptor)              # add to select inputs list 

            Msg = "Length to read = <%s>  " % Length
            PCA_GenLib.WriteLog(Msg,8)
            Msg = "TimeOut = <%s> Seconds " % TimeOut
            PCA_GenLib.WriteLog(Msg,8)                        
            Msg = "ReadAttempts = <%s>  " % ReadAttempts
            PCA_GenLib.WriteLog(Msg,8)
            
            for i in range(ReadAttempts):                        
                readables, writeables, exceptions = select.select(self.ReadSet, [], [],TimeOut)
                for SocketFD in readables:
                    if (SocketFD == self.SocketDescriptor):
                        Message = self.SocketDescriptor.recv(Length)  
                        if not Message:
                            Msg = "server close connection"
                            PCA_GenLib.WriteLog(Msg,0)
                            raise socket.error,"server close connection"
                        Msg = "ReadDataFromSocket OK"
                        PCA_GenLib.WriteLog(Msg,9)
                        return Message
            
            
            Msg = "ReadDataFromSocket retry time out !"
            PCA_GenLib.WriteLog(Msg,6)
            
            return None
            
        except socket.error:
            Msg = "readDataFromSocket socket error  reconnect: <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)
            raise socket.error
            
        except:
            Msg = "readDataFromSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)
            self.Close()
            raise            

    
    ########################################################    
    ## Close Socket    ##
    ##    ##
    ########################################################    
    def Close(self):
        
        try:
                
            self.SocketDescriptor.close()    
        
            Msg = "SMPPClient_Socket close OK"
            PCA_GenLib.WriteLog(Msg,0)    
    
        except socket.error:
            Msg = "Connection close"
            PCA_GenLib.WriteLog(Msg,0)    
        except:
            Msg = "Close Server Socket Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise
            
