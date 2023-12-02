from odoo import models, fields, api
from odoo.modules.module import get_resource_path

RAINBOW_THEME_PRESETS = {
    'callaghan': ('#222222', '#e6522c'),
    'community': ('#7c7bad', '#7c7bad'),
    'enterprise': ('#875a7b', '#00a09d'),
    'flatly': ('#2c3e50', '#2c3e50'),
    'journal': ('#eb6864', '#eb6864'),
    'litera': ('#02b875', '#4582ec'),
    'lumen': ('#158cba', '#158cba'),
    'minty': ('#55b298', '#55b298'),
    'pulse': ('#593196', '#593196'),
    'sandstone': ('#3e3f3a', '#325d88'),
    'solar': ('#073642', '#b58900'),
    'united': ('#772953', '#772953'),
}


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _selection_theme_brand_preset(self):
        return [(t, t.capitalize()) for t in sorted(RAINBOW_THEME_PRESETS.keys())]

    theme_brand_odoo = fields.Char(
        string='Theme brand Odoo',
        config_parameter='rainbow_theme.theme_brand_odoo',
        default='#7C7BAD',
    )

    theme_brand_primary = fields.Char(
        string='Theme brand primary',
        config_parameter='rainbow_theme.theme_brand_primary',
        default='#7C7BAD',
    )

    theme_brand_preset = fields.Selection(
        string='Theme brand presets',
        selection=_selection_theme_brand_preset,
        store=False,
    )

    @api.onchange('theme_brand_preset')
    def _onchange_theme_brand_preset(self):
        theme_preset = False
        if self.theme_brand_preset:
            theme_preset = RAINBOW_THEME_PRESETS.get(self.theme_brand_preset)
        if theme_preset:
            self.theme_brand_odoo = theme_preset[0]
            self.theme_brand_primary = theme_preset[1]

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self._rainbow_colors_update()
        return res

    def _rainbow_colors_update(self):
        theme_colors = get_resource_path('rainbow_theme', 'static/src/scss', 'theme_colors.scss')
        with open(theme_colors, 'w') as scss:
            scss.write("$o-brand-odoo: {0};\n".format(self.theme_brand_odoo or '#7C7BAD'))
            scss.write("$o-brand-primary: {0};\n".format(self.theme_brand_primary or '#7C7BAD'))
            scss.write("$o-required-field: hsl(hue($o-brand-primary), 40, 85);\n")
