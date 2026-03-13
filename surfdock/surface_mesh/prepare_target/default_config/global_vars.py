# global_vars.py: Global variables used by MaSIF -- mainly pointing to environment variables of programs used by MaSIF.
# Pablo Gainza - LPDI STI EPFL 2018-2019
# Released under an Apache License 2.0

import os 
from IPython.core.debugger import set_trace
epsilon = 1.0e-6
import sys

# Absolute paths inside container
msms_bin = "/workspace/surfdock/surface_mesh/tools/transfer/APBS-3.4.1.Linux/bin/msms"
pdb2pqr_bin = "/workspace/surfdock/surface_mesh/tools/transfer/pdb2pqr-linux-bin64-2.1.1/pdb2pqr"
apbs_bin = "/workspace/surfdock/surface_mesh/tools/transfer/APBS-3.4.1.Linux/bin/apbs"
multivalue_bin = "/workspace/surfdock/surface_mesh/tools/transfer/APBS-3.4.1.Linux/share/apbs/tools/bin/multivalue"

for name, path in [
    ("MSMS_BIN", msms_bin),
    ("PDB2PQR_BIN", pdb2pqr_bin),
    ("APBS_BIN", apbs_bin),
    ("MULTIVALUE_BIN", multivalue_bin),
]:
    if not os.path.isfile(path):
        print(f"ERROR: {name} not found at {path}")
        exit(1)
    os.environ[name] = path

# os.environ['MSMS_BIN']= "~/Documents/bachelor_project/docker_pipeline/surfdock/surface_mesh/tools/transfer/APBS-3.4.1.Linux/bin/msms"
# if 'MSMS_BIN' in os.environ:
#    msms_bin = os.environ['MSMS_BIN']
# else:
#   set_trace()
#   print("ERROR: MSMS_BIN not set. Variable should point to MSMS program.")
#   sys.exit(1)
#
# os.environ['PDB2PQR_BIN']="/Documents/bachelor_project/docker_pipeline/surfdock/surface_mesh/tools/transfer/pdb2pqr-linux-bin64-2.1.1/pdb2pqr"
# if 'PDB2PQR_BIN' in os.environ:
#    pdb2pqr_bin = os.environ['PDB2PQR_BIN']
# else:
#   print("ERROR: PDB2PQR_BIN not set. Variable should point to PDB2PQR_BIN program.")
#   sys.exit(1)
# os.environ['APBS_BIN']="/Documents/bachelor_project/docker_pipeline/surfdock/surface_mesh/tools/transfer/APBS-3.4.1.Linux/bin/apbs"
# if 'APBS_BIN' in os.environ:
#    apbs_bin = os.environ['APBS_BIN']
# else:
#   print("ERROR: APBS_BIN not set. Variable should point to APBS program.")
#   sys.exit(1)
# os.environ['MULTIVALUE_BIN']="/Documents/bachelor_project/docker_pipeline/surfdock/surface_mesh/tools/transfer/APBS-3.4.1.Linux/share/apbs/tools/bin/multivalue"
# if 'MULTIVALUE_BIN' in os.environ:
#    multivalue_bin = os.environ['MULTIVALUE_BIN']
# else:
#   print("ERROR: MULTIVALUE_BIN not set. Variable should point to MULTIVALUE program.")
#   sys.exit(1)

class NoSolutionError(Exception):
    pass
# global_vars.py: Global variables used by MaSIF -- mainly pointing to environment variables of programs used by MaSIF.
# Pablo Gainza - LPDI STI EPFL 2018-2019
# Released under an Apache License 2.0
