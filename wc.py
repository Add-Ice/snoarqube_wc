# coding:utf-8

# two problems
# python wc.py -l testinputs/test-1 -c testinputs/test-3
# 如果输错 是否会读下一个文件   python wc.py -l testinputs/test testinputs/test-3

import argparse
import sys

parser = argparse.ArgumentParser()  # 创建一个解析对象
parser.add_argument("-l", help="number of lines", action="store_true")
parser.add_argument("-w", help="number of words", action="store_true")
parser.add_argument("-c", help="number of bytes", action="store_true")
parser.add_argument("-m", help="number of chars", action="store_true")
parser.add_argument("-L", help="number of bytes", action="store_true")
parser.add_argument("--files0-from",
					help="read input from the files specified by NUL-terminated names in file\nIf F is - then read names from standard input",
					dest="filelist", nargs=1)
parser.add_argument("--version", action='version', version="wc.py (GNU coreutils) 8.22\t"
														   "Copyright (C) 2018 Software Engineering\t"
														   "Written by Jiabin Liu")
parser.add_argument('filenames', metavar='file', help='input files', nargs='*')
args = parser.parse_args()  # 进行解析


def calculate_wc(file_file):
	line_count, word_count, char_count, byte_count, max_line_length = 0, 0, 0, 0, 0
	for count, line in enumerate(file_file):
		line_count += line.count(b'\n')  # calculate lines

		a = line.split()  # calculate words
		word_count += len(a)

		line1 = line.decode('utf-8', 'ignore')  # calculate chars
		char_count += len(line1)

		byte_count += len(line)  # calculate bytes

		length = len(line)  # calculate   max lines length
		utf8_length = len(line.decode('utf-8', 'ignore'))
		real_length = (utf8_length - length) / 2 + length
		max_line_length = max(max_line_length, real_length)
	calculate_dict = (line_count, word_count, char_count, byte_count, max_line_length)
	return calculate_dict


def file_wc(filename):
	calculate_file_wc = ()
	try:
		data = open(filename, 'rb')
		calculate_file_wc = calculate_wc(data)
	except IOError as e:
		print(' No such file or directory', e)
	calculate_file_wc_new = (calculate_file_wc, filename)
	return calculate_file_wc_new


def sum_std_in(std_content):  # tuple 还是 tuple
	data__dict = []
	for content in std_content:
		data__dict.append(content.encode('utf-8'))
	calculate_sum_std_in = calculate_wc(data__dict)
	return calculate_sum_std_in


def each_file_result(flaglists, wc_result, circulation_filename):  # calculate wc of each file
	real_result = ''
	if len(wc_result) == 0:
		real_result = "We don't handle that situation yet!"
	elif len(wc_result) == 1:
		real_result = wc_result[0]
	else:
		if 'l' in flaglists:
			real_result += ('\t%i' % wc_result[0])
		if 'w' in flaglists:
			real_result += ('\t%i' % wc_result[1])
		if 'm' in flaglists:
			real_result += ('\t%i' % wc_result[2])
		if 'c' in flaglists:
			real_result += ('\t%i' % wc_result[3])
		if 'L' in flaglists:
			real_result += ('\t%i' % wc_result[4])
		if circulation_filename or len(wc_result) == 5:
			real_result += ('\t%s' % circulation_filename)
		elif not circulation_filename:  # to show the 'total'
			real_result += ('\t%s' % wc_result[5])
	return real_result


def wc_wc(flaglists, file_names):  # show the final result   for the filename of input
	total_lines, total_words, total_bytes, total_chars, most_max = 0, 0, 0, 0, 0

	for filename in file_names:
		wc_result = file_wc(filename)  # ((line_count, word_count, char_count, byte_count, max_line_length),filename)
		print(each_file_result(flaglists, wc_result[0], filename))

		# calculate total
		if len(wc_result[0]) > 1:
			total_lines += wc_result[0][0]
			total_words += wc_result[0][1]
			total_bytes += wc_result[0][2]
			total_chars += wc_result[0][3]
			if wc_result[0][4] > most_max:
				most_max = wc_result[0][4]

	# print total
	if len(file_names) > 1:
		print(each_file_result(flaglists, (total_lines, total_words, total_bytes, total_chars, most_max, "total"), ''))


def wc_wc_std_in(flaglists, file_names):  # for the std_in
	wc_result = sum_std_in(file_names)
	print(each_file_result(flaglists, wc_result, ''))


def filter_check_flags(args_resolve):
	args_dict = args_resolve.__dict__
	flag_lists = []
	for key, value in args_dict.items():
		if value is True:
			flag_lists.append(key)
	if not flag_lists:
		flag_lists_initial = ['l', 'w', 'c']
		return flag_lists_initial
	else:
		return flag_lists


def files0_from_extract_from_read_std_in(std_in_contents):  # read from --files0-from= std_in
	filename_list = []
	if '\0' not in std_in_contents:
		print(std_in_contents)
		filename_list = ['-']
	else:
		content_list_null = std_in_contents.split('\0')
		for iii in content_list_null:
			real_filename = iii.strip()
			if len(real_filename) > 0:
				filename_list.append(real_filename)
	return filename_list


def files0_from_extract_from_file(command_file):  # read from --files0-from= file
	with open(command_file) as f:
		data = f.read()
		file_namelist = files0_from_extract_from_read_std_in(data)
	return file_namelist


if __name__ == '__main__':
	dict_new = vars(args)
	# print(dict_new)  # show real args
	# print(dict_new['filenames'] == ['-'])
	# print(flags_filter(args))
	# pre_args = parser.parse_args(pre_process_sys_argv())

	if args.filenames and args.filelist:
		print('file operands cannot be combined with --files0-from')

	elif args.filenames:
		try:
				wc_wc(filter_check_flags(args), args.filenames)
		except IOError as e:  # IOError失败
			print('wc.py' + args.filenames + ': No such file or directory')

	elif args.filelist:
		try:
			new_list = args.filelist
			file_names_new = []
			if len(new_list) == 1 and len(new_list) == new_list.count('-'):  # 从 --files0-from=- 标准输入读取
				input_content = sys.stdin.read()
				file_names_new = files0_from_extract_from_read_std_in(input_content)

			else:
				file_names_new = files0_from_extract_from_file(new_list[0])  # 从 --files0-from=  文件名读取
			wc_wc(filter_check_flags(args), file_names_new)
		except IOError as e:
			error_name = "".join(args.filelist)
			print('wc.py: cannot open \'' + error_name + '\' for reading: No such file or directory')

	elif len(dict_new['filenames']) == 0 or dict_new['filenames'] == ['-']:  # python wc.py -   报错
		standard_input_content = sys.stdin.readlines()  # 从标准输入读取  计算wc
		if filter_check_flags(args) == ['l', 'w', 'c']:
			wc_wc_std_in(filter_check_flags(args), standard_input_content)
		else:
			print(each_file_result(filter_check_flags(args), sum_std_in(standard_input_content), ''))
