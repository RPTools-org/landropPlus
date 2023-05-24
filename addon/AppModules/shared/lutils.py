# coding :utf-8
import controlTypes, api, winUser
import zDevTools as z
from tones import beep
from time import sleep
import wx

dlgType = "init"
dlgObj = None
selDevice = ""
def findChild(obj, role, wndClass, ctrlID=0, name="", applog=None) :
	try :
		obj = obj.firstChild
	except :
		#if applog : applog.add("findChild : obj nul")
		return None
	while obj  : 
		if applog : applog.addprops(obj, "Boucle findChild ")
		if obj.role == role :
			if ctrlID :
				if obj.windowControlID == ctrlID: break
			if obj.name : 
				if name in obj.name : break
			if wndClass :
				if wndClass in obj.windowClassName : break
		obj = obj.next
	# si pas trouvé, obj vaut None en sortie de voucle
	if obj :
		if applog : 
			applog.addprops(obj, u"Trouvé findChild ")
	return obj
	
def getObjectTree(obj, level, path, applog=None) :
	if not obj : return False
	#if not obj.childCount : return False
	tcc = ""
	if hasattr(obj, "childCount") :
		tcc =  " sur " + str(obj.childCount - 1) + ", " #dernier index et non le nombre

	try :
		obj = obj.firstChild
	except :
		return False
	level += 1
	ctr = 0
	while obj  : 
		if applog : applog.addprops(obj, "niveau " + str(level) + ", " + str(ctr) + tcc)
		beep(343, 1)
		getObjectTree(obj, level, path, applog)
		ctr += 1
		obj = obj.next
	return True
	
def click(obj) :
	# Location : RectLTWH(left=434, top=149, width=37, height=24)
	x = int(obj.location.left + obj.location.width / 2)
	y = int(obj.location[1] + obj.location[3]/2)
	winUser.setCursorPos (x, y)
	winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,1,None,None)
	sleep(0.001) 
	winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
	return
