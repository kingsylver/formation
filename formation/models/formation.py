from odoo import models, fields, api,_
from odoo.exceptions import UserError, AccessError, ValidationError, Warning





class Year(models.Model):
    _name = 'year.year'
    _description = 'Annee de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False)   
    code =fields.Char(string='Code', required=True, readonly=False)
    description=fields.Text(string='Description',  required=False)
    start_date = fields.Date('Date début',help="Date")
    end_date = fields.Date('Date fin',help="Date")
    session_ids = fields.One2many('session.session','year_id', string='Session', required=False) 
    

class Session(models.Model):
    _name = 'session.session'
    _description = 'session de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False)   
    code =fields.Char(string='Code', required=True, readonly=False)
    description=fields.Text(string='Description',  required=False)
    start_date = fields.Date('Date début',help="Date")
    end_date = fields.Date('Date fin',help="Date")
    year_id = fields.Many2one('year.year', string='Année univ',required=False)
    
class Claims(models.Model):
    _name = 'claim.claim'
    _description = 'claim de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False)   
    code =fields.Char(string='Code', readonly=True, default=lambda x: x.env['ir.sequence'].get('claim.claim'))
    description=fields.Text(string='Description',  required=False)
    start_date = fields.Date('Date début',help="Date")
    end_date = fields.Date('Date fin',help="Date")
    regist_id = fields.Many2one('registration.registration', string='Inscription',required=False)
    user_id =  fields.Many2one('res.users', string='Responsable',required=True)
    state=fields.Selection([('new', 'Nouvelle'), ('done', 'Validé'), ('cancel', 'Annulée')], string= 'Status')
    priority=fields.Selection([('1', 'Low'), ('2', 'Moyen'), ('3', 'High')], string= 'Status')
    amount =fields.Float(string='Montant')
    nb_hour=fields.Integer(string='#Heure')  
    total = fields.Float(compute='_total_compute', string='total')
    

    
    @api.one
    @api.depends('amount','nb_hour')
    def _total_compute(self):
        self.total = self.amount * self.nb_hour
    
    
    
class Registration(models.Model):
    _name = 'registration.registration'
    _inherit = ['mail.thread'] 
    #Do not touch _name it must be same as _inherit
    #_name = 'mail.threat'
    _description = 'Registration de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False, help='Nom du Registration ')
    etudiant = fields.Many2one('res.partner', string='Etudiant', domain="[('student_ok', '=',True)]")
    code =fields.Char(string='Code', required=True, readonly=True, default='/')
    description=fields.Text(string='Description',  required=False, help='La description du Registration de formation')
    start_date = fields.Date('Date début',help="Date")
    end_date = fields.Date('Date fin',help="Date")
    cycle_id = fields.Many2one('cycle.cycle', string='Cycle',required=False)
    year_id = fields.Many2one('year.year', string='Année univ',required=False)
    claims_ids = fields.One2many('claim.claim','regist_id', string='Registration', required=False)
    state=fields.Selection([('new', 'Nouvelle'), ('done', 'Validé'), ('cancel', 'Annulée')], string= 'Status',track_visibility='onchange')
    
    nb_reclam = fields.Integer(compute ='_compute_reclam', string='Nombre reclamation')
    
    @api.one
    @api.depends('claims_ids')
    def _compute_reclam(self):
        self.nb_reclam = len(self.claims_ids)
    
    @api.model
    @api.depends('name')
    def create(self, vals):
        if ('code' not in vals) or (vals.get('code')=='/'):
            vals['code'] = self.env['ir.sequence'].get('registration.registration')
        return super(Registration, self).create(vals) 
    
    @api.one    
    def action_new(self):
        self.state = 'new'
        return True
    
    @api.one    
    def action_done(self):
        self.state = 'done'
        return True
    
    @api.one
    def action_cancel(self):
        self.state = 'cancel'
        return True

class Cycle(models.Model):
    _name = 'cycle.cycle'
    _description = 'Cycle de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False, help='Nom du cycle ')   
    code =fields.Char(string='Code', required=True, readonly=False, default='001', help='Le code du cycle')
    description=fields.Text(string='Description',  required=False, help='La description du cycle de formation')
    level_ids = fields.One2many('level.level', "cycle_id", string='Cycle',required=False)
    registrat_ids = fields.One2many('registration.registration','cycle_id', string='Registration') 

  
class Level(models.Model):
    _name = 'level.level'
    _description = 'Niveau de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False, help='Nom du Niveau ')   
    code =fields.Char(string='Code', required=True, readonly=False, default='001', help='Le code du Niveau')
    description=fields.Text(string='Description',  required=False, help='La description du Niveau de formation')
    section_ids = fields.One2many('section.section', "level_id", string='Section',required=False, help='Liaison section -- level')
    cycle_id = fields.Many2one('level.level', string='Cycle',required=False, help='Liaison cycle -- level')

class Section(models.Model):
    _name = 'section.section'
    _description = 'Section de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False, help='Nom du Module ')   
    code =fields.Char(string='Code', required=True, readonly=False, help='Le code du module')
    description=fields.Text(string='Description',  required=False, help='La description du modules de formation')
    module_ids = fields.One2many('module.module','section_id', string='Module', required=False, help='Liaison section -- Module')
    level_id = fields.Many2one('level.level', string='Niveau',required=False, help='Liaison section -- level')
    
class Module(models.Model):
    _name = 'module.module'
    _description = 'Modules de formation ...'
    
    name = fields.Char(string='Nom', required=True, readonly=False, help='Nom du Module ')   
    code =fields.Char(string='Code', required=True, readonly=False, default='001', help='Le code du module')
    description=fields.Text(string='Description',  required=False, help='La description du modules de formation')
    section_id = fields.Many2one('section.section', string='Section',required=False, help='Liaison section -- Module')
    
class Partner(models.Model):
    _inherit = 'res.partner' 

    _description = 'student'
    
    @api.model
    def create(self, vals):
        #raise Warning(vals.get('gender'))
        if vals.get('lastname'):
            if vals.get('gender') == "female":
                vals['lastname'] = "Mme " + vals.get('lastname')
            elif vals.get('gender') == "male":
                vals['lastname'] = "Mr " + vals.get('lastname')
        res = super(Partner, self).create(vals)
        return res
    
 
    student_ok = fields.Boolean(string='Est un étudiant') 
    birthday = fields.Date(string='Date de naissance')
    age = fields.Integer(string='Age')
    reg_ids = fields.One2many('registration.registration','etudiant') 
    

    
class Prof(models.Model):

    _name = 'teacher.teacher'
    _inherit = 'hr.employee'  

    _description = 'teacher.teacher'
 
    age = fields.Integer(string='Age')
    cbi = fields.Char(string="CIN")

    
    
    
    