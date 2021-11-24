# -*- coding:utf-8 -*-

import logging

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class Equipacion(models.Model):
	_name='equipacion'
	_inherit='equipamiento'
	name = fields.Char(string='codigo_equipo')
	proyecto_id = fields.Many2one('conf2',string='Proyecto',ondelete='restrict')
	tarea_id = fields.Many2one('tarea',string="Tarea",ondelete='restrict')
	parent_id = fields.Many2one('espacios',string='Local',ondelete='restrict',index=True)
	_parent_store = True
	_parent_name = "parent_id"
	parent_path = fields.Char(index=True)
	equipamiento_name = fields.Many2one('product.template', string="Nombre equipo Simalga")
	equipo_cliente = fields.Char(string="Nombre equipamiento cliente")
	cantidad = fields.Float(string="cantidad")
	unidad = fields.Char(string="Unidad de medida")
	name_es = fields.Char(string='Equipamiento')
	name_fr = fields.Char(string='Équipement')
	name_en = fields.Char(string='Equipment')
	ull_ids = fields.Char(string="ull")
	sub_ull_ids = fields.Char(string="sub ull")
	sub_ull_2_ids = fields.Char(string="sub ull 2")
	item_code = fields.Char(string="item-code")
	descripcion_es = fields.Text(string='Descripción')
	descripcion_fr = fields.Text(string='Description')
	descripcion_en = fields.Text(string='Description')
	tipo = fields.Char(string="Tipo")
	sub_tipo = fields.Char(string="Sub-tipo")
	tipo_arq = fields.Char(string="Tipo arquitéctonico")
	es_datasheet_es = fields.Boolean(string = 'Ficha técnica')
	datasheet_es = fields.Binary(string="Ficha técnica")
	datasheet_filename_es = fields.Char(string="Nombre de archivo")
	es_datasheet_fr = fields.Boolean(string = 'Fiche technique')
	datasheet_fr = fields.Binary(string="Fiche technique")
	datasheet_filename_fr = fields.Char(string="Nom du fichier")
	es_datasheet_en = fields.Boolean(string = 'Datasheet')
	datasheet_en = fields.Binary(string="Datasheet")
	datasheet_filename_en = fields.Char(string="File name")
	car_alto = fields.Float(string="Alto(cm)")
	car_ancho = fields.Float(string="Ancho(cm)")
	car_largo = fields.Float(string="Largo(cm)")
	car_peso = fields.Float(string="Peso(kg)")
	superficie = fields.Float(string="Superficie (cm2)",compute="_sup_basic",stored=True)
	state = fields.Selection(
				[('creado','Creado'),
				 ('curso','En curso'),
				 ('consolidado','Consolidado'),
				 ('revision','En revisión'),
				 ('enviado','Enviado')],
				default='creado',string="Estado",group_expand='_get_stages'
				)
	@api.onchange('car_ancho','car_largo')
	def _sup_basic(self):
		cm_superficie = self.car_ancho * self.car_largo
		self.superficie = cm_superficie/10000
	ubicacion = fields.Selection(selection=[
	('suelo','suelo'),
	('mural','mural'),
	('sobremesa','sobremesa'),
	],
	string = 'Ubicación predeterminada'
	)
	movilidad = fields.Boolean(string="¿Tiene el equipo una ubicación fija?", default=True)
	fijacion = fields.Boolean(string="¿Necesita el equipo alguna fijación especial?", default=False)
	estructura = fields.Boolean(string="¿Necesita el equipamiento de cambios constructivos en la estructura?", default=False)
	conex_agua = fields.Boolean(string="¿Necesita el equipo conexión a circuito de agua corriente?", default=False)
	conex_tta = fields.Boolean(string="¿Necesita el equipo conexión a circuito de agua especial?", default=False)
	conex_elect = fields.Boolean(string="¿Necesita el equipo conexión a circuito eléctrico corriente?", default=False)
 	#conex_ups = fields.Boolean(string="¿Necesita el equipo conexión a circuito eléctrico de emergencia?", default=False)
	conex_com = fields.Boolean(string="¿Necesita el equipo conexión a red de comunicaciones?", default=False)
	conex_ups = fields.Boolean(string="¿Necesita el equipo conexión a circuito eléctrico de emergencia?", default=False)
	def ver_opciones(self):
		logger.info('hola soy el boton de opciones filtrados')
		logger.info('soy el self')
		logger.info(self)
		logger.info('somos los records')
		for record in self:
			logger.info(record)
		logger.info('hola soy')
		logger.info(record.name)
		view_id = self.env.ref('conf2.view_equipamiento_tree').id
		return{
			'type':'ir.actions.act_window',
			'view_mode':'tree,form',
			'views':[[view_id,'tree'],[false,'form']],
			'res_model':'equipacion',
			'domain':[['parent_id','=',record.name]],
			'target':'current',
			}
			@api.model
	def is_allowed_transition(self, old_state , new_state):
		logger.info('allowed?')
		logger.info('este es el self')
		logger.info(self)
		logger.info('este es el old_state')
		logger.info(old_state)
		logger.info('este es el new_state')
		logger.info(new_state)
		allowed = [('creado','curso'),
			   ('curso','revision'),
			   ('revision','consolidado'),
			   ('consolidado','revision'),
			   ('enviado','revision'),
			   ('revision','consolidado'),
			   ('consolidado','curso'),
			   ('curso','creado')]
		return (old_state, new_state) in allowed
	
	def change_state(self, new_state):
		logger.info('cambiando estado')
		logger.info('este es el self')
		logger.info(self)
		logger.info('este es el nuevo estado')
		logger.info(new_state)
		for project in self:
			logger.info('dentro del for')
			if project.is_allowed_transition(project.state,new_state):
				logger.info('dentro del if')
				project.state = new_state
			else:
				msg = _('Establecer desde %s a %s no está permitido') % (project.state, new_state)
				raise UserError(msg)
	def make_curso(self):
		self.change_state('curso')
	def make_consolidado(self):
		self.change_state('consolidado')
	def make_revision(self):
		self.change_state('revision')
	def make_enviado(self):
		self.change_state('enviado')
	def _get_stages(self, states, domain, order):
		
		return ['creado','curso','consolidado','revision','enviado']
