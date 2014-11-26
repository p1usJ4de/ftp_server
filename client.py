#_*_ coding:utf-8 _*_
import ftplib

class Client:
	def __init__(self, host, port, user, passwd, timeout=20):
		# storing some infomation for next use
		self.host = host
		self.port = int(port)
		self.user = user
		self.passwd = passwd
		self.timeout = int(timeout)

		# Instantiate a ftp instance
		self.ftp = ftplib.FTP()
		# close debug
		self.ftp.set_debuglevel(0)
		
		try:
			self.ftp.connect(self.host, self.port, self.timeout)
			self.ftp.login(self.user, self.passwd)
		except:
			self.ftp = None
			print 'ERROR:connection failed,please contact with ftp server administrator or veriry your username and password again'

	def retrieve(self, filename, destination=None):
		if self.ftp == None:
			return False

		command = 'RETR '+filename
		if destination == None:
			destination = filename
		# open destination file to write
		try:
			f = open(destination, 'wb+')
		except IOError:
			print 'ERROR: can not open file to read'
			return False
		self.ftp.retrbinary(command, f.write)

	def rename(self, fromname, toname):
		if self.ftp == None:
			return False
		try:
			self.ftp.rename(fromname, toname)
		except ftplib.error_perm:
			print 'ERROR:can not rename this file.'
			return False

	def delete(self, filename):
		if self.ftp == None:
			return False
		try:
			self.ftp.delete(filename)
		except ftplib.error_perm:
			print 'ERROR:can not delete this file.'

	def size(self, filename):
		if self.ftp == None:
			return False
		return self.ftp.size(filename)

	def cd(self, pathname):
		if self.ftp == None:
			return False
		try:
			self.ftp.cwd(pahtname)
		except  ftplib.error_perm:
			print 'ERROR:can not change directory.'

	def pwd(self):
		if self.ftp == None:
			return False
		return self.ftp.pwd()

	def store(self, source, destination=None):
		if destination == None:
			destination = source
		command = 'STOR '+destination
		try:
			f = open(source, 'rb+')
		except IOError, e:
			print 'ERROR:can not open file to write'
			return False
		self.ftp.storbinary(command, f)

	def list(self):
		if self.ftp == None:
			return False
		try:
			file_list = self.ftp.nlst()
			for name in file_list:
				print name
		except ftplib.error_perm:
			print 'ERROR:permission denied -- can not list files'

	def mkdir(self, pathname):
		if self.ftp == None:
			return False
		try:
			self.ftp.mkd(pathname)
		except ftplib.error_perm:
			print 'ERROR:permission denied -- can not make a dir'

	def size(self, filename):
		if self.ftp == None:
			return False
		return self.ftp.size(filename)

	def quit(self):
		if self.ftp != None:
			self.ftp.quit()
			self.ftp.close()
		else:
			return False

	def is_login(self):
		return True if self.ftp != None else False

class ClientView:
	welcome_message = '''
		Welcome to this simple ftp server
		Author:p1usj4de
		Any question please contact p1usj4de@163.com
		Please input help to get message about how to use this program
	'''
	help_message = '''1.login host port user passwd [timeout] -- login into a ftp server
2.list -- list files
3.mkdir pathname -- make a new dir
4.get filename destination -- retrieve a file from ftp server
5.post filename destination -- store file in ftp server with name of destination
6.quit -- quit from ftp server
7.exit -- exit from this program
8.rename fromname toname -- rename a ftp file 
9.delete filename -- delete a ftp file
10.cd pathname -- change your working directory
11.pwd -- print current working directory
12.size filename -- return the size of a file in the ftp server
'''
	exit_message = 'Thank you for using.'
	prompt = '>'

	client = None

	is_login_on = False

	def __init__(self, welcome_message=None, prompt=None):
		if welcome_message is not None:
			self.welcome_message = welcome_message
		if prompt is not None:
			self.prompt = prompt 

	def generate_callable_string(self, cmd_list):
		# construct argument string
		arguments = ','.join(['\''+ x +'\'' for x in cmd_list[1:]]) if len(cmd_list) > 1 else ''
		# add function header and join the arguments
		cmd_str = 'self.process_'+cmd_list[0]+'('+arguments+')'
		print cmd_str
		return cmd_str

	'''
		start of a bunch of process_xxx function 
	'''
	def process_login(self, host, port, user, passwd, timeout=20):
		self.client = Client(host, port, user, passwd, timeout)
		self.is_login_on = self.client.is_login()

	def process_get(self, filename, destination=None):
		if self.is_login_on:
			self.client.retrieve(filename, destination)
		else:
			print 'You need to login on first...'

	def process_post(self, filename, destination=None):
		if self.is_login_on:
			self.client.store(filename, destination)
		else:
			print 'You need to login on first...'

	def process_mkdir(self, pathname):
		if self.is_login_on:
			self.client.mkdir(pathname)
		else:
			print 'You need to login on first...'
	
	def process_quit(self):
		if self.is_login_on:
			self.client.quit()
			self.is_login_on = False
		else:
			print 'You need to login on first...'
	
	def process_list(self):
		if self.is_login_on:
			self.client.list()
		else:
			print 'You need to login on first...'

	def process_rename(self, fromname, toname):
		if self.is_login_on:
			self.client.rename(fromname, toname)
		else:
			print 'You need to login on first...'

	def process_delete(self, filename):
		if self.is_login_on:
			self.client.delete(filename)
		else:
			print 'You need to login on first...'

	def process_cd(self, pathname):
		if self.is_login_on:
			self.client.cd(pathname)
		else:
			print 'You need to login on first...'

	def process_pwd(self):
		if self.is_login_on:
			print self.client.pwd()
		else:
			print 'You need to login on first...'


	def process_size(self, filename):
		if self.is_login_on:
			print self.client.size(filename)
		else:
			print 'You need to login on first...'
	'''
		end of a bunch of process_xxx function
	'''
	def main(self):
		print self.welcome_message
		while True:
			command = raw_input(self.prompt).strip().split(' ')
			if command[0] == 'exit':
				print self.exit_message
				break
			if command[0] == 'help':
				print self.help_message
				continue

			cmd_str = self.generate_callable_string(command)
			try:
				exec(cmd_str)
			except AttributeError, e:
				print 'Unrecognised command -- %s' % e
		'''	except SyntaxError, e:
				print 'Arguments error -- %s' % e
			except TypeError, e:
				print 'Arguments error -- %s' % e
		'''		
if __name__ == '__main__':
	view = ClientView()
	view.main()


