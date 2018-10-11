
import sys, time,string
from select import select
import socket,thread
import PCA_GenLib
import PCA_XMLParser
import PCA_ThreadLib
import PCA_ServerSocket	
import PCA_DLL
		
#
########################################################
class ServerHandler:	
	def __init__(self,AcceptorConnection,XMLCFG):		
		try:	
			Msg = "ServerHandler Init ..."
			PCA_GenLib.WriteLog(Msg,9)
			self.AcceptorConnection = AcceptorConnection			
			self.ThreadID = id(AcceptorConnection)
			self.WriteSet = []			
	    		self.WriteSet.append(self.AcceptorConnection)              # add to select inputs list 
	    		self.ReadSet = []			
	    		self.ReadSet.append(self.AcceptorConnection)              # add to select inputs list 	
	    			
	    		Tag = "ContentHandler"
			dll_file_name = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			Msg = "%s=%s" % (Tag,dll_file_name)
			PCA_GenLib.WriteLog(Msg,2)
			
			Script_File = PCA_DLL.DLL(dll_file_name)			
			factory_function="Parser"
			factory_component = Script_File.symbol(factory_function)
			self.parser = factory_component()
			
			
			Script_File = PCA_DLL.DLL(dll_file_name)
			factory_function="Handler"
			factory_component = Script_File.symbol(factory_function)
			self.handler = factory_component()
			
			self.parser.setContentHandler(self.handler)
			
			
			
			Msg = "ServerHandler Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
		except:
			Msg = "ServerHandler error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                	PCA_GenLib.WriteLog(Msg,0)
                	raise
        ########################################################		
	## dispatcher				  	      ##
	##						      ##
	########################################################
	def dispatcher(self,TimeOutSeconds=10.0):		
		try:	
			Msg = "dispatcher Init ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			while 1:
				Flag = PCA_ThreadLib.GetMainTerminateFlag()
				if Flag == "TRUE":
					#Msg = "1 end of ServerHandler <%s> " % self.ThreadID
					#PCA_GenLib.WriteLog(Msg,3)
					break
					
				Length=1024
				ReadAttempts = 1
				Message = self.readDataFromSocket(Length,ReadAttempts,TimeOutSeconds)
				if (Message != None):
					
					Message = self.handle_event(Message)
					if (Message != None):							
						self.sendDataToSocket(Message,TimeOutSeconds)
					
			Msg = "dispatcher exit ...<%s> " % self.ThreadID
			PCA_GenLib.WriteLog(Msg,1)
		except socket.error:
			Msg = "dispatcher socket error"
                	PCA_GenLib.WriteLog(Msg,0)			
                	Msg = "socket error end of thread %s" % self.ThreadID
                	PCA_GenLib.WriteLog(Msg,0)                	
                	return            		
		except:
			Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                	PCA_GenLib.WriteLog(Msg,0)
                	Msg = "error : end of thread %s" % self.ThreadID
                	PCA_GenLib.WriteLog(Msg,0)                	
                	return  
        ############################################
        ##  Handler Client Request Code Here        	
	############################################
	def handle_event(self,Message=None):		
		try:	
			Msg = "handle_event Init ..."
			PCA_GenLib.WriteLog(Msg,9)
			Msg = "recv from client connection id = <%s>:data=%s" % (self.ThreadID,Message)
			PCA_GenLib.WriteLog(Msg,1)
			
			self.parser.parse(Message)
			
			MessageBack = self.handler.getHandlerResponse()
					
			
			Msg = "send to client connection id = <%s>:data=%s" % (self.ThreadID,MessageBack)
			PCA_GenLib.WriteLog(Msg,1)	
					
			
			         	
			
			Msg = "handle_event Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
			return MessageBack
		except:
			Msg = "handle_event error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
               		PCA_GenLib.WriteLog(Msg,0)
               		return None
                	          					
	########################################################		
	## Non-Block I/O Send Socket Data		      ##
	##						      ##
	########################################################
	def sendDataToSocket(self,Message,TimeOutSeconds = 0.2):
		try:
			Msg = "sendDataToSocket "
			PCA_GenLib.WriteLog(Msg,9)
			
			WriteAttempts = 3
					
			for i in range(WriteAttempts):    				  		
    				readables, writeables, exceptions = select([], self.WriteSet, [],TimeOutSeconds)
    				for SocketFD in writeables:
        				if (SocketFD == self.AcceptorConnection):            						
            					SocketFD.send(Message)
            					Msg = "sendDataToSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
            					return 1
			Msg = "sendDataToSocket error ,Time out !"
			PCA_GenLib.WriteLog(Msg,7)
			return None
		except socket.error:
			Msg = "sendDataToSocket socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise socket.error
		except:
			Msg = "sendDataToSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	########################################################		
	## Non-Block I/O Read Socket Data		      ##
	##						      ##
	########################################################
	def readDataFromSocket(self,Length=1024,ReadAttempts = 1,TimeOut = 3.0):
		try:
			Msg = "readDataFromSocket "
			PCA_GenLib.WriteLog(Msg,9)
			
			Msg = "Length to read = <%s>  " % Length
			PCA_GenLib.WriteLog(Msg,8)
			Msg = "TimeOut = <%s> Seconds " % TimeOut
			PCA_GenLib.WriteLog(Msg,8)
			
			Msg = "ReadAttempts = <%s>  " % ReadAttempts
			PCA_GenLib.WriteLog(Msg,8)
				
			for i in range(ReadAttempts):    				  		
    				readables, writeables, exceptions = select(self.ReadSet, [], [],TimeOut)
    				for SocketFD in readables:
        				if (SocketFD == self.AcceptorConnection):
						Message = self.AcceptorConnection.recv(Length)  
						if len(Message) == 0:
							Msg = "Server Close Connection %s " % self.ThreadID
							PCA_GenLib.WriteLog(Msg,1)
							raise socket.error,Msg
            					Msg = "ReadDataFromSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
						return Message				
			
			Msg = "readDataFromSocket retry time out !"
			PCA_GenLib.WriteLog(Msg,6)
			return None			
		except socket.error:		
			Flag = PCA_ThreadLib.SetTerminateFlag("TRUE")
			Msg = "end of ClientRequestHandler "
			PCA_GenLib.WriteLog(Msg,3)
			time.sleep(5)
			self.AcceptorConnection.close()
			raise socket.error
		except:
			Msg = "readDataFromSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			Flag = PCA_ThreadLib.SetTerminateFlag("TRUE")
			raise	
########################################################		
## ServerThreads 				      ##
## 1. Create Server Response Thread		      ##
## 2. Server Request Thread 			      ##
########################################################            					
def ServerThreads(AcceptorConnection,XMLCFG):
	try:
		Msg = "ServerThreads Init ..."
		PCA_GenLib.WriteLog(Msg,9)
		
		Response = ServerHandler(AcceptorConnection,XMLCFG)
		Response.dispatcher()
		
		Msg = "ServerThreads Ok ..."
		PCA_GenLib.WriteLog(Msg,9)
	except:
		PCA_ThreadLib.SetTerminateFlag("TRUE")
		Msg = "ServerThreads error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                PCA_GenLib.WriteLog(Msg,0)
                raise

#############################################################################################  
		
##############################################################
#                
##############################################################
class ThreadAcceptor(PCA_ServerSocket.Acceptor):
	########################################################		
	## Wating Client Connection by non-blocking I/O       ##
	##						      ##
	########################################################
	def dispatcher(self,TimeOut=2.0):
		try:
  			#event loop: listen and multiplex until server process killed	
			Msg = "dispatcher server starting"
			PCA_GenLib.WriteLog(Msg,9)
			
			while 1:
				Msg = "listener dispatcher server loop"
				PCA_GenLib.WriteLog(Msg,9)
				
				Flag = PCA_ThreadLib.GetMainTerminateFlag()
				if Flag == "TRUE":
					Msg = "end of dispatcher"
					PCA_GenLib.WriteLog(Msg,8)
					break
					
    				readables, writeables, exceptions = select(self.ReadSet, [], [],TimeOut)    				
    				for self.SocketConnection in readables:
    					##################################
    				        #### for ready input sockets #####
    				        ##################################
        				if self.SocketConnection in self.SocketConnectionPool:  
        					####################################
	            				## port socket: accept new client ##
	            				## accept should not block	  ##
	            				####################################
	        	    			self.connection, address = self.SocketConnection.accept()
        	    				Msg = 'Dispatcher New Connection <%s> from :%s' % (id(self.connection),address)   # connection is a new socket        	    				
            					PCA_GenLib.WriteLog(Msg,1)   
            					Msg = 'Create new thread'
            					PCA_GenLib.WriteLog(Msg,1)  
            					PCA_ThreadLib.SetTerminateFlag("FALSE")
            					thread.start_new(ServerThreads,(self.connection,self.XMLCFG,))
            					
            					
            					
            		PCA_ThreadLib.SetMainTerminateFlag("TRUE")
            		time.sleep(2)
            		PCA_ThreadLib.SetTerminateFlag("TRUE")
            		time.sleep(2)
           	except :
			Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)	
			PCA_ThreadLib.SetMainTerminateFlag("TRUE")
            		time.sleep(2)
            		PCA_ThreadLib.SetTerminateFlag("TRUE")
            		time.sleep(2)		
			raise


			
if __name__ == '__main__':		

  def MainTest(XMLCFG):
	try:
		print 'Start Program ...'
		try:
			TimeOut = 0.3
			PCA_GenLib.DBXMLCFGInit(XMLCFG)	
    			
			Server = ThreadAcceptor(XMLCFG)			
			try:
				Server.dispatcher(TimeOut)
			finally:				
				Server.close()
		finally:
			PCA_GenLib.CloseLog()

	except:
 	  	print '\n\n uncaught ! < ',sys.exc_type,sys.exc_value,' >'
 	  	import traceback
		traceback.print_exc()  
		raise
   	
  ############################### Main Program ############################################	  
  try:	
  	print "Open cfg file"
	XMLCFG =  open("PCA_Server.cfg","r").read()
	#cfg_file_name = sys.argv[1]
	#XMLCFG =  open(cfg_file_name,"r").read()
	
	MainTest(XMLCFG)
  except:
  	print "Error or .cfg configuration file not found"
 	print "Msg = : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
 	import traceback
	traceback.print_exc()  	
  	sys.exit()
  	
 
 
	


