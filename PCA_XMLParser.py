import string
import sys

#############################################################################
# return the Section in the form <StartTag>XXX</EndTag>. 
# of a field given TAG
# input : (<TAG1>data1</TAG1><TAG2>data2></TAG2> , <TAG2>,</TAG2>)
# output : <TAG2>data1</TAG2>
#############################################################################

def GetTagSection(XMLString,StartTag,EndTag):
	#print "YourXMLString =%s" % XMLString
  	StartPos = string.find(XMLString,StartTag)  
  	if (StartPos == -1 ):
    		Msg = "GetTagSection -- StartTag Not Found !"
    		raise ValueError("GetTagSection -- StartTag Not Found !" + StartTag)
    		
    	#print "StartPos = %s" % StartPos	
        
        EndPos = string.find(XMLString,EndTag)  
  	if (EndPos == -1 ):
    		Msg = "GetTagSection -- EndTag Not Found !"    		
    		raise ValueError("GetTagSection -- EndTag Not Found !")
    		
  	#print "EndPos = %s" % EndPos  	
 	
  	FieldValue = XMLString[StartPos:EndPos+len(EndTag)]    	
  	#return string.strip(FieldValue),XMLString[EndPos+len(EndTag):]
  	return FieldValue,XMLString[EndPos+len(EndTag):]

#############################################################################
# Return first XML Section of input XML string
# input = <TAG1>data1</TAG1><TAG2>data2></TAG2>
# output = <TAG1>data1</TAG1>
#############################################################################
def GetFirstTagSection(XMLString):
	#print "GetFirstTagSection:YourXMLString =%s" % XMLString
	FirstTag = GetTagSection(XMLString,"<",">")[0]
	
	#print "GetFirstTagSection:your tag =%s" % FirstTag
	Tag = FirstTag[1:-1]
	StartTag = "<%s>" % Tag
  	EndTag = "</%s>" % Tag
  	#print "GetFirstTagSection:your start tag =%s" % StartTag
  	#print "GetFirstTagSection:your end tag =%s" % EndTag
	Data = GetTagSection(XMLString,StartTag,EndTag)[0]
	
	
  	return Data

#############################################################################
# input = <TAG1>data1</TAG1>
# output = TAG1
#############################################################################
def GetXMLTag(XMLString):
	
	FirstTag = GetTagSection(XMLString,"<",">")[0]
	Tag = FirstTag[1:-1]
	
  	return Tag
#############################################################################
# return the Section in the form <Tag><Parameter>XXX</Parameter></Tag>. 
# of a field given TAG , in this example return <Parameter>XXX</Parameter>
#############################################################################

def GetTagSectionValue(XMLString,Tag):
	#print "YourXMLString =%s" % XMLString
	#print "Tag =%s" % Tag	
	StartTag = "<%s>" % Tag
  	EndTag = "</%s>" % Tag
  	StartTagLength = len(StartTag)
  	StartPos = string.find(XMLString,StartTag)  
  	if (StartPos == -1 ):
    		Msg = "GetTagSection -- StartTag Not Found !"
    		raise ValueError('GetTagSection -- StartTag Not Found !')
    	StartPos = StartPos + StartTagLength	
    	#print "StartPos = %s" % StartPos	
        EndTagLength = len(EndTag)
        EndPos = string.find(XMLString,EndTag)  
  	if (EndPos == -1 ):
    		Msg = "GetTagSectionValue -- EndTag Not Found !"    		
    		raise ValueError("GetTagSectionValue -- EndTag Not Found !" )
    		
  	#print "EndPos = %s" % EndPos  	
 	
  	FieldValue = XMLString[StartPos:EndPos] 	
  	
  
  	return FieldValue
  	
  	
##########################################################################
# return the value of a field given in the form <TAG>XXX</TAG>. 
# XXX will be returned in this case.
##########################################################################
	
def GetTagValue(XMLString):
	#print "YourXMLString =%s" % XMLString
	
  	StartPos = string.find(XMLString,">")  
  	if (StartPos == -1 ):    		  
    		Msg = "GetTagValue -- StartTag Not Found !"
    		raise
    		
    	#print "StartPos = %s" % StartPos    	
        
        EndPos = string.find(XMLString[1:-1],"<")  
  	if (EndPos == -1 ):
    		Msg = "GetTagValue -- EndTag Not Found !"    		
    		raise
    		
  	#print "EndPos = %s" % EndPos    	  	
 	
  	FieldValue = XMLString[StartPos+1:EndPos+1]
  	return FieldValue;

	
def OldGetTagValue(XMLString):
	#print "YourXMLString =%s" % XMLString
	
  	StartPos = string.find(XMLString,">")  
  	if (StartPos == -1 ):    		  
    		Msg = "GetTagValue -- StartTag Not Found !"
    		raise
    		
    	#print "StartPos = %s" % StartPos    	
        
        EndPos = string.find(XMLString[1:-1],"<")  
  	if (EndPos == -1 ):
    		Msg = "GetTagValue -- EndTag Not Found !"    		
    		raise
    		
  	#print "EndPos = %s" % EndPos    	  	
 	
  	FieldValue = XMLString[StartPos+1:EndPos+1]
  	return FieldValue;  	
##########################################################################
# return the value of a given TAG from a given XML String. 
# 
##########################################################################
	
def GetXMLTagValue(CMD,Tag):
   try:
	StartTag = "<%s>" % Tag
  	EndTag = "</%s>" % Tag
  	MyValue,CMD = GetTagSection(CMD,StartTag,EndTag)
  	
  	#print "Section : %s" % MyValue
  	Field = GetTagValue(MyValue);
   	return string.strip(Field);
   except :
   	#print "GetXMLTagValue : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
   	raise

##########################################################################
# Set XML String Tag value to Python Dictionary  
# 
##########################################################################
def XMLToDict(XMLString):
	XMLDict = {}
	x=1
	
	return {}

##########################################################################
# Set XML String Tag value to Python List  
# 
##########################################################################
def XMLToList(XMLString):
	XMLList = []
	
	
	return []
##############################################################################################################
	
if __name__ == '__main__': 
 
  try :
	
	
	XMLCFG =  open("PCA_DBServer.cfg","r").read()	
	try:
		
		
		CMD = '''
			<RSP>
			<RESULT>SUCCESS</RESULT>
			<MSG>Message</MSG>
			</RSP>'''
		CMD = '''			
		<REQ>
		<CMD>AddAPIConnectionUser</CMD>
		<USER>User Name</USER>
		<PARAMETERS>
		<SP>Service Provider</SP>
		<USERNAME>User Name</USERNAME>
		<ROLEID>User Role ID</ROLEID>
		<ROLE>User Role Name</ROLE>
		<PWD>Password</PWD>
		<SESSIONS>Number of concurrent sessions</SESSIONS>
		</PARAMETERS>
		</REQ>'''

		###################################################################
		print "------------------------------------"
		API_Command = GetXMLTagValue(CMD,"CMD")
		print "your api command = <%s>" % API_Command
		TableName = API_Command[:3]

		tmp = GetTagSection(CMD,"<USER>","</USER>")[0]
		wherecmd = GetXMLTag(tmp)		
		wheredata = GetXMLTagValue(CMD,"USER")
		#print "your api command = <%s>" % wherecmd
		
		XMLString = GetTagSectionValue(CMD,"PARAMETERS")
		#print "CMD value = *%s*" % XMLString
		SQL_STRING = "select "
		while 1:
		
			try:
				data = GetFirstTagSection(XMLString)
				print "GetFirstTagSection:value = *%s*" % data
		
				FirstTagData = GetXMLTag(data)		
				StartTag = "<%s>" % FirstTagData
				EndTag = "</%s>" % FirstTagData
				SQL_STRING = "%s %s," % (SQL_STRING,FirstTagData)
				XMLString = GetTagSection(XMLString,StartTag,EndTag)[1]
				#print "value = *%s*" % XMLString
			except:			
				break
		#print "your sql = *%s*" % SQL_STRING[:-1]
		SQL = "%s from %s where %s='%s';" % (SQL_STRING[:-1],TableName,wherecmd,wheredata)
		print "your sql = *%s*" % SQL
	except :
		#print 'The Field for Tag <%s> Not Found  ' % Tag
		print "Msg = <%s>,<%s>" % (sys.exc_type,sys.exc_value)
		
  except SystemExit:
  	print "",
  except:
  	
   	print "Main Program : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
   	
