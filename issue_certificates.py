import sys

# TODO: fix cert-issuer installation dependency errors
#  in the meantime define here the path to cert-issuer root directory
sys.path.append('../lib/cert-issuer')

from cert_issuer import config, issue_certificates
from cert_issuer.blockchain_handlers import ethereum

from params import Issuer

import logging

logging.basicConfig(level=logging.DEBUG)

app_config = Issuer()
certificate_batch_handler, transaction_handler, connector = ethereum.instantiate_blockchain_handlers(app_config)
res = issue_certificates.issue(app_config, certificate_batch_handler, transaction_handler)

print(f"Transaction ID: {res}")
