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
    "external_dependencies": {"python": ["cert-issuer==2.0.27", "cert-tools==3.0.0a2"]},
    "depends": [
        "event",
        "gamification",
        "survey",
        "event_sale",
        "website_event_sale",
        "auth_metamask",
    ],
    "data": [
        "security/survey_security.xml",
        "views/gamification_badge_views.xml",
        "views/survey_survey_views.xml",
        "views/survey_user_input_views.xml",
        "views/event_event_views.xml",
        "views/website_templates.xml",
        "views/res_partner_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "application": True,
    "development_status": "Alpha",
}
