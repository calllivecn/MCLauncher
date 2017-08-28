#!/usr/bin/env python3
#coding=utf-8

LAUNCHER = r'MCL'
LAUNCHER_version = r'0.1'

MC_CONFIG = 'MCLauncher.json'

import json,os,sys
from urllib.parse import urlsplit
from uuid import uuid4
from argparse import ArgumentParser
from subprocess import check_call

#from pprint import pprint



#########################
#
#
# 函数定义 start
#
#
#########################

ossep = os.sep
pathsep = os.path.pathsep
exists = os.path.exists
isdir = os.path.isdir
abspath = os.path.abspath
pathsplit = os.path.split

def get_json(f):
	with open(f) as fp:
		data = json.load(fp)
	return data

def set_json(obj,f):
	with open(MC_CONFIG,'w') as fp:
	 	data = json.dump(obj,fp)
	return data

def get_uuid():
	return uuid4().hex

def get_Duser_home():
	abs_path , _ = pathsplit(abspath(sys.argv[0]))
	return abs_path

class MCL:
	username = ''
	Duser_home = ''
	gameDir = '.minecraft'
	game_version = '' # __get_game_version()
	json_path = ''

	Djava_library_path = ''
	Duser_home = ''

	jvm_args = ''
	cp_args = ''
	minecraft_args = ''

	# 取消jvm内存设置 '-Xmn{min_mem}m -Xmx{max_mem}m'\
	jvm_cmd = 'java -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow '\
	'-Djava.library.path={Djava_library_path} '\
	'-Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true '\
	'-Duser.home={Duser_home} ' # .format(**jvm_args)

	cp_cmd = '-cp {} '

	minecraft_cmd = 'net.minecraft.client.main.Main '\
	'--username {username} '\
	'--version "{launcher_version}" '\
	'--gameDir {gameDir} '\
	'--assetsDir {assetsDir} '\
	'--assetIndex {master_version} '\
	'--uuid {uuid} '\
	'--accessToken {uuid} '\
	'--userType {userType} '\
	'--versionType "{versionType}" '\
	'--height {height} --width {width} ' # .format(**minecraft_args)


	def __init__(self,username,uuid,Duser_home):
		
		self.username = username
		self.uuid_and_token = uuid
		self.Duser_home = Duser_home

		self.__get_gameDir()
		self.__get_assetsDir()
		self.__get_game_version()
		self.__get_master_version()
		self.__get_Djava_library_path()
		

		self.jvm_args = {'Djava_library_path': self.Djava_library_path ,'Duser_home': self.Duser_home }
		self.__get_classpath()
		self.minecraft_args = {'username': self.username ,
					'launcher_version': LAUNCHER_version ,
					'gameDir': '.' + ossep + self.gameDir ,
					'assetsDir': self.assetsDir ,
					'master_version': self.master_version ,
					'uuid': self.uuid_and_token ,
					'assessToken': self.uuid_and_token ,
					'userType': 'Legacy' ,
					'versionType': LAUNCHER + LAUNCHER_version ,
					'height': 480 , # height ,
					'width': 800 , # widht 
					}

		self.launcher_cmd = self.jvm_cmd.format(**self.jvm_args) + self.cp_cmd.format(self.cp_args) + self.minecraft_cmd.format(**self.minecraft_args)

	def launcher(self):
		print(self.launcher_cmd)
		check_call(self.launcher_cmd,shell=True)


	
	def __get_gameDir(self):
		
		#gamedir = self.Duser_home + ossep + self.gameDir

		if exists(self.gameDir):
			pass
		else:
			print('游戏目录不存在:',self.gameDir)
		
	def __get_game_version(self):
		versions_path = self.gameDir + ossep + 'versions'
		for version in os.listdir(versions_path):
			if isdir(versions_path + ossep + version):
				self.game_version = version # 差多个版本的筛选情况
			else:
				print('没有找到versions目录')
				exit(1)

	def __get_Djava_library_path(self):
		self.Djava_library_path = '.' + ossep + self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '-natives'
		print(self.Djava_library_path,file=sys.stderr)
	
	def __get_assetsDir(self):
		self.assetsDir = '.' + ossep + self.gameDir + ossep + 'assets'

	def	__get_master_version(self):
		tmp = self.game_version.split('.')	
		self.master_version = tmp[0] + '.' + tmp[1]

	def __get_classpath(self):
	
		def get(tmp):
			url = tmp.get('url')
			size = tmp.get('size')
			sha1 = tmp.get('sha1')
			tmp2 = urlsplit(url).path
			tmp2 = tmp2.replace('/',ossep)
			return tmp2
	
		json_path = self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '.json'
		
		libraries = get_json(json_path)
	
		minecraftArghuments = libraries.get('minecraftArguments')
		
		### 解析jar库路径
		jar_path = libraries.get('libraries')
		cp_path = []
		for class_jar_info in jar_path:
			tmp = class_jar_info.get('downloads')
	
			if tmp :
				tmp = tmp.get('artifact')
				if tmp :
					tmp2 = get(tmp)
					cp_path.append(self.gameDir + ossep + 'libraries' + tmp2)
		
		cp=''
		for cp_class in cp_path:
			if exists(cp_class):
				cp += '.' + ossep + cp_class + pathsep
			else:
				print('不存在',cp_class)

		self.cp_args = cp + '.' + ossep + self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '.jar'


#########################
#
#
# 函数定义 end 
#
#
#########################



#########################
#
# 参数解析 argparse start
#
#########################
def parse_args():
	parse = ArgumentParser(description='一个MC启动器',usage=' Using : %(prog)s [-u|--username] [-U|--uuid]',epilog='http://www.none.org')

	#parse.add_argument()


#########################
#
# 参数解析 argparse end
#
#########################





####### testing
class args:
	username = 'test'
	uuid = '73c3632b225043f3b9adfe2387841926'


###### testing 





def main():

	Duser_home = get_Duser_home()
	os.chdir(Duser_home)

	if exists(MC_CONFIG):
		user_data = get_json(MC_CONFIG)
		username = user_data.get('username')
		uuid = user_data.get('uuid')
	else:
		username = args.username
		if args.uuid:
			uuid = args.uuid
		else:
			uuid = __get_uuid()
		user_data = {'username' : username ,'uuid' : uuid}
		set_json(user_data,MC_CONFIG)

	mclauncher = MCL(username,uuid,Duser_home)
	mclauncher.launcher()



if __name__ == "__main__":
	main()
