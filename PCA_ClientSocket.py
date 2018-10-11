import sys, string,time,struct
import socket
import PCA_GenLib
import PCA_XMLParser
import select

#######################################################################################	

class Connector:
	
	########################################################		
	## Init Socket Environment and set socket option      ##
	##						      ##
	########################################################
	def __init__(self,XMLCFG):		
		try:	
			Msg = "Connector init ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			
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
				
    				#self.SocketDescriptor.bind((self.host, self.bind_port))      # bind it to server port number
    				#localhost = "127.0.0.1"
    				self.SocketDescriptor.bind(('', self.bind_port))      # bind it to server port number
    			except:
    				Msg = "bind error..."
				PCA_GenLib.WriteLog(Msg,8)    			
    			
    			Msg = "Connector OK."
			PCA_GenLib.WriteLog(Msg,9)	    						
		except :
			Msg = "Connector Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise
	########################################################		
	## Connect To Server				      ##
	##						      ##
	########################################################
	def connect(self):
		try:
			Msg = "connect Init"
			PCA_GenLib.WriteLog(Msg,9)
			Msg = "Connect to Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
			PCA_GenLib.WriteLog(Msg,1)
			
			self.SocketDescriptor.connect((self.host,self.connect_port))
			
  			Msg = "connect OK"
			PCA_GenLib.WriteLog(Msg,9)
		except socket.error:
			Msg = "connect socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)	
			raise
		except :
			Msg = "connect error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)	
			raise
			
	########################################################		
	## Non-Block I/O Send Socket Data		      ##
	##						      ##
	########################################################
	def sendDataToSocket(self,Message,TimeOutSeconds=0.5,WriteAttempts=1):
		try:
			Msg = "sendDataToSocket "
			PCA_GenLib.WriteLog(Msg,9)	
			
			WriteAttempts = 1	
			self.WriteSet = []
			
	    		self.WriteSet.append(self.SocketDescriptor)              # add to select inputs list 
	    			
			for i in range(WriteAttempts):    				  		
    				readables, writeables, exceptions = select.select([], self.WriteSet, [],TimeOutSeconds)
    				for SocketConnection in writeables:
        				if (SocketConnection == self.SocketDescriptor):
        					         				
            					SocketConnection.send(Message)
            					Msg = "sendDataToSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
            					return 1
        				
			Msg = "sendDataToSocket error ,Time out !"
			PCA_GenLib.WriteLog(Msg,7)
			#raise socket.error,"send time out"
			return None
		except:
			Msg = "sendDataToSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise

	########################################################		
	## Non-Block I/O Read Socket Data		      ##
	##						      ##
	########################################################
	def readDataFromSocket(self,Length=1024,TimeOut = 1.0,ReadAttempts = 1):
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
			PCA_GenLib.WriteLog(Msg,3)
			
			return None
			
		except socket.error:
			Msg = "ReadDataFromSocket socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	
		except:
			Msg = "ReadDataFromSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	

	

	########################################################		
	## Close Socket					      ##
	##						      ##
	########################################################					
	def Close(self):
		try:
			Msg = "Close Socket Init"
			PCA_GenLib.WriteLog(Msg,9)
			##SocketFD.shutdown(1)		# Send FIN , further sends are disallowed
			
			Msg = "Close connection from Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
			PCA_GenLib.WriteLog(Msg,1)
				
			self.SocketDescriptor.close()	
			
			Msg = "Close Socket OK"
			PCA_GenLib.WriteLog(Msg,9)	
		
		except socket.error:
			Msg = "Connection close"
			PCA_GenLib.WriteLog(Msg,0)			
		except:
			Msg = "Close Socket Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise
		
