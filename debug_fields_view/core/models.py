# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(BaseModel, self).fields_get(allfields, attributes)

        # check if we are in debug mode and we have Technical Features enabled
        if request and request.debug and self.user_has_groups('base.group_no_one'):
            for field in res:
                res[field]['string'] = field

        return res
