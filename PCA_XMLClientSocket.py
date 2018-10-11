
import sys, string,time
import socket,select
import PCA_GenLib
import PCA_XMLParser
import PCA_ClientSocket

#######################################################################################	

class Connector(PCA_ClientSocket.Connector):
 
    
    ########################################################    
    ## Init Socket Environment and set socket option      ##
    ##    
    ########################################################
    def __init__(self,XMLCFG):    
        try:    
            Msg = "PCA_SMPPClientSocket init ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            Msg = "Connector init ..."
            PCA_GenLib.WriteLog(Msg,1)
            
            
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
    ##        
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
                    
                    break
                    
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
                        SMPP_Length = self.SocketDescriptor.recv(4)  
                        if not SMPP_Length:
                            Msg = "server close connection 1 "
                            PCA_GenLib.WriteLog(Msg,0)
                            raise socket.error,"server close connection 1"
                            
                        smpp_message_length = struct.unpack("!I",SMPP_Length)[0]  
                        SMPP_Data = self.SocketDescriptor.recv(smpp_message_length-4)  
                        if not SMPP_Data:
                            Msg = "server close connection 2"
                            PCA_GenLib.WriteLog(Msg,0)
                            raise socket.error,"server close connection 2"
                        
                        Message = SMPP_Length + SMPP_Data 
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
            PCA_GenLib.WriteLog(Msg,9)            
        
        except socket.error:
            Msg = "Connection close"
            PCA_GenLib.WriteLog(Msg,0)        
        except:
            Msg = "Close Server Socket Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)            
            raise
            
