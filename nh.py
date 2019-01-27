#!/usr/bin/env python3
import os, npyscreen, curses, sys, time, string

class ActionControllerSearch(npyscreen.ActionControllerSimple):
	def create(self):
		self.add_action("^.*", self.set_search, True)


	def set_search(self, command_line, widget_proxy, live):
		global filtered_history_elements

		keywords = command_line.lower().split()
		filtered_history_elements = []

		for history_element in history_elements:
			if all(keyword in history_element[2].lower() for keyword in keywords): filtered_history_elements.append(history_element)

		self.parent.wMain.values = list(map(lambda x: x[2], filtered_history_elements)) 
		self.parent.wMain.display()


class FmSearchActive(npyscreen.FormMuttActiveTraditional):
	ACTION_CONTROLLER = ActionControllerSearch
	
	def execute_command_in_shell(self, act_on_this, key_press):
		with open(ACTION_FILE, "w") as action_file:
			action_file.write(act_on_this)
		sys.exit(10)


	def edit_command_in_shell(self, _ignore):
		command = filtered_history_elements[self.wMain.cursor_line][2]
		with open(ACTION_FILE, "w") as action_file:
			action_file.write(command)
		sys.exit(11)


	def create(self, *args, **kwargs):
		super(FmSearchActive, self).create(*args, **kwargs)
		self.wStatus1.value = "nh 0.1.0"
		self.wStatus2.value = "Type to search   [Enter] Execute   [TAB] Edit before execution   (Total: {} history lines)".format(len(history_elements))
		self.wMain.actionHighlighted = self.execute_command_in_shell
		self.wMain.values = list(map(lambda x: x[2], filtered_history_elements))
		self.wCommand.BEGINNING_OF_COMMAND_LINE_CHARS = (tuple(string.ascii_letters) + tuple(string.digits) + tuple(string.punctuation))
		self.wCommand.always_pass_to_linked_widget = ["^C", "^B", "^J", "^I"]  # Pass Arrow-Up, Arrow-Down and Enter to Multiline Widget
		self.wMain.add_handlers({curses.ascii.TAB: self.edit_command_in_shell})


class NH_App(npyscreen.NPSAppManaged):
	def onStart(self):
		global filtered_history_elements
		self.registerForm("MAIN", FmSearchActive())


if __name__ == '__main__':
	NH_HOME = os.environ["HOME"] + "/.nh"

	HISTORY_CONTENT_FILE = NH_HOME + "/history"
	ACTION_FILE = NH_HOME + "/action"

	with open(HISTORY_CONTENT_FILE, "r") as history_content_file:
		history_lines = history_content_file.readlines()

	if "HISTTIMEFORMAT" not in os.environ: 
		WORDS_IN_HISTORY_TIME_FORMAT = 0
	else: 
		WORDS_IN_HISTORY_TIME_FORMAT = os.environ["HISTTIMEFORMAT"].strip().count(" ") + 1
	
	history_elements = []
	
	for line in history_lines: 
		split_line = line.split()
		line_index = split_line[0]
		line_timestamp = " ".join(split_line[1:WORDS_IN_HISTORY_TIME_FORMAT+1])
		line_command = " ".join(split_line[1+WORDS_IN_HISTORY_TIME_FORMAT:])
		history_elements.append([line_index, line_timestamp, line_command])
	
	# Overrides
	npyscreen.FormMutt.MAIN_WIDGET_CLASS = npyscreen.MultiLineAction
	npyscreen.FormMutt.MAIN_WIDGET_CLASS_START_LINE = 1

	filtered_history_elements = history_elements

	NH_App = NH_App()
	try: 
		NH_App.run()
	except KeyboardInterrupt: 
		sys.exit(0) #Allow to end the programm with STRG+C without throwing an exception