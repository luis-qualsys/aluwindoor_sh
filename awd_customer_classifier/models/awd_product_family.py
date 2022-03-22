from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class AwdProductFamily(models.Model):
    _name = 'awd.product.family'
    _description = "Familias de productos"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'name'
    _order = 'complete_name'

    name = fields.Char(string='Nombre', index=True, required=True)
    complete_name = fields.Char(string="Nombre completo", compute='_compute_complete_name', recursive=True,
        store=True)
    child_id = fields.One2many('awd.product.family', 'parent_id', 'Categoria hija')
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one('awd.product.family', string='Familia padre', ondelete='cascade', index=True)
    awd_active_compute = fields.Boolean(string='Utilizar en el calculo', default=False)
    awd_product_count = fields.Integer(string='Productos', compute='_product_counter')
    awd_company_id = fields.Many2one('res.company', string='Compañía')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for family in self:
            if family.parent_id:
                family.complete_name = '%s / %s' % (family.parent_id.complete_name, family.name)
            else:
                family.complete_name = family.name

    # @api.constrains('parent_id')
    # def _check_family_recursion(self):
    #     if not self._check_recursion():
    #         raise ValidationError(_('No puedes crear categorias recursivas.'))

    # @api.model
    # def name_create(self, name):
    #     return self.create({'name': name}).name_get()[0]

    # def name_get(self):
    #     if not self.env.context.get('hierarchical_naming', True):
    #         return [(record.id, record.name) for record in self]
    #     return super().name_get()

    # @api.ondelete(at_uninstall=False)
    # def _unlink_except_default_category(self):
    #     main_category = self.env.ref('product.product_category_all')
    #     if main_category in self:
    #         raise UserError(_("You cannot delete this product category, it is the default generic category."))
