# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    lot_ids = fields.Many2many(
        'stock.lot',
        'purchase_order_line_stock_lot_rel',
        'purchase_line_id',
        'lot_id',
        string='Lots/Serial Numbers',
        domain="[('product_id', '=', product_id)]",
        copy=True,
        help="Lot/Serial numbers assigned to this purchase order line."
    )
    expiration_date = fields.Datetime(
        string='Expiry Date',
        compute='_compute_expiration_date',
        store=True,
        readonly=False,
        help="Expiration date assigned to the selected lot(s)."
    )
    lot_expiry_display = fields.Char(
        string='Expiry Dates',
        compute='_compute_lot_expiry_display',
        store=True,
        help="Formatted list of expiry dates for assigned lot(s)."
    )

    @api.depends('lot_ids', 'lot_ids.expiration_date')
    def _compute_expiration_date(self):
        for line in self:
            dates = [lot.expiration_date for lot in line.lot_ids if lot.expiration_date]
            if dates:
                line.expiration_date = dates[0]
            elif not line.expiration_date:
                line.expiration_date = False

    @api.onchange('expiration_date')
    def _onchange_expiration_date(self):
        if self.expiration_date and self.lot_ids:
            for lot in self.lot_ids:
                lot.expiration_date = self.expiration_date

    @api.depends('lot_ids', 'lot_ids.expiration_date', 'expiration_date')
    def _compute_lot_expiry_display(self):
        for line in self:
            expiries = []
            for lot in line.lot_ids:
                if lot.expiration_date:
                    exp_date = lot.expiration_date.date() if isinstance(lot.expiration_date, datetime) else lot.expiration_date
                    exp_str = fields.Date.to_string(exp_date)
                    if exp_str not in expiries:
                        expiries.append(exp_str)
            if not expiries and line.expiration_date:
                exp_date = line.expiration_date.date() if isinstance(line.expiration_date, datetime) else line.expiration_date
                exp_str = fields.Date.to_string(exp_date)
                expiries.append(exp_str)
            line.lot_expiry_display = ", ".join(sorted(expiries)) if expiries else ""

    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        if 'expiration_date' in vals or 'lot_ids' in vals:
            for line in self:
                if line.expiration_date and line.lot_ids:
                    lots_to_update = line.lot_ids.filtered(
                        lambda l: not l.expiration_date or l.expiration_date != line.expiration_date
                    )
                    if lots_to_update:
                        lots_to_update.write({'expiration_date': line.expiration_date})
                if line.move_ids and line.lot_ids:
                    for move in line.move_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
                        move.lot_ids = [(6, 0, line.lot_ids.ids)]
        return res

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for vals in res:
            if self.lot_ids:
                vals['lot_ids'] = [(6, 0, self.lot_ids.ids)]
        return res

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move=move)
        if self.lot_ids:
            res['lot_ids'] = [(6, 0, self.lot_ids.ids)]
        return res
