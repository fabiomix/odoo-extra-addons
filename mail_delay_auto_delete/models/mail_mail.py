# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

import logging
_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = 'mail.mail'


    # Fields declaration

    auto_delete_date = fields.Datetime(string='Auto Delete Date')


    # Business methods

    @api.multi
    def _postprocess_sent_message(self, mail_sent=True):
        """
        Prevents the deletion of sent emails, even if the ``auto_delete`` flag is set.
        Then reset the flag and add the scheduled deletion date.
        """
        auto_delete_ids = []
        if mail_sent:
            auto_delete_ids = self.filtered(lambda mail: mail.auto_delete)

        if auto_delete_ids:
            for mail in auto_delete_ids:
                # disable auto_delete flag only in cache to save a write call.
                # super() should temporarily see the object with the flag off and skip the unlink().
                mail._cache.update(mail._convert_to_cache({'auto_delete': False}))
            _logger.debug('Postponed elimination for auto_delete emails %s', auto_delete_ids.ids)

        res = super(MailMail, self)._postprocess_sent_message(mail_sent=mail_sent)

        if auto_delete_ids:
            sys_params = self.env['ir.config_parameter'].sudo()
            auto_delete_delay = int(sys_params.get_param('mail.auto_delete.delay', 48))  # default 2 days
            auto_delete_date = datetime.utcnow() + timedelta(hours=auto_delete_delay)
            auto_delete_ids.sudo().write({
                'auto_delete': True,
                'auto_delete_date': auto_delete_date.strftime(DATETIME_FORMAT)
            })

        return res

    @api.model
    def _gc_auto_delete_mail(self):
        utcnow = datetime.utcnow().strftime(DATETIME_FORMAT)
        self.search([
            ('auto_delete', '=', True),
            ('auto_delete_date', '<', utcnow),
            ('state', '!=', 'exception')
        ]).unlink()
        return True
