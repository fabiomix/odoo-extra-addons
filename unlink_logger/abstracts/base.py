# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    _inherit = 'base'

    # List of fields that should be logged on unlink
    _unlink_log_fields = []


    # CRUD methods (and name_get, name_search, ...) overrides

    def unlink(self):
        if self._unlink_log_fields:
            for record in self:
                log_dict = {'model': record._name, 'id': record.id}
                for field_name in self._unlink_log_fields:
                    log_dict.update({field_name: record.mapped(field_name)})
                _logger.info(log_dict)
        return super(Base, self).unlink()
