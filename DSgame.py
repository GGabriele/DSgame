import re
import pprint

# Defining REGEX.
regex = "(?P<number>.+)?\(.*\).*"
regex1 = "(?P<pc_number>.+)\(.*\sLACP\(a\)\s(?P<port_number>.+)\(.+\)\n"

# Dictionary holding final data.	
diagram = {}

# Open portchannel.txt file, where command output is stored.
with open("portchannel.txt", 'r') as f:
	for line in f:
		match_portchannel = re.match(regex1, line, re.DOTALL)
		match_port = re.match(regex, line, re.DOTALL)

		# If there is a match, the line contains the Port-channel ID
		if match_portchannel:
			group_pc = match_portchannel.groupdict()
			portchannel_number = group_pc["pc_number"]
			port_number = group_pc["port_number"]
			ports = port_number.split()

			# If multiple ports belong to the PoX.
			if len(ports) > 1:
				port_number = []
				for port in ports:
					match_port = re.match(regex, port, re.DOTALL)
					if match_port:
						group_port = match_port.groupdict()
						port = group_port["number"]
						port_number.append(port)
			diagram[portchannel_number] = port_number
		
		# While if only the second regex matches, ports belong to the last Port-channel.
		elif match_port:
			ports = line.split()
			port_number = diagram[portchannel_number]
			for port in ports:
					match_regex = re.match(regex, port, re.DOTALL)
					if match_regex:
						group_port = match_regex.groupdict()
						port = group_port["number"]
						port_number.append(port)
			diagram[portchannel_number] = port_number
		else:
			pass

	# Pretty printing the I-hope-it-is-good-output.
	pretty = pprint.PrettyPrinter(indent=2, depth=10).pprint
	pretty(diagram)	
