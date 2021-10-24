# -*- coding: UTF-8 -*-
# Author: Alberto Buffolino
# Original license of imported module, see:
# https://github.com/nvaccess/nvda/blob/master/source/appModules/eclipse.py

from nvdaBuiltin.appModules.eclipse import *
from addonHandler import initTranslation
from displayModel import DisplayModelTextInfo
from NVDAObjects.IAccessible.sysTreeView32 import TreeViewItem
import controlTypes as ct
import textInfos

initTranslation()

unreadLabel = _("Unread, ")
# for pre-2022.1 compatibility
TREEVIEWITEM = ct.Role.TREEVIEWITEM if hasattr(ct, "Role") else ct.ROLE_TREEVIEWITEM

class AppModule(AppModule):

	def __init__(self, processID, appName=None):
		super(AppModule, self).__init__(processID, appName)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == TREEVIEWITEM and obj.windowStyle not in (1442923045, 1446068773):
			clsList.insert(0, NewsItem)

class NewsItem(TreeViewItem):

	def isUnread(self):
		info = DisplayModelTextInfo(self, position=textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		fields = info.getTextWithFields()
		try:
			bold = fields[0].field["bold"]
		except:
			bold = False
		return bold

	def event_gainFocus(self):
		if self.name == super().name and self.isUnread():
			self.name = unreadLabel+self.name
		else:
			self.name = super().name
		super(NewsItem, self).event_gainFocus()
