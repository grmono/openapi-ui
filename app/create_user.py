import sys, argparse
from definitions.request_models import *
from database.db_handler import *


def main(args):
	tenant_info = CreateTenant(**args)
	if TenantManagement().create_tenant(tenant_info):
		print("Created account succesfully")
	else:
		print("Account already exists")



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-username", dest="username", action="store", required=True)
	parser.add_argument("-password", dest="password", action="store", required=True)
	parser.add_argument("-role", dest="role", action="store", required=False)
	parser.add_argument("-email", dest="email", action="store", required=False)
	parser.add_argument("-firstname", dest="firstname", action="store", required=False)
	parser.add_argument("-lastname", dest="lastname", action="store", required=False)
	try:
		main(vars(parser.parse_args()))
	except KeyboardInterrupt:
		sys.exit(0)
