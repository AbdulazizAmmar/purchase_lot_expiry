# -*- coding: utf-8 -*-
{
    'name': 'Purchase Lot & Serial Expiration Tracking',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Add lot/serial numbers and expiration dates to Purchase Order lines with tag display across Pickings and Invoices',
    'description': """
Purchase Lot & Serial Expiration Tracking
=========================================
This module enables the selection and management of Lot/Serial Numbers and their corresponding
Expiration Dates directly within Purchase Order lines.

Key Features:
- Assign Lot/Serial Numbers and Expiration Dates on Purchase Order lines.
- Display Lot/Serial Numbers as tags (using widget="many2many_tags") across Purchase Orders, Stock Pickings, and Vendor Bills.
- Display Expiration Dates as styled badges/tags across Purchase Orders, Stock Pickings, and Vendor Bills.
- Direct synchronization from Purchase Order lines to Stock Moves / Pickings and Account Move Lines (Vendor Bills).
- Dynamic lot domain filtering per product to prevent errors.
""",
    'author': 'Antigravity',
    'website': 'https://www.odoo.com',
    'depends': [
        'purchase_stock',
        'account',
        'product_expiry',
    ],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
