import platform

function_declartation_pattern = r'^(\w+\s*\**\s*\w+\((?:.*)\))\s*\{*$'

host_system = platform.system()
cpp_files_mimetype = "text/x-c++src"
if host_system == "Windows":
    cpp_files_mimetype = "text/plain"
