# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Odoo Blockchain proxy",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Odoo proxy to AEOdoo Certification",
    "author": "Dario Lodeiros (CommitSun), "
    "Eric Antones (NuObit) ,"
    "Fernando La Chica (Guadaltech), "
    "Odoo Community Association (OCA)",
    "website": "https://githut.com/aeodoo/blockhain",
    "depends": [
        "blockchain_cert",
        "event",
        "survey",
        "event_sale",
        "website_event_sale",
        "auth_metamask",
    ],
    "data": [
        "views/survey_survey.xml",
        "views/event_event.xml",
        "views/bc_certification_template.xml",
        "views/website_templates.xml",
        "views/res_partner.xml",
    ],
    "application": True,
    "development_status": "Alpha",
}
