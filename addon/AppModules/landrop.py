# coding :utf-8

import appModuleHandler, controlTypes, api, globalVars
from NVDAObjects.window import Window
from tones import beep
from time import sleep
import ui
from keyboardHandler import KeyboardInputGesture
import wx, gui # for searchBox
# import   modukles from shared sub folder
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import lutils 
# outils de developpement
# import zDevTools as z # pour   classe memoryLog
#  py3compatibility pas encore utiles pour l'instant
#import py3compatibility
#from  py3compatibility import _unicode
del sys.path[-1]

class AppModule(appModuleHandler.AppModule):
	applog = None # référence à l'objet de la classe zDevTools memorylog
	_instance = False # pour searchBox

	def event_foreground(self,obj,nextHandler):
		lutils.dlgObj = None
		if obj.role == controlTypes.Role.DIALOG and obj.windowClassName == "Qt5152QWindowIcon" :
			lutils.dlgObj =  obj
			# if obj.WindowClassName != "Qt5152QWindowIcon" : 
				# lutils.dlgType = "other"
				# return nextHandler()
			nm = obj.name
			if "Select File(s) to be Sent" in nm :
				lutils.dlgType = "main"
			elif "Send to" in nm : 
				lutils.dlgType = "sendto"
			elif "Transferring" in nm :
				lutils.dlgType = "transfer"
				if lutils.selDevice :
					wx.CallLater(1000, ui.message, _("Please  accept this transfer on : " + lutils.selDevice))
					# lutils.selDevice = ""
			elif "Settings" in nm :
				lutils.dlgType = "settings"
				# Settings dialogue Device NameDownload PathDiscoverableServer Port
			else :
				lutils.dlgType = "other"
		nextHandler()

	# def event_gainFocus (self,obj,nextHandler):
		# beep(200, 20)
		#nextHandler()
	
	#def chooseNVDAObjectOverlayClasses (self,obj,clsList):
	# pour un usage ultérieur
	
	# def event_NVDAObject_init(self, obj):
		# # attribue un libellé au champ de recherche
		# # pour obtenir  le windowControlID 106,  donner le focus au champ de recherche puis presser control+puissance 2
		# if isinstance(obj, Window) and obj.windowClassName == "Edit" and obj.windowControlID == 106 :
			# obj.name = "Rechercher : "
	def sayDeviceName(self, o) :
		if hasattr(o, "name") : nm = o.name
		else : nm = _("No device found")
		lutils.selDevice = nm
		# translator
		msg = _("{0}, address : {1}, port : {2}")
		wx.CallLater(150,ui.message,msg.format(nm, lutils.dlgObj.getChild(1).value, str(lutils.dlgObj.getChild(3).value)))
		return
	def selectFirstDevice(self) :
		if lutils.dlgType != "sendto" : return
		fo = lutils.dlgObj.getChild(4) # list
		if fo.role != controlTypes.Role.LIST : return
		if not fo or  fo.childCount  == 0 : 
			ui.message(_("No target device found"))
			return 
		fo = fo.firstChild
		if not fo or fo.role != controlTypes.Role.LISTITEM : return
		lutils.click(fo)
		api.setFocusObject(fo)
		self.sayDeviceName(fo)
		return 

		
	# scripts
	def script_tab(self, gesture) :
		if lutils.dlgType != "sendto" : return gesture.send()
		fo =api.getFocusObject()
		if fo != lutils.dlgObj.getChild(3) : 
			# beep(100, 40)
			return gesture.send() # edit port 
		# beep(400, 40)
		fo = fo.next # list
		if fo.role != controlTypes.Role.LIST : return gesture.send()
		if not fo or  fo.childCount  == 0 : 
			ui.message(_("No target device found"))
			return gesture.send()
		fo = fo.firstChild
		if not fo or fo.role != controlTypes.Role.LISTITEM : return gesture.send()
		lutils.click(fo)
		api.setFocusObject(fo)
		self.sayDeviceName(fo)
		return 

	def script_shiftTab(self, gesture) :
		if lutils.dlgType != "sendto" : return gesture.send()
		fo =api.getFocusObject()
		if not (fo.role == controlTypes.Role.BUTTON and fo.name == "Send") : 
			# beep(100, 40)
			return gesture.send() # edit port 
		# beep(400, 40)
		fo = lutils.dlgObj.getChild(4) # list
		if fo.role != controlTypes.Role.LIST : return gesture.send()
		if not fo or  fo.childCount  == 0 : 
			ui.message(_("No target device found"))
			return gesture.send()
		fo = fo.firstChild
		if not fo or fo.role != controlTypes.Role.LISTITEM : return gesture.send()
		lutils.click(fo)
		api.setFocusObject(fo)
		self.sayDeviceName(fo)
		return 
	def script_upArrow(self, gesture) :
		if lutils.dlgType != "sendto" : return gesture.send()
		fo =api.getFocusObject() # globalVars.focusObject
		if  fo.role != controlTypes.Role.LISTITEM :		 return gesture.send()
		o = fo.previous
		if  o :
			fo = o
			lutils.click(fo)
		self.sayDeviceName(fo)
		return 
	def script_downArrow(self, gesture) :
		if lutils.dlgType != "sendto" : return gesture.send()
		fo =api.getFocusObject() # globalVars.focusObject
		if fo.role == controlTypes.Role.EDITABLETEXT : 				return self.selectFirstDevice()

		if  fo.role != controlTypes.Role.LISTITEM :		 return gesture.send()
		o = fo.next
		if  o :
			fo = o
			lutils.click(fo)
		self.sayDeviceName(fo)
		return 


		# control+puissance2 :currentObject : obtenir les attributs de l'objet qui a le focus ainsi que la liste inverse de ses ascendants
	def script_currentObject(self, gesture) : 
		# beep(440,30)
		memLog = z.memoryLog(activate=True, basePath="") # 1er param :  True=actif ou Falses=inactif # journalisation  memoire
		#o = api.getFocusObject()
		o = api.getNavigatorObject()
		memLog.addprops(o, u"Attributs Objet Navigator")
		# Remontée de parent en parent
		memLog.add("Liste des ascendants  en sens invers")
		asc = ""
		i = -1
		o = o.parent
		while o :
			asc = str(memLog.addprops(o, "# " + str(i), update=False)) + asc
			i -= 1
			o = o.parent
		memLog.add(asc)
		memLog.save("GrandRobert objet courant") # enregistre mini-journal  et l'affiche dans le bloc notes

	# script_listObjects : liste des objets descendants  de la fenêtre. 
	def script_listObjects(self, gesture) : 
		#beep(440, 30)
		memLog = z.memoryLog(activate=True, basePath="") # 1er param :  True=actif ou Falses=inactif, si basePath vide, crée un sous dossier GrandRobertLogs  du dossier  documents  
		memLog.add(u"Liste des objets enfants de la fenêtre du Grand Robert")
		#fg = api.getForegroundObject() # objet fenÃªtre au premier plan, le Grand Robert
		fg =globalVars.foregroundObject
		try :
			# la fonction getObjectTree est récursive, elle s'appelle elle-même afin de parcourir tous les niveaux de l'arborescence des objets de NVDA pour cette fenêtre
			lutils.getObjectTree(fg, level=0, path="", applog=memLog)
		finally :
			memLog.save("GrandRobert objets") # enregistre mini-journal  et l'affiche dans le bloc notes
		return
		# ci-dessous, méthode  non récursive sur 4 niveaux
		# on boucle parmi plusieurs générations de descendants   de fg
		# o = fg
		# i = 0 # index de child
		# while o : # tant que o n'est pas None
			# memLog.addprops(o, "Niveau 1, " + str(i) + "; " )
			# o2 = o.firstChild
			# j = 0
			# while o2 :
				# memLog.addprops(o2, "  Niveau 2, " + str(j) + "; " )
				# o3 = o2.firstChild 
				# k = 0
				# while o3 :
					# memLog.addprops(o3, "    Niveau 3, " + str(k) + "; " )
					# o4 = o3.firstChild
					# l = 0
					# while o4 :
						# memLog.addprops(o4, "        Niveau 4, " + str(l) + "; " )
						# l += 1
						# o4 =  o4.next
					# k += 1
					# o3 = o3.next
				# j += 1
				# o2 = o2.next
			# i += 1
			# o = o.next # objet frere suivant 
		# apres boucle
		# memLog.save("GrandRobert objets") # enregistre mini-journal  et l'affiche dans le bloc notes


	__gestures={
		"kb:tab" : "tab",	
		"kb:shift+tab" : "shiftTab",	
	"kb:downArrow" : "downArrow",	
	"kb:upArrow" : "upArrow",	
	u"kb:control+²":"currentObject", # voir def script_currentObject 
	u"kb:shift+²":"listObjects", 
	}
