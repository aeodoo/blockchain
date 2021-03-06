import base64
import logging
import os
import subprocess

from odoo import _, fields, models
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)


class GamificationBadge(models.Model):
    _inherit = "gamification.badge"

    criteria_narrative = fields.Html("Criteria Narrative", translate=True)

    def action_create_template(self):
        survey_class = self.env["survey.survey"]
        abs_path = os.path.abspath(self.env.company.data_dir)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        template_dir = os.path.join(abs_path, "template_dir")
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)

        for badge_id in self:
            if not badge_id.image_1920:
                raise ValidationError(_("Your badget must have image"))
            badge_file_name = (
                abs_path
                + os.sep
                + survey_class.get_valid_filename(badge_id.name + ".png")
            )
            with open(badge_file_name, "wb") as badge_image_file:
                badge_image_file.write(base64.b64decode(badge_id.image_1920))

            issuer_file_name = (
                abs_path
                + os.sep
                + survey_class.get_valid_filename(self.env.company.name + ".png")
            )
            with open(issuer_file_name, "wb") as issuer_image_file:
                issuer_image_file.write(base64.b64decode(self.env.company.logo))

            process = subprocess.Popen(
                [
                    "python",
                    self.env.company.blockcert_path
                    + os.sep
                    + "cert-tools"
                    + os.sep
                    + "cert_tools"
                    + os.sep
                    + "create_v2_certificate_template.py",
                    "--data_dir=" + abs_path,
                    "--template_dir=" + template_dir,
                    "--template_name=" + badge_id.name,
                    "--template_file_name="
                    + survey_class.get_valid_filename(badge_id.name),
                    "--issuer_email=" + self.env.company.email or "",
                    "--issuer_name=" + self.env.company.name or "",
                    "--issuer_id=" + self.env.company.issuer_id or "",
                    "--issuer_key=" + self.env.company.issuer_key.lower() or "",
                    "--issuer_public_key=" + self.env.company.issuer_public_key.lower()
                    or "",
                    "--issuer_url=" + self.env.company.issuer_certs_url,
                    "--certificate_title=" + badge_id.name or "",
                    "--criteria_narrative=" + badge_id.criteria_narrative or "",
                    "--badge_id=" + str(badge_id.id),
                    "--certificate_description=" + str(badge_id.description),
                    "--cert_image_file=" + badge_file_name,
                    "--issuer_logo_file=" + issuer_file_name,
                ],
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

            while True:
                output = process.stdout.readline()
                log_line = output.strip()
                if log_line:
                    logger.info(log_line)
                return_code = process.poll()
                if return_code is not None:
                    logger.info(_("RETURN CODE: ") + str(return_code))
                    for output in process.stdout.readlines():
                        logger.info(output.strip())
                    break
