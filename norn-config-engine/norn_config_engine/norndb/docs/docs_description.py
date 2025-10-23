"""
    Mongoengine Documents specification
"""
from types import DynamicClassAttribute

from mongoengine import DynamicDocument
from mongoengine import DictField
from mongoengine import StringField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import BooleanField
from mongoengine import FloatField
from mongoengine import IntField
from mongoengine import DateTimeField

class ConstVars:
    HOST_ROLES = [
        "nginx",
        "haproxy"
    ]
    HOST_STATUS = [
        "running",
        "stopped",
        "not_installed"
    ]
    LB_KIND = [
        "nginx",
        "haproxy"
    ]
    MAIN_CONFIGG_POLICY = [
        "manual",
        "auto"
    ]
    TEMPLATE_ENGINES = [
        "jinja",
    ]

    LINT_STATUS = [
        "passed"
    ]

class HostDoc(DynamicDocument):
    name = StringField(required=True, unique=True)
    cluster = StringField(required=True)
    roles = StringField(choices=ConstVars.HOST_ROLES)
    labels = DictField()
    agent = DictField()
    status = StringField(choices=ConstVars.HOST_STATUS)
    sys_options = DictField()
    created_at = DateTimeField(required=True)

class ClusterDoc(DynamicDocument):
    name = StringField(required=True, unique=True)
    labels = DictField()
    ip_addrs = DictField()
    hosts = ListField(ReferenceField(HostDoc))
    lb_kind = StringField(choices=ConstVars.LB_KIND)
    main_config_template_ref = StringField(required=True)
    main_config_policy = StringField(required=True, choices=ConstVars.MAIN_CONFIGG_POLICY)
    created_at = DateTimeField(required=True)

class ServiceDoc(DynamicDocument):
    name = StringField(required=True, unique=True)
    template_ref = StringField(required=True)
    labels = DictField()
    enable = BooleanField(required=True)
    create_at = DateTimeField(required=True)
    description = StringField()

class ServicePlacementDoc(DynamicDocument):
    service = ReferenceField(ServiceDoc)
    cluster = ReferenceField(ClusterDoc)
    enabled = BooleanField(required=True)
    template_ref = StringField()
    context_overlay = DictField()
    created_at = DateTimeField(required=True)
    notes = StringField()

class RevisionDoc(DynamicDocument):
    service = ReferenceField(ServiceDoc)
    git = DictField()
    context = DictField()
    template_ref = StringField()
    author = StringField()
    hash = StringField()
    created_at = DateTimeField(required=True)

class ArtifactDoc(DynamicDocument):
    service = ReferenceField(ServiceDoc, required=True)
    revision = ReferenceField(RevisionDoc, required=True)
    cluster = StringField(required=True)
    lb_kind = StringField(required=True, choices=ConstVars.LB_KIND)
    render = DictField()
    composed_from = DictField()
    created_at = DateTimeField(required=True)

class ConfigTemplateDoc(DynamicDocument):
    engine = StringField(required=True, choices=ConstVars.TEMPLATE_ENGINES)
    fs_path = StringField(required=True)
    version = StringField(required=True)
    lint_status = StringField(choices=ConstVars.LINT_STATUS)
    schema = DictField(required=True)
    created_at = DateTimeField(required=True)
    owner = StringField()

class ContextDoc(DynamicDocument):
    template_ref = StringField(required=True)
    version = IntField(required=True)
    data = DictField(required=True)
    created_at = DateTimeField(required=True)

class SnapshotDoc(DynamicDocument):
    cluster = StringField(required=True)
    lb_kind = StringField(required=True, choices=ConstVars.LB_KIND)
    state = StringField(required=True)
    services = DictField(required=True)
    manifest = DictField(required=True)
    composed_from = DictField(required=True)
    bundle = DictField(required=True)
    retention = DictField(required=True)
    timestamps = DictField(required=True)
    actor = DictField(required=True)

class SnapshotDiffDoc(DynamicDocument):
    cluster = StringField(required=True)
    from_snapshot = StringField(required=True)
    to_snapshot = StringField(required=True)
    patch = ListField(required=True)
    bundle_delta = DictField(required=True)
    created_at = DateTimeField(required=True)

class DeploymentDoc(DynamicDocument):
    cluster = StringField(required=True)
    snapshot = ReferenceField(SnapshotDoc)
    state = StringField(required=True)
    targets = ListField(required=True)
    batches = ListField(required=True)
    gates = DictField(required=True)
    timestamps = DictField(required=True)
    actor = StringField(required=True)

class HostStateDoc(DynamicDocument):
    cluster = StringField(required=True)
    host_id = StringField(required=True)
    active_snapshot = StringField(required=True)
    last_good_snapshot = StringField(required=True)
    files = ListField(required=True)
    updated_at = DateTimeField(required=True)

class EventDoc(DynamicDocument):
    ts = DateTimeField(required=True)
    cluster = StringField(required=True)
    kind = StringField(required=True)
    refs = DictField(required=True)
    payload = DictField(required=True)
