#!/usr/bin/env python3
import sys
import shlex
import subprocess
from collections import deque
import pathlib
import shutil

base_dll_paths = [pathlib.Path("/usr/i686-w64-mingw32/sys-root/mingw/bin/"),
			pathlib.Path("/usr/i686-w64-mingw32/sys-root/bin/")]
current_directory = pathlib.Path(".")
get_header_command = "i686-w64-mingw32-objdump -p {} | grep 'DLL Name:' | sed -e 's/\t*DLL Name: //g'"
sanitize_dll_substitute = shlex.quote

temp_paths = []
for base_dll_path in base_dll_paths:
	if not base_dll_path.exists():
		print("base_dll_path doesn't exist, ignoring: {}".format(base_dll_path))
	else:
		temp_paths.append(base_dll_path)
base_dll_paths = temp_paths

dlls_notfound = set()
dlls_found = set()
in_progress = deque()
dlls_handled = set()

for target in sys.argv[1:]:
	if target not in dlls_handled:
		in_progress.appendleft(target)
		dlls_handled.add(target)

while True:
	try:
		elem = in_progress.pop()
	except IndexError:
		print("Queue empty, halting.")
		break
	print("Scanning {}".format(elem))
	subproc = subprocess.run(get_header_command.format(sanitize_dll_substitute(elem)),
					shell=True, text=True, capture_output=True)
	dependencies = shlex.split(subproc.stdout)
	for dll in dependencies:
		if dll not in dlls_handled:
			dlls_handled.add(dll)
			for base_dll_path in base_dll_paths:
				dll_path = base_dll_path / dll
				if dll_path.exists():
					print("{} found, copying...".format(dll))
					dlls_found.add(dll)
					shutil.copyfile(dll_path, current_directory / dll)
					in_progress.appendleft(dll)
			if dll not in dlls_found:
				print("{} not found".format(dll))
				dlls_notfound.add(dll)
		else:
			print("{}, skipping".format(dll))

print("Not found: {}".format(dlls_notfound))
