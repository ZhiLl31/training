from odoo import models,fields,api
from odoo.exceptions import ValidationError

class PermohonanCuti(models.Model):
	_name   = 'cep.permohonan.cuti'
	_description    = 'Permohonan Cuti'

	line_ids = fields.One2many(comodel_name='cep.permohonan.cuti.line', inverse_name='cuti_id' , string='cuti_ids')
	

	name = fields.Char(string='Nama')
	wilayah = fields.Char(string='Wilayah/Div')
	nik = fields.Char(string='NIK')
	jabatan = fields.Char(string='Jabatan')

	# start_date = fields.Date(string='Dari Tanggal')
	# end_date = fields.Date(string='Sampai Tanggal')
	# jumlah = fields.Char(string='Jumlah Hari')
	alamat = fields.Char(string='Alamat Selama Cuti')
	no_telp = fields.Char(string='No Telp Selama Cuti')
	# pengajuan = fields.Date(string='Tanggal Pengajuan')
	ttd = fields.Binary(string='Tanda Tangan Pemohon')

	jumlah_cuti = fields.Char(string='Jumlah Cuti Disetujui')
	alasan = fields.Char(string='Alasan')
	tanda_tangan = fields.Binary(string='Tanda Tangan')
	
	jatah_cuti = fields.Char(string='Jatah Cuti tahun berjalan')
	cuti_terpakai = fields.Char(string='Jumlah Cuti Terpakai')
	cadangan = fields.Char(string='Cadangan Cuti bersama')
	jumlah_pengajuan = fields.Char(string='Jumlah Pengajuan Cuti')
	sisa_cuti = fields.Char(string='Sisa Cuti Tersedia')
	ttd_hrd = fields.Binary(string='Tanda Tangan HRD/GA')
	state = fields.Selection(string='Status', selection=[('draft', 'DRAFT'), ('confirm', 'CONFIRM'),('reject','REJECT'), ('approve', 'APPROVE'), ('done', 'DONE')],default='draft', tracking=True)
	image_1920 = fields.Binary(string='Foto')
	
	
	@api.constrains('create_uid')
	def _compute_name(self):
		for record in self:
			record.name = record.create_uid.name

	@api.constrains('no-telp')
	def _check_no_telp(self):
		for record in self:
			if record.no_telp and not record.no_telp.isdigit():
				raise ValidationError('No Telp selama cuti hanya boleh berisi angka')

	@api.constrains('nik')
	def _check_nik(self):
		for record in self:
			if record.nik and not record.nik.isdigit():
				raise ValidationError('NIK Hanya Boleh Diisi dengan angka')
			 
	def action_draft(self):
			self.state='draft'

	def action_confirm(self):
			self.state='confirm'
				
	def action_approve(self):
			self.state='approve'

	def action_done(self):
			self.state='done'	

	def action_reject(self):
			self.unlink()
			self.state='reject'	
			return True


class PermohonanCutiLine(models.Model):
	_name = 'cep.permohonan.cuti.line'
	_description = 'Permohonan Cuti Line'

	cuti_id = fields.Many2one(comodel_name='cep.permohonan.cuti', string='cuti_id', ondelete='cascade', index=True)
	jenis_cuti = fields.Selection(string='Jenis Cuti', selection=[
	('biasa', 'Cuti Tahunan/Biasa'),
	('nikah', 'Pernikahan Karyawan/ti'),
	('nak', 'Pernikahan Anak Kandung'),
	('im', 'Istri Melahirkan'),
	('kak', 'Khitanan Anak Kandung'),
	('pak', 'Pembaptisan Anak Kandung'),
	('kkt', 'Kematian keluarga Tanggungan'),
	('kom', 'Kematian Orang Tua/Mertua'),
	('haid', 'Cuti Haid (Khusus Wanita)'),
	('lahir', 'Cuti Melahirkan (Khusus Wanita)'),
	('cphl', 'Cuti Pengganti Hari Libur'),
	('lain', 'Cuti Lainnya')
	], required=True, default='biasa')
	tanggal_cuti = fields.Date(string='Tanggal Cuti')
	approval = fields.Selection(string='Status', selection=[
		('draft', 'DRAFT'),
		('approve', 'APPROVE'),
		('reject','REJECT'),
		], default='draft')
	
	def action_approve(self):
		self.approval='approve'

	def action_reject(self):
		self.approval= 'reject'

	approval_state_check = fields.Boolean(string="Approval State Check", compute="_compute_approval_state_check")

	@api.onchange('cuti_id.state')
	def _compute_approval_state_check(self):
		for record in self:
			record.approval_state_check = record.cuti_id.state != 'approve'
	
	@api.constrains('tanggal_cuti','cuti_id.create_uid')
	def _check_duplicate_cuti_date(self):
		for rec in self:
			duplicate_cuti = self.env['cep.permohonan.cuti.line'].search([
				('tanggal_cuti', '=', rec.tanggal_cuti),
				('cuti_id.create_uid', '=', rec.cuti_id.create_uid.id),
				('id', '!=', rec.id),
			])
			if duplicate_cuti:
				raise ValidationError('tidak boleh mengajukan cuti dengan tanggal yang sama ')