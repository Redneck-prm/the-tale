
from django.db import models

from rels.django import RelationIntegerField

from the_tale.game.artifacts import relations


class ArtifactRecord(models.Model):

    MAX_UUID_LENGTH = 32
    MAX_NAME_LENGTH = 32

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    editor = models.ForeignKey('accounts.Account', null=True, related_name='+', blank=True, on_delete=models.SET_NULL)

    type = RelationIntegerField(relation=relations.ARTIFACT_TYPE, relation_column='value')
    power_type = RelationIntegerField(relation=relations.ARTIFACT_POWER_TYPE, relation_column='value')
    state = RelationIntegerField(relation=relations.ARTIFACT_RECORD_STATE, relation_column='value')

    rare_effect = RelationIntegerField(relation=relations.ARTIFACT_EFFECT, relation_column='value')
    epic_effect = RelationIntegerField(relation=relations.ARTIFACT_EFFECT, relation_column='value')

    special_effect = RelationIntegerField(relation=relations.ARTIFACT_EFFECT, relation_column='value', default=relations.ARTIFACT_EFFECT.NO_EFFECT.value)

    level = models.IntegerField(default=0)

    uuid = models.CharField(max_length=MAX_UUID_LENGTH, unique=True)

    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True, null=False, db_index=True)

    description = models.TextField(null=False, default='', blank=True)

    mob = models.ForeignKey('mobs.MobRecord', null=True, related_name='+', blank=True, on_delete=models.SET_NULL)

    data = models.TextField(null=False, default='{}')

    class Meta:
        permissions = (("create_artifactrecord", "Может предлагать артефакты"),
                       ("moderate_artifactrecord", "Может утверждать артефакты"),)
