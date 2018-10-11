import sys
import PCA_GenLib
import PCA_XMLParser


class File_Reader:

	SEQ_NO = 1

	########################################################		
	##
	########################################################
	def __init__(self,XMLCFG,Tag):
		try:
			Msg = "File_Reader Init "
			PCA_GenLib.WriteLog(Msg,9)			
			
			Msg = "Your Tag  = <%s>" % (Tag)
			PCA_GenLib.WriteLog(Msg,8)						
			
			self.Tag = Tag
			
			self.StartTag = "<%s%s>" % (self.Tag,self.SEQ_NO)
			self.EndTag = "</%s%s>" % (self.Tag,self.SEQ_NO)
			
			Msg = "Your XMLCFG  = <%s>" % (XMLCFG)
			PCA_GenLib.WriteLog(Msg,8)
			
			self.XMLCFG = XMLCFG
			
			
			Msg = "File_Reader Init OK"
			PCA_GenLib.WriteLog(Msg,9)
		except:
			Msg = "File_Reader Init Error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)	
			raise
	#########################################################################
	# Get File from Input Directory
	#
	#########################################################################
	def GetXMLConfiguration(self):
		try:
			Msg = "GetXMLConfiguration Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			(Section,self.RestXMLCFG) = PCA_XMLParser.GetTagSection(self.XMLCFG,self.StartTag,self.EndTag)
			self.SEQ_NO = self.SEQ_NO + 1	
			self.StartTag = "<%s%s>" % (self.Tag,self.SEQ_NO)
			self.EndTag = "</%s%s>" % (self.Tag,self.SEQ_NO)	
			
			Msg = "Your Data = %s" % Section
			PCA_GenLib.WriteLog(Msg,9)
			
		
			Msg = "GetXMLConfiguration OK"
			PCA_GenLib.WriteLog(Msg,9)
			
			return Section
  		except:
			Msg =  "GetXMLConfiguration Error <%s> <%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,3)
			return None


	########################################################		
	##
	########################################################
	def Close(self):
		try:
			Msg = "Close Init "
			PCA_GenLib.WriteLog(Msg,9)
			
			Msg = "Close OK"
			PCA_GenLib.WriteLog(Msg,9)
		except:
			Msg = "Close Error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)	
			raise
			
