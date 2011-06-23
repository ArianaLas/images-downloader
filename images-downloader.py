#!/usr/bin/python
# coding=utf-8

import urllib.request, sys, getopt, platform, os;

class imagesDownloader:
	__urls = '';
	__name = '';
	__ext = ('jpg', 'png', 'gif', 'jpeg', 'bmp');
	__target = '';
	__amount = 0;
	__recursive = False;
	__depth = None;
	__keepDomain = False;
	__verbose = False;
	__sep = '/';
	__count = 0;

	def __init__(self):
		if platform.system().lower() == 'windows':
			self.__sep = '\\';
		try:
			options, args = getopt.getopt((sys.argv[1:]),
			'n:e:t:a:rd:khv',
			['name=', 'extension=', 'target-dir=', 'amount=', 'recursive', 'depth', 'keep-domain', 'help', 'verbose']);
		except getopt.GetOptError as err:
			print('[E] Bad option(s)...');
			self.__usage();
			sys.exit(1);
		for option, value in options:
			if option in ('-n', '--name'):
				self.__v('Setting image name as %s' % value);
				self.__name = value;
			elif option in ('-e', '--extension'):
				self.__v('Setting image extension(s) as %s' % value);
				self.__ext = value.split(',');
			elif option in ('-t', '--target-dir'):
				self.__v('Setting target directory to write images as %s' % value);
				if value[-1] in ('/', '\/'):
					self.__target = value;
				else:
					self.__target = value + self.__sep;
			elif option in ('-a', '--amount'):
				self.__v('Setting amount of images to download as %s' % value);
				self.__amount = value;
			elif option in ('-r', '--recursive'):
				self.__v('Setting option recursive searching');
				self.__recursive = True;
			elif option in ('-d', '--depth'):
				self.__v('Setting depth of recursive searching as %s' % value);
				self.__depth = value;
			elif option in ('-k', '--keep-domain'):
				self.__v('Setting option keep-domain');
				self.__keepDomain = True;
			elif option in ('-h', '--help'):
				self.__usage();
				sys.exit(0);
			elif option in ('-v', '--verbose'):
				self.__verbose = True;
		if not self.__target:
			target = '.%s' % self.__sep;
			self.__v('Setting target directory to write images as default %s' % self.__target);
		if self.__amount == None:
			self.__v('Setting amount of images to download as max');
		if self.__depth == None:
			self.__v('Setting depth of recursive searching as max');
		self.__urls = args;
		if not self.__urls:
			self.__usage();
			sys.exit(1);
		self.__prepare();
		self.__parse();
	
	def __v(self, text):
		if self.__verbose == True:
			print('[I] %s...' % text);
	
	def __usage(self):
		print('========== IMAGE-DOWNLOADER ==========');
		print('Automatically searching and downloading images from web pages');
		print('Author: Ariana Las <ariana.las@gmail.com>');
		print('\n[E] <- Error\n[W] <- Warning\n[I] <- Information\n');
		print('Usage:\timages-downloader [options] url(s)');
		print('\t-n --name\n\t\timage name (default is original image name)');
		print('\t-e --extension\n\t\timage extension (default are all known image extensions)\n\t\tif need various, use "," for example: -e jpg,png,gif');
		print('\t-t --target-dir\n\t\ttarget directory to write downloaded images\n\t\t(default current directory)');
		print('\t-a --amount\n\t\tmaximum amount of images to download (default all)\n\t\tmaximum amount of images if there is less images\n\t\ton the page than you gave in amount');
		print('\t-r --recursive\n\t\trecursive searching in pages');
		print('\t-d --depth\n\t\tdepth of recursion (default max)');
		print('\t-v --verbose\n\t\tverbose mode');
		print('\t-h --help\n\t\tdisplay help');
 
	def __prepare(self):
		self.__v('Preparing directories');
		try:
			self.__v('Checking target');
			if not os.path.exists(self.__target):
				self.__v('Directory %s not found, trying to create' % self.__target);
				os.mkdir(self.__target);
			self.__v('Checking access in target directory...');
			if not os.access(self.__target, os.W_OK):
				raise Exception('[E] Target directory is not writable!');
		except OSError:
			print('[E] Cannot create target directory');
			sys.exit(2);
		except Exception as err:
			print(err);
			sys.exit(2);

	def __getContent(self, url):
		headers = {'User-agent':'images-downloader'};
		request = urllib.request.Request(url, None, headers);
		fh = urllib.request.urlopen(request);
		charset = fh.info().get_content_charset();
		content = None;
		byteS = fh.read();
		if not charset:
			for charset in ('utf8', 'iso-8859-2', 'iso-8859-1', 'cp1250', 'cp1252'):
				try:
					print('Trying decode %s' % charset);
					content = byteS.decode(charset);
					break;
				except:
					continue;
			if content == None:
				raise Exception('Cannot decode page %s' % url);
		else:
			content = byteS.decode(charset.lower());	
		fh.close();
		return content;

	def __parse(self):
		for url in self.__urls:
			try:
				content = self.__getContent(url);
			except Exception as err:
				print('[E] ' + str(err));
				continue;
			url=urllib.parse.urlparse(url);
			page = "%s://%s" % (url.scheme, url.netloc);
			index = 0;
			while True:
				index = content.find('src="', index);
				if index == -1:
					break;
				index += 5;
				last = content.find('"', index);
				found = content[index:last];
				if not found[0:7] == 'http://':
					if found[0] != '/' and page[-1] != '/':
						page += '/';
					found = page + found;
				self.__v('Found: %s' % found);
				index = last + 1;
				posDot = found.rfind('.');
				ext = found[posDot + 1:];
				name = found[found.rfind('/') + 1:posDot];
				self.__downloadImage(found, name, ext);
				

	def __downloadImage(self, url, name, ext):
		if ext in self.__ext:
			fh = urllib.request.urlopen(url);
			content = fh.read();
			if self.__name:
				name = self.__name;
			path = '%s%s.%s' % (self.__target, name, ext);
			i = 1;
			while os.path.exists(path):
				path = '%s%s-%d.%s' % (self.__target, name, i, ext);
				i += 1;
			if int(self.__amount) == 0:
				img = open(path, 'wb');
				self.__v('Writing image as %s' % path);
				img.write(content);
				img.close();
			if int(self.__amount) > 0 and self.__count < int(self.__amount):
					img = open(path, 'wb');
					self.__v('Writing image as %s' % path);
					img.write(content);
					self.__count += 1;
					img.close();
		else:
			self.__v('Skipping - bad extension of image');
		
		

if __name__ == '__main__':
	try:
		imagesDownloader();
	except KeyboardInterrupt:
		print('[I] Aborting...');
		sys.exit(4);
