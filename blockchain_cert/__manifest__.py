# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Konos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "BlockChain Certification",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Ethereum Certification AEOdoo",
    "author": "Dario Lodeiros (CommitSun), "
    "Fernando La Chica (Guadaltech), "
    "Eric Antones (NuObit) ,"
    "Odoo Community Association (OCA)",
    "website": "https://githut.com/OCA/helpdesk",
    "depends": ["base",],
    "data": [
        "data/bc_certification_data.xml",
        "security/blockchain_cert_security.xml",
        "security/ir.model.access.csv",
        "views/bc_certification.xml",
        "views/bc_certification_template.xml",
        "views/bc_issuer.xml",
        "views/bc_certification_menu.xml",
    ],
    "application": True,
    "development_status": "Alpha",
}
