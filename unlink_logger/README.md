# Unlink Logger
Log info about records before their deletion.

## Features
This module is intended to be extended by a developer, who defines for each Odoo
model the fields that must be written into the log file before a record is
deleted.

A working example is provided for the `ir.attachment` class, showing the name of
the file that is about to be deleted.

Dotted names (fields of relational fields) and one2many are supported.

### Example
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _unlink_log_fields = ['name', 'partner_id.name']
```

### Output
```
INFO mydb odoo.addons.unlink_logger.abstracts.base: {'model': 'sale.order', 'partner_id.name': ['Deco Addict'], 'name': ['SO005'], 'id': 5}
INFO mydb odoo.models.unlink: User #2 deleted sale.order records with IDs: [5]
```
