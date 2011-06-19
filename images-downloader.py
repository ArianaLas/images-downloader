#!/usr/bin/python
# coding=utf-8

import urllib.request, sys, getopt, platform;

class imagesDownloader:
	__urls = '';
	__name = 'img';
	__ext = 'jpg';
	__target = '';
	__amount = None;
	__recursive = False;
	__depth = None;
	__verbose = False;
	__sep = '/';

	def __init__(self):
		if platform.system().lower() == 'windows':
			self.__sep = '\\';
		try:
			options, args = getopt.getopt((sys.argv[1:]),
			'n:e:t:a:rd:hv',
			['name=', 'extension=', 'target-dir=', 'amount=', 'recursive', 'depth', 'help', 'verbose']);
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
				self.__target = value;
			elif option in ('-a', '--amount'):
				self.__v('Setting amount of images to download as %s' % value);
				self.__amount = value;
			elif option in ('-r', '--recursive'):
				self.__v('Setting option recursive searching');
				self.__recursive = True;
			elif option in ('-d', '--depth'):
				self.__v('Setting depth of recursive searching as %s' % value);
				self.__depth = value;
			elif option in ('-h', '--help'):
				self.__usage();
				sys.exit(0);
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
		self.__parse();
	
	def __v(self, text):
		print('[I] %s...' % text);
	
	def __usage(self):
		print('========== IMAGE-DOWNLOADER ==========');
		print('Automatically searching and downloading images from web pages');
		print('Author: Ariana Las <ariana.las@gmail.com>');
		print('\n[E] <- Error\n[W] <- Warning\n[I] <- Information\n');
		print('Usage:\timages-downloader [options] url(s)');
		print('\t-n --name\n\t\timage name (default is img - if more: img, img-1, img-2...)');
		print('\t-e --extension\n\t\timage extension (default is jpg)\n\t\tif need various, use "," for example: -e jpg,png,gif');
		print('\t-t --target-dir\n\t\ttarget directory to write downloaded images\n\t\t(default current directory)');
		print('\t-a --amount\n\t\tmaximum amount of images to download (default all)');
		print('\t-r --recursive\n\t\trecursive searching in pages');
		print('\t-d --depth\n\t\tdepth of recursion (default max)');
		print('\t-h --help\n\t\tdisplay help');

	def __getContent(self, url):
		fh = urllib.request.urlopen(url);
		charset = fh.info().get_content_charset();
		if not charset:
			charset="utf8";
		content = fh.read().decode(charset);	
		fh.close();
		return content;

	def __parse(self):
		for url in self.__urls:
			content = self.__getContent(url);
			url=urllib.parse.urlparse(url);
			page = "%s://%s" % (url.scheme, url.netloc);
			print("Page: %s" % page);
			index = 0;
			while True:
				index = content.find('<img src="', index);
				if index == -1:
					break;
				index += 10;
				last = content.find('"', index);
				found = content[index:last];
				# TODO: detect !absolute path
				print("Found: %s" % found);
				index = last + 1;
				

	#def __downloadImage(self, url):
		

if __name__ == '__main__':
	try:
		imagesDownloader();
	except KeyboardInterrupt:
		print('[I] Aborting...');
		sys.exit(4);
