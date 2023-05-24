# coding :utf-8
# version 4.2 avec NVDA+F4 et NVDA+shift+f4
from NVDAObjects.IAccessible import IAccessible
from tones import beep
import os
from api import  copyToClip
from speech import speak
import characterProcessing
if not hasattr(characterProcessing, "SYMLVL_SOME"):
	SYMLVL_SOME = characterProcessing.SymbolLevel.SOME
else:
	from characterProcessing import SYMLVL_SOME
from ui import message
import zRoleTexts
import controlTypes
#from cv2 import getTickCount
import time
from wx import CallLater
def clsListToText(lst) :
	cl = str()
	i = 0
	for e in lst :
		cl += str(i) + ": " + str(e) + "\n"
		i += 1
	return "liste classes :\n" + cl
	
	mtlog = 0 # objet  partagée de la classe memorylog, instancié dans __init__ de appModule
class memoryLog() :
	_prevLine = ""
	active = False
	textLog = ""
	path = "" # file path
	def __init__(self, activate, basePath) :
		self.active = activate
		if basePath == "" :
			self.path =  getDocumentsPath() + "\\GrandRobertLogs" # basePath sans \ à la fin ni nom de fichier
		else :
			self.path = basePath
		self.activate(activate)
		return
	def activate(self, flag) :
		self.active = flag
		if flag :
			os.makedirs(self.path, exist_ok=True) # crée le répertoire s'il n(existe pas
		return
	def add(self, line) :
		if not self.active : return
		if line == self._prevLine : return
		self.textLog = self.textLog + str(line) + "\n"
		return
	def addText(self, line) :
		if not self.active : return
		self.textLog = self.textLog + str(line)
		return
	def copy(self) :
		if not self.active : return
		message("Copie du journal")
		copyToClip (self.textLog)
		message(self.textLog)
	def addprops(self, o , title="", update=True ) :
		if not self.active : return
		#tc = str(getTickCount()())
		tc = "" # str(time.time())
		title  = tc + "-" + title

		if not o :
			self.textLog = self.textLog + str(title) + " : objet nul dans memoryLog\n"
			return
		r = 0 
		if hasattr(o, "role") : r = o.role
		tRole = zRoleTexts.roleConsts[r] 
		
		tID =  ""
		tmp = getIA2Attribute(o)
		if tmp : tID = ", ID : " + str(tmp)
		
		tTag = ""
		if hasattr(o, "tag") : tTag = ", tag : " +  str(o.tag)
		if hasattr(o, "childCount") :
			tCC =  ", childCount : " + str(o.childCount)
		else : tCC = "no childCount attribute"
		
		tName = ""
		tmp = o.name
		if tmp : tName = ", name : " +  str(tmp)
		
		tVal = ""
		tmp = o.value
		if tmp : tVal = ", val : " + str(tmp)
		
		if o.windowClassName : 
			tWndClass =  str(o.windowClassName)
			if tWndClass.startswith("Afx") :  tWndClass = "AFX etc"
			tWndClass = ", wcl : "  + tWndClass
		else : tWndClass = ""
		if hasattr(o, "windowControlID") : 
			tcID = o.windowControlID
			if tcID : tcID =  ", ctrlID : " + str(tcID)
		else : tcID = ""

		tActions = ""
		try :
			ac = o._get_actionCount()
			if ac > 0 :
				tActions = ", Actions : "
				for j in range (ac) :
					tActions = tActions + o.getActionName(j) + ", "
		except: 
			tActions = ""
			pass

		l = title + " : " + tRole + tID +  tTag + tCC + tName + tVal + str(tcID) + tWndClass + ", " + getTextStates(o) + tActions + "\n"
		if update :
			self.textLog = self.textLog + l
			return
		else :
			return l
	def reinit(self) :
		if not self.active : return
		self.textLog = str("")
		self._prevLiene = ""
	def save(self, baseName, delFile=False) :
		if not self.active : return
		lt = time.localtime(time.time())
		curDate= str(lt.tm_year) + "-" + str(lt.tm_mon) + "-" + str(lt.tm_mday) + " " + str(lt.tm_hour) + "-" + str(lt.tm_min) + "-" + str(lt.tm_sec) 
		fullPath  = self.path +"\\" + baseName + " " + curDate + ".txt"
		#message("chemain : " + fullPath)
		with open(fullPath, mode="a", encoding="utf8") as file_obj:
			file_obj.write(self.textLog)
		self.reinit()
		os.startfile (fullPath)
		if delFile :
			CallLater(7000, os.remove, fullPath)

def getTextStates(o) :
	tStates = ""
	if not hasattr(o, "states") : return "pas d'attributs"
	if (controlTypes.State.UNAVAILABLE if hasattr(controlTypes, "State") else controlTypes.STATE_UNAVAILABLE) in o.states : tStates = tStates + str(", UNAVAILABLE")
	if (controlTypes.State.FOCUSED if hasattr(controlTypes, "State") else controlTypes.STATE_FOCUSED) in o.states : tStates = tStates + str(", FOCUSED")
	if (controlTypes.State.SELECTED if hasattr(controlTypes, "State") else controlTypes.STATE_SELECTED) in o.states : tStates = tStates + str(", SELECTED")
	if (controlTypes.State.BUSY if hasattr(controlTypes, "State") else controlTypes.STATE_BUSY) in o.states : tStates = tStates + str(", BUSY")
	if (controlTypes.State.PRESSED if hasattr(controlTypes, "State") else controlTypes.STATE_PRESSED) in o.states : tStates = tStates + str(", PRESSED")
	if (controlTypes.State.CHECKED if hasattr(controlTypes, "State") else controlTypes.STATE_CHECKED) in o.states : tStates = tStates + str(", CHECKED")
	if (controlTypes.State.HALFCHECKED if hasattr(controlTypes, "State") else controlTypes.STATE_HALFCHECKED) in o.states : tStates = tStates + str(", HALFCHECKED")
	if (controlTypes.State.READONLY if hasattr(controlTypes, "State") else controlTypes.STATE_READONLY) in o.states : tStates = tStates + str(", READONLY")
	if (controlTypes.State.EXPANDED if hasattr(controlTypes, "State") else controlTypes.STATE_EXPANDED) in o.states : tStates = tStates + str(", EXPANDED")
	if (controlTypes.State.COLLAPSED if hasattr(controlTypes, "State") else controlTypes.STATE_COLLAPSED) in o.states : tStates = tStates + str(", COLLAPSED")
	if (controlTypes.State.INVISIBLE if hasattr(controlTypes, "State") else controlTypes.STATE_INVISIBLE) in o.states : tStates = tStates + str(", INVISIBLE")
	if (controlTypes.State.PROTECTED if hasattr(controlTypes, "State") else controlTypes.STATE_PROTECTED) in o.states : tStates = tStates + str(", PROTECTED")
	if (controlTypes.State.REQUIRED if hasattr(controlTypes, "State") else controlTypes.STATE_REQUIRED) in o.states : tStates = tStates + str(", REQUIRED")
	if (controlTypes.State.DEFUNCT if hasattr(controlTypes, "State") else controlTypes.STATE_DEFUNCT) in o.states : tStates = tStates + str(", DEFUNCT")
	if (controlTypes.State.INVALID_ENTRY if hasattr(controlTypes, "State") else controlTypes.STATE_INVALID_ENTRY) in o.states : tStates = tStates + str(", INVALID_ENTRY")
	if (controlTypes.State.MODAL if hasattr(controlTypes, "State") else controlTypes.STATE_MODAL) in o.states : tStates = tStates + str(", MODAL")
	if (controlTypes.State.MULTILINE if hasattr(controlTypes, "State") else controlTypes.STATE_MULTILINE) in o.states : tStates = tStates + str(", MULTILINE")
	if (controlTypes.State.ICONIFIED if hasattr(controlTypes, "State") else controlTypes.STATE_ICONIFIED) in o.states : tStates = tStates + str(", ICONIFIED")
	if (controlTypes.State.OFFSCREEN if hasattr(controlTypes, "State") else controlTypes.STATE_OFFSCREEN) in o.states : tStates = tStates + str(", OFFSCREEN")
	if (controlTypes.State.SELECTABLE if hasattr(controlTypes, "State") else controlTypes.STATE_SELECTABLE) in o.states : tStates = tStates + str(", SELECTABLE")
	if (controlTypes.State.FOCUSABLE if hasattr(controlTypes, "State") else controlTypes.STATE_FOCUSABLE) in o.states : tStates = tStates + str(", FOCUSABLE")
	if (controlTypes.State.CLICKABLE if hasattr(controlTypes, "State") else controlTypes.STATE_CLICKABLE) in o.states : tStates = tStates + str(", CLICKABLE")
	if (controlTypes.State.EDITABLE if hasattr(controlTypes, "State") else controlTypes.STATE_EDITABLE) in o.states : tStates = tStates + str(", EDITABLE")
	if (controlTypes.State.CHECKABLE if hasattr(controlTypes, "State") else controlTypes.STATE_CHECKABLE) in o.states : tStates = tStates + str(", CHECKABLE")
	if (controlTypes.State.OBSCURED if hasattr(controlTypes, "State") else controlTypes.STATE_OBSCURED) in o.states : tStates = tStates + str(", OBSCURED")
	if (controlTypes.State.CROPPED if hasattr(controlTypes, "State") else controlTypes.STATE_CROPPED) in o.states : tStates = tStates + str(", CROPPED")
	if (controlTypes.State.OVERFLOWING if hasattr(controlTypes, "State") else controlTypes.STATE_OVERFLOWING) in o.states : tStates = tStates + str(", OVERFLOWING")
	if (controlTypes.State.UNLOCKED if hasattr(controlTypes, "State") else controlTypes.STATE_UNLOCKED) in o.states : tStates = tStates + str(", UNLOCKED")
	if (controlTypes.State.HAS_ARIA_DETAILS if hasattr(controlTypes, "State") else controlTypes.STATE_HAS_ARIA_DETAILS) in o.states : tStates = tStates + str("" + ", has aria details")
	return u"états" + tStates
def getDocumentsPath() :
	import ctypes.wintypes
	CSIDL_PERSONAL = 5       # My Documents
	SHGFP_TYPE_CURRENT = 0   # Get current, not default value

	buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
	ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
	#message(buf.value)
	return str(buf.value)

def getIA2Attribute (obj,attribute_value=False,attribute_name ="id"):
	r= hasattr (obj,"IA2Attributes") and attribute_name in obj.IA2Attributes.keys ()
	if not r :return False
	r =obj.IA2Attributes[attribute_name]
	return r if not attribute_value  else r ==attribute_value

