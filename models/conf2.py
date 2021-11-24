# -*- coding:utf-8 -*-

import logging
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
logger = logging.getLogger(__name__)

class Conf2(models.Model):
	_name = "conf2"
	name = fields.Char(string="Proyecto",required=True)
	state = fields.Selection(
				[('creado','Creado'),
				 ('curso','En curso'),
				 ('revision','En revisión'),
				 ('enviado','Enviado')],
				default='creado',string="Estado",group_expand='_get_stages'
				)
	fecha_ini = fields.Date(string="Fecha Inicio")
	fecha_fin = fields.Date(string="Fecha Fin")
	child_tareas_ids =fields.One2many('tarea','parent_id', string = 'Tareas configuración')
	child_documental_ids = fields.One2many('documental','parent_id',string = 'Tareas documentales')
	estudios = fields.Boolean(string="¿Incluye estudios?")
	estudios_ini = fields.Date(string="Fecha Inicio")
	estudios_fin = fields.Date(string="Fecha Fin (estimada)")
	estudios_resp = fields.Many2one('res.users','Responsable realización')
	estudios_resp_id = fields.Integer(related="estudios_resp.id", readonly=True)
	mapa = fields.Boolean(string="¿Incluye mapa?")
	mapa_ini = fields.Date(string="Fecha Inicio")
	mapa_fin = fields.Date(string="Fecha Fin (estimada)")
	mapa_resp = fields.Many2one('res.users','Responsable realizacion')
	mapa_resp_id = fields.Integer(related="mapa_resp.id", readonly=True)
	plan_funcional = fields.Boolean(string="¿Incluye plan funcional?")
	plan_funcional_ini = fields.Date(string="Fecha Inicio")
	plan_funcional_fin = fields.Date(string="Fecha Fin (estimada)")
	plan_funcional_resp = fields.Many2one('res.users','Responsable realizacion')
	plan_funcional_resp_id = fields.Integer(related="plan_funcional_resp.id", readonly=True)
	plan_espacios = fields.Boolean(string="¿Incluye plan de espacios?")
	plan_espacios_ini = fields.Date(string="Fecha Inicio")
	plan_espacios_fin = fields.Date(string="Fecha Fin (estimada)")
	plan_espacios_resp = fields.Many2one('res.users','Responsable realizacion')
	plan_espacios_resp_id = fields.Integer(related="plan_espacios_resp.id", readonly=True)
	plan_equipamiento = fields.Boolean(string="¿Incluye plan de equipamiento?")
	plan_equipamiento_ini = fields.Date(string="Fecha Inicio")
	plan_equipamiento_fin = fields.Date(string="Fecha Fin (estimada)")
	plan_equipamiento_resp = fields.Many2one('res.users','Responsable realizacion')
	plan_equipamiento_resp_id = fields.Integer(related='plan_equipamiento_resp.id',readonly=True)
	progreso_tareas_ids = fields.Float(related="child_tareas_ids.completado")
	completado = fields.Float(string="Completado", default=0.0,compute="_progreso",stored=True)
	def create_tarea(self):
		logger.info('in self:',self.id)
		logger.info('estudios:',self.estudios)
		logger.info('mapa:',self.mapa)
		logger.info('funcional:',self.plan_funcional)
		logger.info('espacios:',self.plan_espacios)
		logger.info('equipamiento:',self.plan_equipamiento)
		logger.info('plan_equipamieto_resp:',self.plan_equipamiento_resp_id)
		nombre = self.name
		tareas = []
		documentales = []
		if self.estudios == True:
			documentales.append('estudio')
		if self.mapa == True:
			documentales.append('mapa')
		if self.plan_funcional == True:
			documentales.append('plan funcional')
		if self.plan_espacios == True and self.plan_equipamiento == False:
			tareas.append('plan de espacios')
		if self.plan_equipamiento == True and self.plan_espacios ==False:
			tareas.append('plan de espacios obl')
			tareas.append('plan de equipamiento')
		if self.plan_equipamiento == True and self.plan_espacios == True:
			tareas.append('plan de equipamiento')
			tareas.append('plan de espacios')
		for documental in documentales:
			if documental == 'estudio':
				record = self.env['documental'].create({'parent_id':self.id,'name':documental+' '+nombre,'fecha_ini':self.estudios_ini,'fecha_fin':self.estudios_fin,'responsable':self.estudios_resp_id})
			if documental  == 'mapa' :
				record = self.env['documental'].create({'parent_id':self.id,'name':documental+' '+nombre,'fecha_ini':self.mapa_ini,'fecha_fin':self.mapa_fin,'responsable':self.mapa_resp_id})
			if documental == 'plan funcional':
				record = self.env['documental'].create({'parent_id':self.id,'name':documental+' '+nombre,'fecha_ini':self.plan_funcional_ini,'fecha_fin':self.plan_funcional_fin,'responsable':self.plan_funcional_resp_id})


		for tarea in tareas:
			if tarea == 'plan de espacios':
				record = self.env['tarea'].create({'parent_id':self.id,'name':tarea+' '+nombre,'fecha_ini':self.plan_espacios_ini,'fecha_fin':self.plan_espacios_fin,'responsable':self.plan_espacios_resp_id})

	def _progreso(self):
		for record in self:
			logger.info('HOLA')
			logger.info(record.id)
			logger.info(record.child_tareas_ids)
			tareas = record.child_tareas_ids
			logger.info('len tareas')
			logger.info(len(tareas))
			if len(tareas) > 0:
				logger.info('+ de 0 tareas')
				completado = 0.0
				n_tareas = 0
				for tarea in tareas:
					logger.info(tarea.id)
					completado = completado + self.env['tarea'].search([('id','=',tarea.id)]).completado
					n_tareas = n_tareas + 1
			else:
				n_tareas = 0
				completado = 0.0
			logger.info('completado en tareas')
			logger.info(completado)
			logger.info('n_tareas en tareas')
			logger.info(n_tareas)
			documentales = record.child_documental_ids
			logger.info('documentales')
			logger.info(documentales)
			if len(documentales) > 0:
				logger.info('+ de 0 documental')
				for documental in documentales:
					logger.info(documental.id)
					completado = completado + self.env['documental'].search([('id','=',documental.id)]).completado
					n_tareas = n_tareas + 1
			logger.info('completado en documental')
			logger.info(completado)
			logger.info('n_tareas en documental')
			logger.info(n_tareas)

			if completado > 0.0:
				logger.info('completado + de 0.0')
				total_completado = completado / n_tareas
				logger.info('total completado')
				logger.info(total_completado)
				record.completado = total_completado
			else:
				record.completado = 0.0

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
			   ('revision','enviado'),
			   ('enviado','revision'),
			   ('revision','curso'),
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
	def make_revision(self):
		self.change_state('revision')
	def make_enviado(self):
		self.change_state('enviado')
	def ver_tareas(self):
		logger.info('hola soy el boton tareas filtradas')
		logger.info('soy el self')
		logger.info(self)
		logger.info('somos los records')
		for record in self:
			logger.info(record)
		logger.info('hola soy')
		logger.info(record.name)
		view_id = self.env.ref('conf2.view_tareas_tree').id
		context = dict(self.env.context)
		context['form_view_initial_mode'] = 'edit'
		return{
			'type':'ir.actions.act_window',
			'view_mode':'tree,form',
			'views':[[view_id,'tree'],[False,'form']],
			'res_model':'tarea',
			'domain':[['parent_id','=',record.name]],
			'target':'current',
			}

	def _get_stages(self, states, domain, order):
		return ['creado','curso','revision','enviado']
