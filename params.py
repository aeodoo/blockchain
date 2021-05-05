import os
from cert_core import Chain

# base path to data directory
DATA_PATH = '../data'


class Template:
    def __init__(self):
        # issuer information
        self.issuer_url = 'https://www.aeodoo.org'
        self.issuer_email = 'certification@aeodoo.org'
        self.issuer_name = 'AEOdoo'
        # https://github.com/blockchain-certificates/cert-issuer/blob/master/examples/issuer/profile.json
        self.issuer_id = 'http://localhost:8080/issuer-testnet.json'
        # https://github.com/blockchain-certificates/cert-issuer/blob/master/examples/issuer/revocation-list.json
        self.revocation_list = 'http://localhost:8080/revocation-list-testnet.json'
        self.issuer_signature_lines = [{
            "job_title": "AEOdoo Issuer",
            "signature_image": "images/issuer-signature.png",
            "name": "AEOdoo signature"
        }]

        # ropsten
        self.issuer_public_key = 'ecdsa-koblitz-pubkey:0xBbF4f8158117CE8c20B12683a80F0301f542A555'

        # goerli
        # self.issuer_public_key = 'ecdsa-koblitz-pubkey:0x7a2e484941128Cb81B71746d4697bf948a121977'

        # certificate information
        self.certificate_description = "Lorem ipsum dolor sit amet, mei docendi concludaturque ad, cu nec partem " \
                                       "graece. " \
                                       "Est aperiam consetetur cu, expetenda moderatius neglegentur ei nam, " \
                                       "suas dolor laudem eam an."
        self.certificate_title = 'Certificate of Accomplishment'
        self.criteria_narrative = 'Nibh iriure ei nam, modo ridens neglegentur mel eu. At his cibo mucius.'

        # https://community.blockcerts.org/t/how-to-generate-my-own-certificate-using-cert-tool/211/7
        self.badge_id = '82a4c9f2-3588-457b-80ea-da695571b8fc'  # Issuer Guid (generated with uuid4())

        self.display_html = None
        self.hash_emails = False
        self.additional_global_fields = None
        self.additional_per_recipient_fields = None

        # base data dir
        self.abs_data_dir = DATA_PATH

        # images
        self.issuer_logo_file = 'images/logo.png'
        self.cert_image_file = 'images/certificate-image.png'
        self.issuer_signature_file = 'images/issuer-signature.png'

        # template output directory
        self.template_dir = 'certificate_templates'
        self.template_file_name = 'aeodoo1_v2.json'

        ## instanciate fields
        self.filename_format = 'uuid'
        self.unsigned_certificates_dir = 'unsigned_certificates'


class Issuer:
    def __init__(self):
        # mainnet
        # self.chain = Chain.parse_from_chain('ethereum_mainnet')
        # # self.ethereum_rpc_url = 'localhost:8545'
        # self.issuing_address = '0x0000000000000000000000000000000000000000'
        # self.key_file = 'aeodoo_mainnet.key'

        # ropsten
        self.chain = Chain.parse_from_chain('ethereum_ropsten')
        # self.ropsten_rpc_url = 'localhost:8545'
        self.issuing_address = '0xBbF4f8158117CE8c20B12683a80F0301f542A555'
        self.key_file = 'aeodoo_ropsten.key'

        # goerli
        # self.chain = Chain.parse_from_chain('ethereum_goerli')
        # self.goerli_rpc_url = 'https://goerli-light.eth.linkpool.io'
        # #self.goerli_rpc_url = 'https://rpc.slock.it/goerli'
        # self.issuing_address = '0x7a2e484941128Cb81B71746d4697bf948a121977'
        # self.key_file = 'aeodoo_goerli.key' #

        ################################
        # transaction params
        self.gas_limit = 25000
        self.gas_price = 20000000000

        # path to private keys folder
        self.usb_name = os.path.join(DATA_PATH, 'keys')

        # put your unsigned certificates here for signing.
        self.unsigned_certificates_dir = os.path.join(DATA_PATH, 'unsigned_certificates')

        # where to store intermediate files, for debugging and checkpointing.
        self.work_dir = os.path.join(DATA_PATH, 'tmp')
        self.signed_certificates_dir = os.path.join(self.work_dir, 'signed_certificates')

        # final blockchain certificates output.
        self.blockchain_certificates_dir = os.path.join(DATA_PATH, 'blockchain_certificates')

        # other params
        self.safe_mode = False
        self.max_retry = 10
