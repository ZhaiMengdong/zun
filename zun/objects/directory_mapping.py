from oslo_log import log as logging
from oslo_versionedobjects import fields

from zun.common import exception
from zun.db import api as dbapi
from zun.objects import base
from zun.objects import container


_DIRECTORY_MAPPING_OPTIONAL_JOINED_FIELD = []
DIRECTORY_MAPPING_OPTIONAL_ATTRS = _DIRECTORY_MAPPING_OPTIONAL_JOINED_FIELD

@base.ZunObjectRegistry.register
class DirectoryMapping(base.ZunPersistentObject, base.ZunObject):
    # Version 1.0: Initial version
    # Version 1.1: Add field "auto_remove"
    VERSION = '1.1'

    fields = {
        'id': fields.IntegerField(),
        'uuid': fields.UUIDField(nullable=False),
        'user_id': fields.StringField(nullable=True),
        'project_id': fields.StringField(nullable=True),
        'local_directory': fields.StringField(nullable=True),
        'container_path': fields.StringField(nullable=True),
        'container_uuid': fields.UUIDField(nullable=True),
    }

    @staticmethod
    def _from_db_object(directory, db_volume):
        """Converts a database entity to a formal object."""
        for field in directory.fields:
            if field in DIRECTORY_MAPPING_OPTIONAL_ATTRS:
                continue
            setattr(directory, field, db_volume[field])

        directory.obj_reset_changes()
        return directory

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [DirectoryMapping._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable
    def create(self, context):
        """Create a DirectoryMapping record in the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object.
        """
        values = self.obj_get_changes()
        db_directory = dbapi.create_directory_mapping(context, values)
        self._from_db_object(self, db_directory)


    @base.remotable
    def destroy(self, context=None):
        """Delete the DirectoryMapping from the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object.
        """
        if not self.obj_attr_is_set('id'):
            raise exception.ObjectActionError(action='destroy',
                                              reason='already destroyed')
        dbapi.destroy_directory_mapping(context, self.uuid)
        delattr(self, 'id')
        self.obj_reset_changes()

    @base.remotable_classmethod
    def list_by_container(cls, context, container_uuid):
        filters = {'container_uuid': container_uuid}
        #import pdb;pdb.set_trace()
        db_directories = dbapi.list_directory_mappings(context, filters=filters)
        return DirectoryMapping._from_db_object_list(db_directories, cls, context)