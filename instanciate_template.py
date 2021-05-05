from cert_tools import instantiate_v2_certificate_batch as inst_templ


def get_recipients_from_roster(config):
    rosters = [
        {'name': 'Satoshi Nakamoto',
         'pubkey': 'ecdsa-koblitz-pubkey:0x25B8dfbB23C818Eab79e36Ce867D5C60a884370F',
         'identity': 'satoshi@blockchain.org',
         },
        {'name': 'Gavin Wood',
         'pubkey': 'ecdsa-koblitz-pubkey:0xC0618aBA0a469C474Fc8e77FA984e39612F66d86',
         'identity': 'gavin@blockchain.org',
         },
        {'name': 'Vitalik Buterin',
         'pubkey': 'ecdsa-koblitz-pubkey:0xa164D4bAeD040B0Cd6EbeF830cFdAF0b3b376723',
         'identity': 'vitalik@blockchain.org',
         },
    ]
    recipients = map(lambda x: inst_templ.Recipient(x), rosters)
    return list(recipients)


inst_templ.get_recipients_from_roster = get_recipients_from_roster

from params import Template

config = Template()
inst_templ.instantiate_batch(config)
