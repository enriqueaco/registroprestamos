# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
import operator

def index():
    if(auth.user!=None):
        prestamos = db((db.registroprestamos01.devuelto==0)&(db.registroprestamos01.usuario==auth.user.email)).select(orderby=~db.registroprestamos01.fechaprestamo)
    else:
        prestamos = db(db.registroprestamos01.devuelto==0).select(orderby=~db.registroprestamos01.fechaprestamo)
    pass
    MAX_PUBLICACIONES=db(db.registroprestamos01).select(db.registroprestamos01.indice,orderby=~db.registroprestamos01.id,limitby=(0,1)).first()
    MAX_PUBLICACIONES=MAX_PUBLICACIONES['indice']

    #MAX_PUBLICACIONES=db(db.registroprestamos01).count()

    #MAX_PUBLICACIONES=db(db.registroprestamos01).count()
    response.flash = T("Bienvenido a SPICM")
    return dict(message=T('Welcome to web2py!'),prestamos=prestamos,contador=session.contador,MAX_PUBLICACIONES=MAX_PUBLICACIONES)

def estadisticas():
    fecha=''
    devoluciones=''
    instituciones=''
    categorias=''
    cantinst=''
    canttipop=''
    cantcateg=''
    tipoprestamos=''
    MAX_PUBLICACIONES=db(db.registroprestamos01).count()
    if request.vars['fecha'] and request.vars['biblioteca']:
        fecha=request.vars['fecha']
        biblioteca=request.vars['biblioteca']
        devoluciones=db((db.registroprestamos01.fechadevolucion.like(fecha+'%'))&(db.registroprestamos01.devuelto==1)&(db.registroprestamos01.biblioteca==biblioteca)).select()
        #autores=db((db.registroprestamos01.fechadevolucion.like(fecha+'%'))&(db.registroprestamos01.devuelto==1)).select(db.registroprestamos01.fechadevolucion,groupby=db.registroprestamos01.fechadevolucion)
        cantinst=db.registroprestamos01.institucion.count()
        instituciones=db((db.registroprestamos01.fechadevolucion.like(fecha+'%'))&(db.registroprestamos01.devuelto==1)&(db.registroprestamos01.biblioteca==biblioteca)).select(db.registroprestamos01.institucion,cantinst,groupby=db.registroprestamos01.institucion)
        canttipop=db.registroprestamos01.institucion.count()
        cantcateg=db.registroprestamos01.categoria.count()
        categorias=db((db.registroprestamos01.fechadevolucion.like(fecha+'%'))&(db.registroprestamos01.devuelto==1)&(db.registroprestamos01.biblioteca==biblioteca)).select(db.registroprestamos01.categoria,cantcateg,groupby=db.registroprestamos01.categoria)
        tipoprestamos=db((db.registroprestamos01.fechadevolucion.like(fecha+'%'))&(db.registroprestamos01.devuelto==1)&(db.registroprestamos01.biblioteca==biblioteca)).select(db.registroprestamos01.tipoprestamo,canttipop,groupby=db.registroprestamos01.tipoprestamo)
    response.flash = T("Bienvenido a SPICM")
    return dict(message=T('Welcome to web2py!'),contador=session.contador,MAX_PUBLICACIONES=MAX_PUBLICACIONES,fecha=fecha,devoluciones=devoluciones,instituciones=instituciones,cantinst=cantinst,tipoprestamos=tipoprestamos,canttipop=canttipop,cantcateg=cantcateg,categorias=categorias)

def modelo():
    prestamos = db(db.registroprestamos01.devuelto==1).select(orderby=~db.registroprestamos01.fechaprestamo)
    MAX_PUBLICACIONES=db(db.registroprestamos01).count()
    response.flash = T("Bienvenido a SPICM")
    return dict(message=T('Welcome to web2py!'),prestamos=prestamos,contador=session.contador,MAX_PUBLICACIONES=MAX_PUBLICACIONES)

def devueltos():
    if(auth.user!=None):
        prestamos = db((db.registroprestamos01.devuelto==1)&(db.registroprestamos01.usuario==auth.user.email)).select(orderby=~db.registroprestamos01.fechaprestamo)
    else:
        prestamos = db(db.registroprestamos01.devuelto==1).select(orderby=~db.registroprestamos01.fechaprestamo)
    pass
    #prestamos = db(db.registroprestamos01.devuelto==1).select(orderby=~db.registroprestamos01.fechaprestamo)
    MAX_PUBLICACIONES=db(db.registroprestamos01).count()
    response.flash = T("Bienvenido a SPICM")
    return dict(message=T('Welcome to web2py!'),prestamos=prestamos,contador=session.contador,MAX_PUBLICACIONES=MAX_PUBLICACIONES)


@auth.requires_membership('administrar')
def devolver():
    db(db.registroprestamos01.id == request.args(0, cast=int)).update(**{'devuelto':1})
    return dict(form=redirect(URL('index')))


@auth.requires_membership('administrar')
def prestamo():
    form=SQLFORM(db.registroprestamos01)
    if form.process(session=None,formname='prestamo').accepted:
        response.flash='Formulario correcto'
        redirect(URL('index'))
    elif form.errors:
        response.flash=form.errors
    else:
        response.flash='Llene el formulario'
    return dict(usuario=auth.user.email)

@auth.requires_membership('administrar')
def edicionprestamo():
    editar=db.registroprestamos01(request.args(0, cast=int)) or redirect(URL('index'))
    form=SQLFORM(db.registroprestamos01,editar,deletable=False,fields=['indice','tipoprestamo','titulo0','codigo0','autor0','volumen0','numero0','titulo1','codigo1','autor1','volumen1','numero1','titulo2','codigo2','autor2','volumen2','numero2','titulo3','codigo3','autor3','volumen3','numero3','titulo4','codigo4','autor4','volumen4','numero4','titulo5','codigo5','autor5','volumen5','numero5','titulo6','codigo6','autor6','volumen6','numero6','titulo7','codigo7','autor7','volumen7','numero7','titulo8','codigo8','autor8','volumen8','numero8','titulo9','codigo9','autor9','volumen9','numero9','categoria','nota','ci','nombre','apellidos','institucion','fechaprestamo','fechadevolucion','email','devuelto','biblioteca','usuario'],showid=False, labels={'tipoprestamo':'Tipo de Prestamo','fechaprestamo':'Fecha de Prestamo','fechadevolucion':'Fecha de Devolución'},formstyle="ul")
    if form.process().accepted:
        response.flash='Formulario correcto'
        redirect(URL('index'))
    elif form.errors:
        response.flash=form.errors
    else:
        response.flash='Llene el formulario'
    return dict(form=form,usuario=auth.user.email)

@auth.requires_membership('administrar')
def delete():
    db(db.registroprestamos01.id == request.args(0, cast=int)).delete()
    return dict(form=redirect(URL('index')))


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


@auth.requires_membership('admin')
def adminuser():
    grid = SQLFORM.grid(db.auth_membership)
    
    grid1 = SQLFORM.grid(db.auth_user)
    return dict(grid=grid,grid1=grid1)
