from flask_table import Table, Col, LinkCol
 
class ResultsPersona(Table):
    Id = Col('Id', show=False)
    Nombre = Col('Nombre')
    Apellido1 = Col('Primer Apellido')
    Apellido2 = Col('Segundo Apellido')
    Matricula = Col('Matricula')
    Email = Col('Email')
    Pass = Col('Password', show=False)
    edit = LinkCol('Editar', 'edit_view_user', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_user', url_kwargs=dict(id='Id'))

class ResultsRoles(Table):
    Id = Col('Id', show=False)
    Nombre = Col('Nombre')
    edit = LinkCol('Editar', 'edit_view_rol', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_rol', url_kwargs=dict(id='Id'))

class ResultsEditorial(Table):
    Id = Col('Id', show=False)
    Nombre = Col('Nombre')
    edit = LinkCol('Editar', 'edit_view_editorial', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_editorial', url_kwargs=dict(id='Id'))
class ResultsAutor(Table):
    Id = Col('Id', show=False)
    Nombre = Col('Nombre')
    edit = LinkCol('Editar', 'edit_view_autor', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_autor', url_kwargs=dict(id='Id'))
class ResultsArea(Table):
    Id = Col('Id', show=False)
    Nombre = Col('Nombre')
    edit = LinkCol('Editar', 'edit_view_area', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_area', url_kwargs=dict(id='Id'))

class ResultsTipo(Table):
    Id = Col('Id', show=False)
    Tipo = Col('Nombre')
    Descr = Col('Descripción')
    edit = LinkCol('Editar', 'edit_view_tipo', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_tipo', url_kwargs=dict(id='Id'))

class ResultsCiudad(Table):
    Id = Col('Id', show=False)
    Pais = Col('País')
    Ciudad = Col('Ciudad')
    edit = LinkCol('Editar', 'edit_view_ciudad', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_ciudad', url_kwargs=dict(id='Id'))

class ResultsTPrestamo(Table):
    Id = Col('Id', show=False)
    Tipo = Col('Tipo de Prestamo')
    Descripcion = Col('Descripción')
    edit = LinkCol('Editar', 'edit_view_tprestamo', url_kwargs=dict(id='Id'))
    delete = LinkCol('Eliminar', 'delete_tprestamo', url_kwargs=dict(id='Id'))
    