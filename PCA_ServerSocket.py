
import sys, time,string
from select import select
import socket
import PCA_GenLib
import PCA_XMLParser

class Acceptor:
	ConnectionLoginState = {}
	########################################################		
	## Init Socket Environment and set socket option      ##
	##						      ##
	########################################################
	def __init__(self,XMLCFG):		
		try:	
			Msg = "Acceptor Init ..."
			PCA_GenLib.WriteLog(Msg,9)
			self.XMLCFG = XMLCFG
			
			Tag = "LISTEN_HOST"
			host = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			self.host = host
			
			
			Tag = "LISTEN_PORT"
			port = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			self.port = string.atoi(port)

			Msg = "Listen Host=<%s>,Port=<%s>" % (self.host,self.port)
			PCA_GenLib.WriteLog(Msg,1)
			
			
			numPortSocks = 1                      		 # number of ports for client connects	
			# make main sockets for accepting new client requests
			self.SocketConnectionPool, self.ReadSet, self.WriteSet = [], [], []
	
			for i in range(numPortSocks):
				Msg = "Call Socket..."
				PCA_GenLib.WriteLog(Msg,9)
	    			SocketDescriptor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # make a TCP/IP spocket object
	    			
	    			# you should add "setsockopt(level, optname, value)"  here
	    			#  /* Set SO_REUSEADDR socket option to allow socket reuse */
	    			SocketDescriptor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    			Msg = "setsockopt..SO_REUSEADDR."
				PCA_GenLib.WriteLog(Msg,9)
				
	    			#   /* Set SO_KEEPALIVE socket option */
      			  	SocketDescriptor.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE,1 )
      			  	Msg = "setsockopt...SO_KEEPALIVE"
				PCA_GenLib.WriteLog(Msg,9)
				
				SocketDescriptor.bind(('', self.port))      # bind it to server port number

    				Msg = "setsockopt..bind port = <%s>." % self.port
				PCA_GenLib.WriteLog(Msg,0)
 
	    			SocketDescriptor.listen(5)                         # listen, allow 5 pending connects
	    		
				Msg = "setsockopt..Listen.SocketFD=<%s>" % (SocketDescriptor)
				PCA_GenLib.WriteLog(Msg,9)
 
    				self.SocketConnectionPool.append(SocketDescriptor) # add to main list to identify
	    			self.ReadSet.append(SocketDescriptor)              # add to select inputs list 
	    			self.WriteSet.append(SocketDescriptor)             # add to select output list 
    				                    
    			
    			
    			Msg = "Acceptor Initial Ok "
			PCA_GenLib.WriteLog(Msg,9)	
		except :
			Msg = "Acceptor Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise

	########################################################		
	## Wating Client Connection by non-blocking I/O       ##
	##						      ##
	########################################################
	def dispatcher(self,TimeOut=0.2):
		try:
  			#event loop: listen and multiplex until server process killed	
			Msg = "dispatcher server starting"
			PCA_GenLib.WriteLog(Msg,9)
			RecvDataCNT = 0
			while 1:
				
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
	        	    			connection, address = self.SocketConnection.accept()
        	    				Msg = 'Dispatcher New Connection <%s> from :%s' % (id(connection),address)   # connection is a new socket        	    				
            					PCA_GenLib.WriteLog(Msg,1)   
            					         				
            					self.ReadSet.append(connection)   # add to select list, wait
            					self.WriteSet.append(connection)  # add to select list, wait
            					
            					self.ConnectionLoginState[id(connection)] = 'N'
                				Msg = "Set ConnectionLoginState <%s> to N " % id(connection)
                				PCA_GenLib.WriteLog(Msg,1)
            					
        				else:
            					try:
            						RecvDataCNT = RecvDataCNT + 1
            						ClientMessage = self.SocketConnection.recv(1)
            					
            						if not ClientMessage:
            							Msg = "Client Close Connection ..id=%s" % id(self.SocketConnection)
                						PCA_GenLib.WriteLog(Msg,1)
                						self.SocketConnection.close()                   # close here and remv from
                						self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                						self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                						
                						Msg = "Del ConnectionLoginState <%s>" % id(self.SocketConnection)
                						PCA_GenLib.WriteLog(Msg,1)
								del self.ConnectionLoginState[id(self.SocketConnection)]

                					else:
                						###################################
                						### Got Data Message From Client ##
                						###################################
                						#Message = self.readDataFromSocket(ClientMessage)
                						self.handle_event(self.SocketConnection,ClientMessage)
                						
                				except socket.error:
                					Msg = "dispatcher socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                					PCA_GenLib.WriteLog(Msg,0)	
                					
                					self.SocketConnection.close()                   # close here and remv from
                					self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                					self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                					del self.ConnectionLoginState[id(self.SocketConnection)]
                					
                					break
                		
                		if len(readables) == 0 or RecvDataCNT >= 10:
                			RecvDataCNT = 0
					self.handle_timeout()                					
		except :
			Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise
	
	
	########################################################		
	## 						      ##
	##						      ##
	########################################################					
	def handle_event(self,SocketEventFD,ClientMessage):
		try:
			Msg = "handle_event Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			
			
			Msg = "handle_event OK"
			PCA_GenLib.WriteLog(Msg,9)			
		except:
			Msg = "handle_event Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	
	
	########################################################		
	## 						      ##
	##						      ##
	########################################################					
	def handle_timeout(self):
		try:
			Msg = "handle_timeout Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			
			
			Msg = "handle_timeout OK"
			PCA_GenLib.WriteLog(Msg,9)			
		except:
			Msg = "handle_timeout Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	
				
	########################################################		
	## Non-Block I/O Read Socket Data		      ##
	##						      ##
	########################################################
	def readDataFromSocket(self,SocketEventFD,Length=1024,TimeOut = 3.0,ReadAttempts = 1):
		try:
			Msg = "readDataFromSocket "
			PCA_GenLib.WriteLog(Msg,9)
			
			for i in range(ReadAttempts):    				  		
    				readables, writeables, exceptions = select(self.ReadSet, [], [],TimeOut)
    				for SocketFD in readables:
        				if (SocketFD == SocketEventFD):
						Message = SocketFD.recv(Length)  
						if len(Message) == 0:
							Msg = "Client Close Connection id=<%s>" % id(SocketFD)
							PCA_GenLib.WriteLog(Msg,2)
							raise socket.error,Msg
            					
						Msg = "ReadDataFromSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
						return Message
				
			
			Msg = "readDataFromSocket retry time out !"
			PCA_GenLib.WriteLog(Msg,6)
			return None
		
		except socket.error:
			
			SocketEventFD.close()                   # close here and remv from
                	self.ReadSet.remove(SocketEventFD)      # del list else reselected 
                	self.WriteSet.remove(SocketEventFD)     # del list else reselected 
                						
                	Msg = "Del ConnectionLoginState <%s>" % id(SocketEventFD)
                	PCA_GenLib.WriteLog(Msg,2)
			del self.ConnectionLoginState[id(SocketEventFD)]
			raise socket.error
			
		except:
			Msg = "readDataFromSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
			
	########################################################		
	## Non-Block I/O Send Socket Data		      ##
	##						      ##
	########################################################
	def sendDataToSocket(self,SocketEventFD,Message,TimeOut=5.0,WriteAttempts=1):
		try:
			Msg = "sendDataToSocket "
			PCA_GenLib.WriteLog(Msg,9)	
	
			for i in range(WriteAttempts):    				  		
    				readables, writeables, exceptions = select([], self.WriteSet, [],TimeOut)
    				for SocketFD in writeables:
        				if (SocketFD == SocketEventFD):
        					#Msg = "Send :*%s*" % PCA_GenLib.HexDump(Message)
            					#PCA_GenLib.WriteLog(Msg,5)            				
            					SocketFD.send(Message)
            					Msg = "sendDataToSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
            					return 1
        				
			Msg = "sendDataToSocket error ,Time out !"
			PCA_GenLib.WriteLog(Msg,1)
			return None
		except:
			Msg = "sendDataToSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			#SocketEventFD.close()
			raise
	########################################################		
	## Close Socket					      ##
	##						      ##
	########################################################					
	def close(self):
		try:
			Msg = "close Acceptor Socket Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			##self.SocketConnection.shutdown(1)		# Send FIN , further sends are disallowed
			
			
			self.SocketConnection.close()	
			
			Msg = "close Acceptor Socket OK"
			PCA_GenLib.WriteLog(Msg,9)
			
		except socket.error:
			Msg = "close socket error"
			PCA_GenLib.WriteLog(Msg,0)
		except AttributeError:
			self.SocketConnectionPool[0].close()		
		except:
			Msg = "close Acceptor Socket Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	
			
			

			
if __name__ == '__main__':		

  def MainTest(XMLCFG):
	try:
		print 'Start Program ...'
		try:
			TimeOut = 0.3
			PCA_GenLib.DBXMLCFGInit(XMLCFG)	
			
			Server = Acceptor(XMLCFG)
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
	
	MainTest(XMLCFG)
  except:
  	print "Error or .cfg configuration file not found"
 	print "Msg = : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
 	import traceback
	traceback.print_exc()  	
  	sys.exit()
  	
 
 
	


