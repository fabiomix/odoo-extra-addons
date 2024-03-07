# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class IrAutoVacuum(models.AbstractModel):
    _inherit = 'ir.autovacuum'

    @api.model
    def power_on(self, *args, **kwargs):
        self.env['mail.mail']._gc_auto_delete_mail()
        return super(IrAutoVacuum, self).power_on(*args, **kwargs)
