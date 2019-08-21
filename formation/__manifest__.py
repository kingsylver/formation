# -*- coding: utf-8 -*-

{
    'name': 'Formation Odoo 11',
    'version': '1.0',
    'author': 'Ait-Mlouk Addi',
    'website': 'https://www.sdatacave.com',
    'support': 'aitmlouk@gmail.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 1,
    'category': 'category',
    'description': """
        Put your description here for your module:
            - model1
            - model2
            - model3
    """,
    'depends': ['base', 'mail','hr','website'],
    'summary': 'Formation, odoo 11, erp',
    'data': [
        #'security/formation.xml',
        #'security/ir.model.access.csv',
        'report/report.xml',
        'report/registration.xml',
        'views/formation_views.xml',
        'views/formation_inherit.xml',
        'data/sequence.xml',
        'controllers/formation.xml',
        'controllers/claim.xml',
        'wizard/wizard_view.xml',
        'menu.xml',
    ],
    'demo': [
        #'demo/ModuleName_demo.xml'
    ],
    'css': [
        #'static/src/css/ModuleName_style.css'
    ],
    
    'price': 100.00,
    'currency': 'EUR',
    'installable': True,
    'application': True,
}
