import logging
import os
import re
import shutil
import subprocess

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    @api.depends("is_blockchain_certification", "state", "blockchain_published")
    def _compute_blockchain_controls_visible(self):
        for survey_id in self:
            if not survey_id.is_blockchain_certification:
                survey_id.blockchain_controls_visible = False
            elif survey_id.is_blockchain_certification and survey_id.state != "closed":
                survey_id.blockchain_controls_visible = False
            elif (
                survey_id.is_blockchain_certification
                and survey_id.state == "closed"
                and not survey_id.blockchain_published
            ):
                survey_id.blockchain_controls_visible = True
            else:
                survey_id.blockchain_controls_visible = False

    blockchain_controls_visible = fields.Boolean(
        compute="_compute_blockchain_controls_visible", store=True
    )
    is_blockchain_certification = fields.Boolean("Is blockchain certification")
    blockchain_published = fields.Boolean("Published on blockchain", default=False)

    @api.model
    def get_valid_filename(self, file_name):
        s = str(file_name).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", s)

    def action_create_template(self):
        for survey_id in self:
            survey_id.certification_badge_id.action_create_template()

    def get_user_inputs(self):
        return self.env["survey.user_input"].search(
            [
                ("survey_id", "=", self.id),
                ("test_entry", "=", False),
                ("quizz_passed", "=", True),
            ]
        )

    def create_current_roster(self, path):
        roster_filename = (
            path
            + os.sep
            + self.get_valid_filename(self.certification_badge_id.name)
            + ".csv"
        )
        if os.path.exists(roster_filename):
            os.remove(roster_filename)

        f = open(roster_filename, "a")
        f.write("name,pubkey,identity\n")
        user_input_ids = self.get_user_inputs()
        if not user_input_ids:
            raise ValidationError(_("No users has passed the exam"))
        for user_input_id in user_input_ids:
            partner_id = user_input_id.partner_id
            if not partner_id or not partner_id.public_address or not partner_id.email:
                raise ValidationError(
                    _(
                        "Partner {} {} must have filled name, email and public address"
                    ).format(partner_id.id, partner_id.name)
                )
            f.write(
                "{},{},{}\n".format(
                    partner_id.name.replace(",", " "),
                    partner_id.public_address,
                    partner_id.email,
                )
            )
        f.close()
        return roster_filename

    def prepare_configuration_issuer(self, path):
        unsigned_certificates_dir = path + os.sep + "unsigned_certificates_dir"
        blockchain_certificates_dir = path + os.sep + "blockchain_certificates_dir"
        signed_certificates_dir = path + os.sep + "signed_certificates_dir"
        if not os.path.exists(unsigned_certificates_dir):
            raise ValidationError(_("You must instantiate templates"))
        if os.path.exists(blockchain_certificates_dir):
            shutil.rmtree(blockchain_certificates_dir, ignore_errors=True)
        os.makedirs(blockchain_certificates_dir)
        if os.path.exists(signed_certificates_dir):
            shutil.rmtree(signed_certificates_dir, ignore_errors=True)
        os.makedirs(signed_certificates_dir)
        work_dir = path + os.sep + "work_dir"
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)
        os.makedirs(work_dir)
        key_filename = path + os.sep + "key_file.ini"
        if os.path.exists(key_filename):
            os.remove(key_filename)

        f = open(key_filename, "a")
        f.write(self.env.company.issuer_key.lower())
        f.close()

    def sign_and_send_certificates(self):
        if self.blockchain_published:
            return
        abs_path = os.path.abspath(self.env.company.data_dir)
        user_input_ids = self.get_user_inputs()
        args = [
            "python",
            self.env.company.blockcert_path
            + os.sep
            + "cert-issuer"
            + os.sep
            + "cert_issuer",
            "-m cert_issuer",
            "--issuing_address=" + self.env.company.issuer_public_key.lower(),
            "--key_file=key_file.ini",
            "--usb_name=" + abs_path,
            "--unsigned_certificates_dir="
            + os.path.join(abs_path, "unsigned_certificates_dir"),
            "--signed_certificates_dir="
            + os.path.join(abs_path, "signed_certificates_dir"),
            "--blockchain_certificates_dir=" + os.path.join(abs_path, "work_dir"),
            "--chain=" + self.env.company.environment,
            "--no_safe_mode=True",
            "--gas_limit=" + str(self.env.company.gas_limit or 40000),
        ]
        if self.env.company.etherscan_api_token:
            args.append("--etherscan_api_token" + self.env.company.etherscan_api_token)
        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, universal_newlines=True,
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
        if return_code == 0:
            user_input_ids.write({"blockchain_published": True})
            self.blockchain_published = True

    def action_sign_and_send_certificates(self):
        abs_path = os.path.abspath(self.env.company.data_dir)
        for survey_id in self:
            user_input_ids = survey_id.get_user_inputs()
            if not user_input_ids:
                raise ValidationError(_("No users has passed the exam"))
            self.prepare_configuration_issuer(abs_path)
            survey_id.with_delay().sign_and_send_certificates()

    def action_unpublish(self):
        for survey_id in self:
            user_input_ids = survey_id.get_user_inputs()
            if not user_input_ids:
                raise ValidationError(_("No users has passed the exam"))
            user_input_ids.write({"blockchain_published": False})
            survey_id.blockchain_published = False

    def action_instantiate_template(self):
        abs_path = os.path.abspath(self.env.company.data_dir)
        if not os.path.exists(abs_path):
            raise ValidationError(_("You must create a valid template first"))

        template_dir = os.path.join(abs_path, "template_dir")
        if not os.path.exists(template_dir):
            raise ValidationError(_("You must create a valid template first"))

        unsigned_certificates_dir = os.path.join(abs_path, "unsigned_certificates_dir")
        if not os.path.exists(unsigned_certificates_dir):
            os.makedirs(unsigned_certificates_dir)

        for survey_id in self:
            badge_file_name = (
                abs_path
                + os.sep
                + self.get_valid_filename(
                    survey_id.certification_badge_id.name + ".png"
                )
            )
            if not os.path.exists(badge_file_name):
                raise ValidationError(_("You must create a valid template first"))
            roster_filename = survey_id.create_current_roster(abs_path)
            process = subprocess.Popen(
                [
                    "python",
                    self.env.company.blockcert_path
                    + os.sep
                    + "cert-tools"
                    + os.sep
                    + "cert_tools"
                    + os.sep
                    + "instantiate_v2_certificate_batch.py",
                    "--data_dir=" + abs_path,
                    "--issuer_certs_url=" + self.env.company.issuer_certs_url,
                    "--template_dir=" + template_dir,
                    "--template_file_name="
                    + self.get_valid_filename(survey_id.certification_badge_id.name),
                    "--unsigned_certificates_dir="
                    + os.path.join(abs_path, "unsigned_certificates_dir"),
                    "--roster=" + roster_filename,
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

    @api.onchange("is_blockchain_certification")
    def on_change_is_blockchain_certification(self):
        for record in self:
            if record.is_blockchain_certification:
                record.is_time_limited = True
                record.questions_selection = "all"
                record.users_can_go_back = True
                record.scoring_type = "scoring_with_answers"
                record.passing_score = 90
                record.certificate = True
                if not record.certification_mail_template_id:
                    record.certification_mail_template_id = record.env.ref(
                        "survey.mail_template_certification"
                    )
                record.certification_give_badge = True
                record.access_mode = "token"
                record.users_login_required = True
                record.is_attempts_limited = True
