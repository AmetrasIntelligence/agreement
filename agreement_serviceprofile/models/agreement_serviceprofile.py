# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class AgreementServiceProfile(models.Model):
    _name = "agreement.serviceprofile"
    _inherit = "mail.thread"
    _description = "Agreement Service Profiles"

    def _default_stage_id(self):
        return self.env.ref("agreement_serviceprofile.servpro_stage_draft")

    name = fields.Char(required=True)
    stage_id = fields.Many2one(
        "agreement.stage",
        string="Stage",
        default=_default_stage_id,
        copy=False,
        group_expand="_read_group_stage_ids",
    )
    agreement_id = fields.Many2one("agreement", string="Agreement", ondelete="cascade")
    active = fields.Boolean(
        default=True,
        help="If unchecked, it will allow you to hide this service profile "
        "without removing it.",
    )

    notes = fields.Text()
    product_id = fields.Many2one(
        "product.template",
        "Service Product",
        domain="[('detailed_type', '=', 'serviceprofile'), ('type', '=', 'service')]",
    )
    product_variant_id = fields.Many2one(
        "product.product",
        "Service Product Variant",
        domain="[('detailed_type', '=', 'serviceprofile'), ('type', '=', 'service')]",
    )
    use_product_variant = fields.Boolean(default=False)
    partner_id = fields.Many2one(related="agreement_id.partner_id", string="Partner")

    # Used for Kanban grouped_by view
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stages |= stages.search([("stage_type", "=", "serviceprofile")], order=order)
        return stages
