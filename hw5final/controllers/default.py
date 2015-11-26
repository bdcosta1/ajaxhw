# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time


def index():
    board_id = gluon_utils.web2py_uuid()
    loggedIn = True
    if auth.user_id is None:
        loggedIn = False
    return dict(board_id=board_id, loggedIn=loggedIn, user_id=auth.user_id)

def posts():
    boardNum = request.args(1)
    loggedIn = True
    if auth.user_id is None:
        loggedIn = False
    return dict(loggedIn=loggedIn, user_id=auth.user_id, boardNum=boardNum)
@auth.requires_signature()
def add_board():
    """db.post.update_or_insert((db.boards.message_id == request.vars.msg_id),
            message_id=request.vars.msg_id,
            message_content=request.vars.msg,
            is_draft=json.loads(request.vars.is_draft))
            db.boards.insert(name=request.vars.name, board_creator=request.vars.user_id)"""


    db.boards.update_or_insert((db.boards.draft_id == request.vars.draft_id), name = request.vars.name, draft_id=request.vars.draft_id, board_creator=auth.user_id, description = request.vars.description)
    return "ok"

@auth.requires_signature()
def add_post():
    """db.post.update_or_insert((db.boards.message_id == request.vars.msg_id),
            message_id=request.vars.msg_id,
            message_content=request.vars.msg,
            is_draft=json.loads(request.vars.is_draft))
            db.boards.insert(name=request.vars.name, board_creator=request.vars.user_id)"""


    db.post.update_or_insert((db.post.draft_id == request.vars.draft_id), name = request.vars.name, draft_id=request.vars.draft_id, post_creator=auth.user_id, board_table_id = request.vars.boardNum, description =request.vars.description)
    return "ok"

@auth.requires_signature()
def deleteBoard():
    db(db.boards.draft_id == request.vars.key).delete()
    return "ok"

@auth.requires_signature()
def newBoardHandle():
    db.boards.update_or_insert((db.boards.draft_id == request.vars.draft_id), name = request.vars.name, draft_id = request.vars.draft_id, board_creator=auth.user_id)
    return "ok"

@auth.requires_signature()
def newPostHandle():
    db.post.update_or_insert((db.post.draft_id == request.vars.draft_id), name = request.vars.name, draft_id = request.vars.draft_id, post_creator=auth.user_id, board_table_id = request.vars.boardNum, description = request.vars.description)
    return "ok"

@auth.requires_signature()
def update_board():
    row = db(db.boards.id == request.vars.loc).select().first()
    row.update_record(name = request.vars.name)
    return "ok"

@auth.requires_signature()
def update_post():
    row = db(db.post.id == request.vars.loc).select().first()
    row.update_record(name = request.vars.name, description = request.vars.description)
    return "ok"

def load_boards():
    """Loads all messages for the user."""
    rows = db(db.boards).select()
    d = {r.id: {'name': r.name, 'fromDB': r.fromDB, 'board_creator': r.board_creator, 'draft_id': r.draft_id}
         for r in rows}
    return response.json(dict(board_dict=d))
def load_posts():
    boardNum = request.vars.boardNum
    rows = db(db.post.board_table_id == boardNum).select()
    d = {r.id: {'name': r.name, 'fromDB': r.fromDB, 'post_creator': r.post_creator, 'draft_id': r.draft_id, 'description': r.description, 'created_on': r.created_on}
         for r in rows}
    return response.json(dict(post_dict=d))

@auth.requires_signature()
def deletePost():
    key = request.vars.key
    db(db.post.id == request.vars.key).delete()
    return "ok"


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()