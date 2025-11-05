# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # --------------------------
    # Vendor Information
    # --------------------------
    vendor_no = fields.Char(string="Vendor No")
    vendor_contact = fields.Char(string="Vendor Contact")
    vendor_phone = fields.Char(string="Vendor Phone")
    vendor_email = fields.Char(string="Vendor Email")
    vendor_address_display = fields.Html(string="Vendor Address")

    @api.onchange('partner_id')
    def _onchange_partner_id_vendor_info(self):
        """Auto-fill vendor details from partner when vendor changes, but keep editable."""
        for rec in self:
            partner = rec.partner_id
            if partner:
                rec.vendor_phone = partner.phone or ""
                rec.vendor_email = partner.email or ""
                rec.vendor_address_display = partner._display_address(without_company=True)
            else:
                rec.vendor_phone = ""
                rec.vendor_email = ""
                rec.vendor_address_display = ""

    # --------------------------
    # Shipping Details (Employee-based)
    # --------------------------
    ship_employee_id = fields.Many2one(
        'hr.employee',
        string="Shipping Employee",
        help="Employee responsible for shipping",
        ondelete="set null"
    )
    ship_phone = fields.Char(string="Ship Phone")
    ship_email = fields.Char(string="Ship Email")
    ship_to = fields.Many2one('res.company', string="Ship To", default=lambda self: self.env.company)
    ship_address_display = fields.Html(string="Shipping Address")

    @api.onchange('ship_employee_id')
    def _onchange_ship_employee_id(self):
        """Auto-fill shipping info from employee."""
        for rec in self:
            emp = rec.ship_employee_id
            if emp:
                rec.ship_phone = emp.work_phone or ""
                rec.ship_email = emp.work_email or ""
            # Don't clear user-entered values if employee removed

    @api.onchange('ship_to')
    def _onchange_ship_to(self):
        """Auto-fill shipping address from selected company."""
        for rec in self:
            company = rec.ship_to
            rec.ship_address_display = (
                company.partner_id._display_address(without_company=True) if company else ""
            )

    # --------------------------
    # Billing Details (Employee-based)
    # --------------------------
    bill_employee_id = fields.Many2one(
        'hr.employee',
        string="Billing Employee",
        help="Employee responsible for billing",
        ondelete="set null"
    )
    bill_phone = fields.Char(string="Bill Phone")
    bill_email = fields.Char(string="Bill Email")
    bill_to = fields.Many2one('res.company', string="Bill To", default=lambda self: self.env.company)
    bill_address_display = fields.Html(string="Billing Address")

    @api.onchange('bill_employee_id')
    def _onchange_bill_employee_id(self):
        """Auto-fill billing info from employee."""
        for rec in self:
            emp = rec.bill_employee_id
            if emp:
                rec.bill_phone = emp.work_phone or ""
                rec.bill_email = emp.work_email or ""

    @api.onchange('bill_to')
    def _onchange_bill_to(self):
        """Auto-fill billing address from selected company."""
        for rec in self:
            company = rec.bill_to
            rec.bill_address_display = (
                company.partner_id._display_address(without_company=True) if company else ""
            )
