from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
from hashlib import md5

class DummyMD5Authorizer(DummyAuthorizer):
	def validate_authentication(self, username, password, handler):
		hash = md5(password).hexdigest()
		return self.user_table[username]['pwd'] == hash

class MyServer:
	server = None

	perms_list = {'normal':'lr', 'admin':'elradfmwM'}

	def __init__(self, port=2121):
		self.authorizer = DummyMD5Authorizer()
		handler = FTPHandler
		handler.authorizer = self.authorizer
		port = int(port)
		self.server = FTPServer(('0.0.0.0', port), handler)
		
	def add_user(self, username, password, user_dir='.', perm='normal'):
		if perm not in self.perms_list.keys():
			perm = self.perms_list['normal']
		else:
		 	perm = self.perms_list[perm]

		self.authorizer.add_user(username, md5(password).hexdigest(), user_dir, perm)

	def main(self):
		self.server.serve_forever()

class MyServerManager:

	welcome_message = '''
		Welcome to MyServer Management.
		Author:p1usj4de
		Any question please contact p1usj4de@163.com
	'''

	help_message = '''1.add_user username passwd perm -- add a ftp user(perm could be normal or admin)
2.add_mass prefix num passwd -- add a mass user, perm will be normal,password will be same
4.run -- start the server'''

	prompt = '>'
	server = None

	def __init__(self, prompt=None):
		if not prompt == None:
			self.prompt = prompt

		self.server = MyServer()
	
	def process_add_user(self, cmd_list):
		if len(cmd_list) != 4:
			print 'Argument failed'
			return False
		self.server.add_user(cmd_list[1],cmd_list[2],perm=cmd_list[3])
		
	def process_add_mass(self, cmd_list):
		if len(cmd_list) != 4:
			print 'Argument failed'
			return False
		for index in range(int(cmd_list[2])):
			user = cmd_list[1] + str(index) # username = prefix + index number
			passwd = cmd_list[3]
			self.server.add_user(user, passwd)
			print 'add user for (%s) with password (%s)' % (user, passwd)

	def main(self):
		print self.welcome_message
	       	while True:
	 		command = raw_input(self.prompt).strip().split(' ')
	 		if command[0] == 'add_user':
	 			self.process_add_user(command)
	 		elif command[0] == 'add_mass':
	 			self.process_add_mass(command)
	 		elif command[0] == 'run':
	 			break
	 		elif command[0] == 'help':
	 			print self.help_message
	 		else:
	 			print 'Unrecognised command...'
	 	self.server.main()

if __name__ == '__main__':
	manager = MyServerManager()
	manager.main()
