import sys, time,string
import select
import socket,thread
import PCA_GenLib
import PCA_XMLParser
import PCA_ThreadLib
import PCA_ThreadServer
import PCA_DLL
import PCA_ServerSocket
import PCA_XMLConfiguration
import PCA_SMPP_Parameter_Tag
import PCA_SMPPMessage
import PCA_SMPPParser

SocketMutex = thread.allocate_lock()

ExitFlag = "FALSE"
###############################################################################
## 
###############################################################################

def ConnectToServer(ClientConnector):
    global ExitFlag
    try:
        while 1:
        
            Flag = PCA_ThreadLib.GetMainTerminateFlag()
            SocketMutex.acquire()        
            Flag = ExitFlag        
            SocketMutex.release() 
            if Flag == "TRUE":
                Msg = "break from ConnectToServer"
                PCA_GenLib.WriteLog(Msg,1)
                break
        
            try:        
                try:
                    ClientConnector.Close()
                except:
                    x=1    
                ClientConnector.connect()    
                break    
            except:
                try:
                    ClientConnector.Close()
                except:
                    x=1
    
                Msg = "connect error , sleep 2 second before retry : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                PCA_GenLib.WriteLog(Msg,0)
                time.sleep(2)
                continue
    
        return ClientConnector
    
    except:
       Msg = "ConnectToServer error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
       PCA_GenLib.WriteLog(Msg,0)
       raise
                
###############################################################################
## 
###############################################################################
class ResponseHandler(PCA_ServerSocket.Acceptor):   
                
   
    def __init__(self,XMLCFG):                
        try:        
            Msg = "ResponseHandler Init ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            self.parser = PCA_SMPPParser.Parser()
            self.handler = PCA_SMPPParser.Handler()
            self.parser.setContentHandler(self.handler)
                
            Msg = "ResponseHandler Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
        except:
            Msg = "ResponseHandler error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)
            raise
        ##################################################################################     
        ##  code after tuning
        ##################################################################################   	
    def handle_event(self,SocketBuffer,ClientConnector):
        global ExitFlag
        
        try:        
            Message = None
            
            Msg = "ResponseHandler handle_event Init ..."
            PCA_GenLib.WriteLog(Msg,9)            
            
            while 1:
                #######################################################
                ## Read Response from Server             
                ##                        
                #######################################################
                Flag = PCA_ThreadLib.GetTerminateFlag()
                SocketMutex.acquire()                
                Flag = ExitFlag                
                SocketMutex.release() 
                if Flag == "TRUE":
                    Msg = "end of response handler bf read" 
                    PCA_GenLib.WriteLog(Msg,1)
                    break
                try:
                    Message = ClientConnector.readDataFromSocket(Length=1024,TimeOut = 5.0,ReadAttempts = 1)
                except socket.error:                    
                    Msg = "ResponseHandler readDataFromSocket socket (Server) error"
                    PCA_GenLib.WriteLog(Msg,1)
                    Msg = "Re-Connect to Server ....."
                    PCA_GenLib.WriteLog(Msg,1)
                    ClientConnector = ConnectToServer(ClientConnector)
                    continue
                    
                except select.error:                    
                    Msg = "ResponseHandler readDataFromSocket socket select (Server) error"
                    PCA_GenLib.WriteLog(Msg,1)
                    Msg = "close Server connection "
                    PCA_GenLib.WriteLog(Msg,1)   
                    ClientConnector = ConnectToServer(ClientConnector)
                    continue
                    
                Flag = PCA_ThreadLib.GetTerminateFlag()
                if Flag == "TRUE":
                    Msg = "end of response handler af read" 
                    PCA_GenLib.WriteLog(Msg,1)
                    break
                
                if Message == None:
                    Msg = "read data from Server 5 seconds time-out"  
                    PCA_GenLib.WriteLog(Msg,3)
                    continue
                
                    
                self.parser.parse(Message)
               
                command_id = self.handler.get_smpp_command_desc()
                Msg = "recv from Server =*%s*" % command_id
                PCA_GenLib.WriteLog(Msg,1)
                #####################################################################
                ##                Send back to client                 
                ##################################################################### 
                ServerID = self.handler.get_smpp_seq_no()
                
                
                if SocketBuffer.has_key(ServerID):
                    SocketMutex.acquire() 
                    try:
                        #(AcceptorConnection,client_ip,client_port) = SocketBuffer[ServerID]
                        (AcceptorConnection) = SocketBuffer[ServerID]
                        del SocketBuffer[ServerID]
                    except:
                        
                        Msg = "get SocketBuffer error =\n%s" % SocketBuffer
                        PCA_GenLib.WriteLog(Msg,1)
                        SocketMutex.release()
                        break
                        
                    SocketMutex.release()                    
                else:
                    Msg = "Can not find originl client request connection =\n%s" % SocketBuffer
                    PCA_GenLib.WriteLog(Msg,1)
                    Msg = "send back to Client key failure : %s " % Message
                    PCA_GenLib.WriteLog(Msg,1)
                    break
                    
                self.WriteSet = []
                self.ReadSet = []
                self.ReadSet.append(AcceptorConnection)   # add to select list, wait
                self.WriteSet.append(AcceptorConnection)  # add to select list, wait
                
                try:                
                
                    result = self.sendDataToSocket(AcceptorConnection,Message,TimeOut=0.1,WriteAttempts=3)
                    if result != None:
                    
                        Msg = "send back to Client ok : id=<%s>" % (id(AcceptorConnection))
                        PCA_GenLib.WriteLog(Msg,1)
                    else:
                    
                        Msg = "send back to Client timeout failure : id=<%s>" % (id(AcceptorConnection))
                        PCA_GenLib.WriteLog(Msg,1)
                        
                except socket.error: 
                    
                    Msg = "ResponseHandler sendDataToSocket (Client) socket error"
                    PCA_GenLib.WriteLog(Msg,1)
                    Msg = "send back to Client socket error : id=<%s>" % (id(AcceptorConnection))
                    PCA_GenLib.WriteLog(Msg,1)
                    
                    Msg = "should close Client connection but not in response thread"
                    PCA_GenLib.WriteLog(Msg,1) 
                    
            Msg = "ResponseHandler handle_event Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
            
        except socket.error:
        
            Msg = "ResponseHandler handle_event socket exception"
            PCA_GenLib.WriteLog(Msg,1)            
            time.sleep(0.2)
        except:
            
            PCA_ThreadLib.SetTerminateFlag("TRUE")
            
            Msg = "ResponseHandler handle_event error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0) 
            try:
                Msg = "close Server connection "
                PCA_GenLib.WriteLog(Msg,1)   
                ClientConnector.Close()
            except:
                x=1
        
########################################################                

########################################################                
def ResponseThread(SocketBuffer,ClientConnector,XMLCFG):
    global ExitFlag
    
    try:
    
        Msg = "ResponseThread Init ..."
        PCA_GenLib.WriteLog(Msg,9)
        
        
        ServerResponseHandler = ResponseHandler(XMLCFG)        
        ServerResponseHandler.handle_event(SocketBuffer,ClientConnector)
        
        Msg = "ResponseThread Ok ..."
        PCA_GenLib.WriteLog(Msg,9)
        
        
        SocketMutex.acquire()        
        ExitFlag = "TRUE"        
        SocketMutex.release() 
        
        Msg = "normal end of ResponseThread"
        PCA_GenLib.WriteLog(Msg,1)
    except:
        PCA_ThreadLib.SetTerminateFlag("TRUE")
        
        Msg = "error end of ResponseThread"
        PCA_GenLib.WriteLog(Msg,1)
        
        SocketMutex.acquire()        
        ExitFlag = "TRUE"        
        SocketMutex.release() 
        
        Msg = "ResponseThread error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
        PCA_GenLib.WriteLog(Msg,0)
        try:
            
            Msg = "close Server connection "
            PCA_GenLib.WriteLog(Msg,1)   
            ClientConnector.Close()
            
        except:
            x=1
        return


#############################################################################################  
    
##############################################################
#                
##############################################################
class ThreadAcceptor(PCA_ThreadServer.ThreadAcceptor):
    ########################################################		
    ## Init Socket Environment and set socket option      ##
    ##    ##
    ########################################################
    ClientConnector = 'na'
    ClientConnectorList = []
    IgnoreConnectorList = []
    SocketBuffer = {}
       
    ConnectionLoginState = {}
    number_of_server_connection = 0
    target_id = 1

    response_message = None
    
    ################################################
    ##
    ################################################
    def __init__(self,XMLCFG,cfg_file_name):    
        try:    
            PCA_ThreadServer.ThreadAcceptor.__init__(self,XMLCFG)
            
            self.XMLCFG = XMLCFG
            self.cfg_file_name = cfg_file_name
            
            PCA_ThreadLib.SetMainTerminateFlag("FALSE")
            PCA_ThreadLib.SetTerminateFlag("FALSE") 
            
            Tag = "APPCFG"
            StartTag = Tag
            
            StartTag = "<%s>" % Tag
            EndTag = "</%s>" % Tag
            
            
            (APPCFG,XMLCFG) = PCA_XMLParser.GetTagSection(XMLCFG,StartTag,EndTag)
            
            TaskList = []
            XMLConfiguration = PCA_XMLConfiguration.File_Reader(APPCFG,"TASK")
            
            ###################################################################
            #
            #    Read Configuration File to Task List
            #
            ###################################################################
            
            while 1:
            
                Task = XMLConfiguration.GetXMLConfiguration()
                
                if (Task == None):
                    #Msg = "Your Task  = <%s>" % (Task)
                    #PCA_GenLib.WriteLog(Msg,1)
                    break
                else:                    
                    Msg = "Your Task  = <%s>" % (Task)
                    PCA_GenLib.WriteLog(Msg,4)                    
                    ########################################################
                    #
                    #  Connect to Multi Server 
                    #
                    ########################################################
            
                    Tag = "CLIENT_SOCKET"
                    dll_file_name = PCA_XMLParser.GetXMLTagValue(self.XMLCFG,Tag)
                    Msg = "%s=%s" % (Tag,dll_file_name)
                    PCA_GenLib.WriteLog(Msg,1)
            
                    Script_File = PCA_DLL.DLL(dll_file_name)            
                    factory_function="Connector"
                    factory_component = Script_File.symbol(factory_function)
                    self.ClientConnector = factory_component(Task)
            
                    self.ClientConnector.connect()            
                    
                    thread.start_new(ResponseThread,(self.SocketBuffer,self.ClientConnector,self.XMLCFG,))
                    time.sleep(0.5)
                    Tag = "SOURCD_ID"
            
                    Source_id = PCA_XMLParser.GetXMLTagValue(Task,Tag)
                    Msg = "%s=%s" % (Tag,Source_id)
                    PCA_GenLib.WriteLog(Msg,1)
                    
                    self.ClientConnectorList.append((self.ClientConnector,Source_id))
                    self.number_of_server_connection = self.number_of_server_connection + 1
            
            XMLConfiguration.Close()
              
            self.parser = PCA_SMPPParser.Parser()
            self.handler = PCA_SMPPParser.Handler()
            self.parser.setContentHandler(self.handler)
            
        except :
            Msg = "Gateway ProxyAcceptor Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)    
            raise
        ########################################################
        ##    
        ## Wating Client Connection by non-blocking I/O       
        ##    
        ########################################################
    def dispatcher(self,TimeOut=2.0):
        global ExitFlag
        try:
        
            Msg = "dispatcher server starting ........"
            PCA_GenLib.WriteLog(Msg,1)    
        
            while 1:
                Msg = "listener dispatcher server loop %s timeout" % TimeOut
                PCA_GenLib.WriteLog(Msg,3)
                
                Flag = PCA_ThreadLib.GetMainTerminateFlag()
                SocketMutex.acquire()        
                Flag = ExitFlag        
                SocketMutex.release() 
                
                if Flag == "TRUE":
                    Msg = "end of PSAAdapter dispatcher"
                    PCA_GenLib.WriteLog(Msg,1)
                    break
                    
                readables, writeables, exceptions = select.select(self.ReadSet, [], [],TimeOut)                
                for self.SocketConnection in readables:
                    ###################################################################
                    #
                    #  for ready input sockets 
                    #
                    ###################################################################
                    if self.SocketConnection in self.SocketConnectionPool:  
                        ########################################
                        ##
                        ##     port socket: accept new client 
                        ##     accept should not block	  
                        ##
                        ########################################
                        
                        self.connection, address = self.SocketConnection.accept()
                        Msg = 'Dispatcher New Connection <%s> from :%s' % (id(self.connection),address)   # connection is a new socket                            
                        PCA_GenLib.WriteLog(Msg,1) 
                        
                        self.ReadSet.append(self.connection)   # add to select list, wait
                        self.WriteSet.append(self.connection)  # add to select list, wait
                        
                        client_ip = address[0]
                        client_port = address[1]
                        
                        SocketMutex.acquire()
                        #ServiceID = "%s" % id(self.connection)
                        #ServiceID = "na"
                        #self.SocketBuffer[ServiceID] = (self.connection,client_ip,client_port)
                        
                        Msg = "socket buffer : %s " % self.SocketBuffer
                        PCA_GenLib.WriteLog(Msg,2)
                        
                        SocketMutex.release() 
                        
                    else:
                        if not self.ConnectionLoginState.has_key(id(self.SocketConnection)):
                            self.ConnectionLoginState[id(self.SocketConnection)] = 'N'
                            Msg = "Set ConnectionLoginState <%s> to N " % id(self.SocketConnection)
                            PCA_GenLib.WriteLog(Msg,0)
                        
                        self.handle_event(self.SocketConnection)
            
            Msg = "end of dispatcher"
            PCA_GenLib.WriteLog(Msg,0)            
            
            PCA_ThreadLib.SetMainTerminateFlag("TRUE")
            time.sleep(2)
            PCA_ThreadLib.SetTerminateFlag("TRUE")
            time.sleep(2)
            
            SocketMutex.acquire()            
            ExitFlag = "TRUE"            
            SocketMutex.release() 
        except :
            Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)            
            PCA_ThreadLib.SetMainTerminateFlag("TRUE")
            time.sleep(2)
            PCA_ThreadLib.SetTerminateFlag("TRUE")
            time.sleep(2)            
            
            SocketMutex.acquire()            
            ExitFlag = "TRUE"            
            SocketMutex.release()            
            raise
            

            
    ########################################################		
    ##    
    ##  Handle Client Request
    ##
    ########################################################
    def handle_event(self,AcceptorConnection): 
        command_seq_no = 0
        ServerID = 0
        try:    
            Msg = "RequestHandler handle_event Init ..."
            PCA_GenLib.WriteLog(Msg,9)
            
            
            Message = None
            self.response_message = None
            client_connection_id = "%s" % id(AcceptorConnection)
            #######################################################
            ##
            ##            Read Request from Client            
            ##            
            #######################################################
            try:
 
                Message = self.readDataFromSocket(AcceptorConnection,Length=1024,TimeOut = 5.0,ReadAttempts = 1)
 
            except KeyError:
                Msg = "RequestHandler readDataFromSocket Key.error , connection already closed"
                PCA_GenLib.WriteLog(Msg,2)
                Msg = "Del ConnectionLoginState"
                PCA_GenLib.WriteLog(Msg,0)
                try:
                    del self.ConnectionLoginState[id(AcceptorConnection)]
                except:
                    x=1
                
                raise socket.error
                
            except socket.error:            
                Msg = "RequestHandler readDataFromSocket Client socket.error"
                PCA_GenLib.WriteLog(Msg,1)
                
                Msg = "close Client connection id=<%s>" % client_connection_id
                PCA_GenLib.WriteLog(Msg,1)  
                try:
                    self.ReadSet.remove(AcceptorConnection)   
                    self.WriteSet.remove(AcceptorConnection) 
                except:
                    x=1
                    
                AcceptorConnection.close()
                Msg = "Del ConnectionLoginState"
                PCA_GenLib.WriteLog(Msg,0)
                try:
                    del self.ConnectionLoginState[id(AcceptorConnection)]
                except:
                    x=1
                raise socket.error
                
            Msg = "recv from Client : id=<%s>" % (client_connection_id)
            PCA_GenLib.WriteLog(Msg,2)
            
                  
            self.parser.parse(Message)
            command_id = self.handler.get_smpp_command_desc()
            #if resp_data == "deliver_sm":
            Msg = "recv from Client =*%s*" % command_id
            PCA_GenLib.WriteLog(Msg,1)
            
            #####################################################################
            ### Client Message Maybe more than 1 request 
            #####################################################################
            if self.ConnectionLoginState[id(AcceptorConnection)] == 'N':
            
                Msg = "recv from Client but no bind request yet ,id=<%s>" % (client_connection_id)
                PCA_GenLib.WriteLog(Msg,0)
                command_seq_no = self.handler.get_smpp_seq_no()
                self.SMPPWriter = PCA_SMPPMessage.SMPP_PDU_Writer(command_seq_no)
         
                if command_id == "bind_transmitter":
                    self.SMPPWriter.ConstructHeader(PCA_SMPP_Parameter_Tag.bind_transmitter_resp)
                    self.response_message = self.SMPPWriter.ConstructParameter("gateway")
                    self.ConnectionLoginState[id(self.SocketConnection)] = 'Y'
                elif command_id == "bind_receiver":                    
                    self.SMPPWriter.ConstructHeader(PCA_SMPP_Parameter_Tag.bind_receiver_resp)
                    self.response_message = self.SMPPWriter.ConstructParameter("gateway")
                    self.ConnectionLoginState[id(self.SocketConnection)] = 'Y'
                #elif command_id == "submit_sm":                    
                #    self.SMPPWriter.ConstructHeader(PCA_SMPP_Parameter_Tag.submit_sm_resp)
                #    self.response_message = self.SMPPWriter.ConstructParameter("gateway")
              
                elif command_id == "unbind":                    
                    self.SMPPWriter.ConstructHeader(PCA_SMPP_Parameter_Tag.unbind_resp)
                    self.response_message = self.SMPPWriter.ConstructParameter()
             
                else:
                    Msg = "unexpected data ,id=<%s> , no response " % (client_connection_id)
                    PCA_GenLib.WriteLog(Msg,0)
                    return

                try:                
                    result = self.sendDataToSocket(AcceptorConnection,self.response_message,TimeOut=0.1,WriteAttempts=3)
                    Msg = "send response back to Client " 
                    PCA_GenLib.WriteLog(Msg,0) 
                    return

                except:
                    Msg = "send response back to client error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                    PCA_GenLib.WriteLog(Msg,0) 
                    return 

            try:
                
               
                
                try:

                    
                    if command_id == "submit_sm":     
                        
                        ######### Get one XMLServer Connection fd for send request ##############
                       
                        
                        Msg = "target_id = %s" % self.target_id
                        PCA_GenLib.WriteLog(Msg,1)
                
                        for (ClientConnector,Source_id) in self.ClientConnectorList:
                            if int(Source_id) == self.target_id:
                                break
                                
                        self.target_id = self.target_id + 1        
                        if self.target_id > self.number_of_server_connection:
                            self.target_id = 1
                        
                   
               
                        command_seq_no = self.handler.get_smpp_seq_no()  
                        ServerID = command_seq_no
                        SocketMutex.acquire() 
                        try:
                            self.SocketBuffer[ServerID] = (AcceptorConnection) 
                        except:                
                            Msg = "get SocketBuffer error =\n%s" % self.SocketBuffer
                            PCA_GenLib.WriteLog(Msg,1)
                        SocketMutex.release()
                        
                        result = ClientConnector.sendDataToSocket(Message,TimeOutSeconds=0.01,WriteAttempts=1)
                        if result != None:
                            Msg = "send to Server Source_id=<%s> ok " % (Source_id)
                            PCA_GenLib.WriteLog(Msg,2)
                        else:
                            Msg = "send to Server Source_id=<%s> failure timeout " %  (Source_id)
                            PCA_GenLib.WriteLog(Msg,1)  

                            Msg = "Close Connection: source_id=*%s* " % Source_id
                            PCA_GenLib.WriteLog(Msg,1)  
                        
                                       
                
                    elif command_id == "unbind":     
                        Msg = "unbind requeset , send unbind and remove id=%s" % id(self.SocketConnection)
                        PCA_GenLib.WriteLog(Msg,2)
                        self.SMPPWriter.ConstructHeader(PCA_SMPP_Parameter_Tag.unbind_resp)
                        self.response_message = self.SMPPWriter.ConstructParameter()
                        self.ConnectionLoginState[id(self.SocketConnection)] = 'N'
                        Msg = "send response back to Client " 
                        PCA_GenLib.WriteLog(Msg,0) 
                        self.sendDataToSocket(AcceptorConnection,self.response_message,0.1,3)
                        
             
                    else:
                        Msg = "un-support command , ignore"
                        PCA_GenLib.WriteLog(Msg,1)  
                        
                except socket.error:                        
                        Msg = "send to Primary Server Source_id=<%s> socket error " % (Source_id)
                        PCA_GenLib.WriteLog(Msg,2)
            except:            
                Msg = "error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                PCA_GenLib.WriteLog(Msg,0)            
                Msg = "nothing send back to Client ........ "
                PCA_GenLib.WriteLog(Msg,0) 
            
            Msg = "RequestHandler handle_event Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
            
        except socket.error:            
        
            Msg = "RequestHandler handle_event socket exception,delete socket buffer id=<%s>" % client_connection_id
            PCA_GenLib.WriteLog(Msg,3)

            Msg = "close client connection id=<%s>" % client_connection_id
            PCA_GenLib.WriteLog(Msg,1)
            
            SocketMutex.acquire()            
            try:            
                del self.SocketBuffer[client_connection_id]
            except:
                x=1
            SocketMutex.release() 
            
            time.sleep(0.1)            
        except:
        
            PCA_ThreadLib.SetTerminateFlag("TRUE")            
            Msg = "RequestHandler handle_event error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0) 
            try:
                
                Msg = "close Server connection "
                PCA_GenLib.WriteLog(Msg,1)   
                ClientConnector.Close()
                
                Msg = "close Client connection "
                PCA_GenLib.WriteLog(Msg,1)   
                
                AcceptorConnection.close()
            except:
                x=1
            
            raise
