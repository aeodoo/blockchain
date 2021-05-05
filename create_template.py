from cert_tools import create_v2_certificate_template as create_tmpl

from params import Template

config = Template()
create_tmpl.write_certificate_template(config)
