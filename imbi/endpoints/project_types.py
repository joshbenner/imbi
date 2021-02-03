import re

from imbi.endpoints import base


class _RequestHandlerMixin:

    ID_KEY = 'id'
    FIELDS = ['id', 'name', 'description', 'icon_class']
    DEFAULTS = {'icon_class': 'fas fa-folder'}

    GET_SQL = re.sub(r'\s+', ' ', """\
        SELECT id, "name", created_at, created_by,
               last_modified_at, last_modified_by,
               description, slug, icon_class
          FROM v1.project_types
         WHERE id=%(id)s""")


class CollectionRequestHandler(_RequestHandlerMixin,
                               base.CollectionRequestHandler):

    NAME = 'project-types'
    ITEM_NAME = 'project-type'

    COLLECTION_SQL = re.sub(r'\s+', ' ', """\
        SELECT id, "name", description, slug, icon_class
          FROM v1.project_types
         ORDER BY "name" ASC""")

    POST_SQL = re.sub(r'\s+', ' ', """\
        INSERT INTO v1.project_types
                    ("name", created_by, description, slug, icon_class)
             VALUES (%(name)s, %(username)s, %(description)s, %(slug)s,
                     %(icon_class)s)
          RETURNING id""")


class RecordRequestHandler(_RequestHandlerMixin, base.AdminCRUDRequestHandler):

    NAME = 'project-type'

    DELETE_SQL = 'DELETE FROM v1.project_types WHERE id=%(id)s;'

    PATCH_SQL = re.sub(r'\s+', ' ', """\
        UPDATE v1.project_types
           SET "name"=%(name)s,
               last_modified_at=CURRENT_TIMESTAMP,
               last_modified_by=%(username)s,
               description=%(description)s,
               slug=%(slug)s,
               icon_class=%(icon_class)s
         WHERE id=%(id)s""")