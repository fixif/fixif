import sys

sys.path.append("/home/lauter/pythonsollya-install/lib/python2.7/site-packages")

import sollya

sollya.execute("gabarit.sol")

check_modulus_filter_in_specification = sollya.parse("checkModulusFilterInSpecification")
present_results = sollya.parse("presentResults")

