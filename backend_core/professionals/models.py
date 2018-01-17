# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db import models


CONTRACTOR = 'CONTRACTOR'
ARCHITECT = 'ARCHITECT'
DESIGNER = 'DESIGNER'
MEISTER = 'MEISTER'
PROFESSIONAL = 'PROFESSIONAL'
# TODO: take care
PROFESSIONAL_CHOICES = (
    (CONTRACTOR, _('Contractor')),
    (ARCHITECT, _('Architect')),
    (DESIGNER, _('Designer')),
    (MEISTER, _('Meister')),
    (PROFESSIONAL, _('Professional')),
)

# entity type
C = 'Corporation'
S = 'Sole Ownership'
P = 'Partnership'
ENTITY_CHOICES = (
    (C, _('Corporation')),
    (P, _('Partnership')),
    (S, _('Sole Ownership')),
)

# TODO: load static file into professional subtype
# professional subtype
GC = 'General Contractor'
LC = 'Landscaping Contractor'
SPC = 'Swimming Pool Contractor'
KBR = 'KBR'
RG = 'Roofing Contractor'
PL = 'Plumbing Contractor'
FC = 'Fencing Contractor'
HVAC = 'HVAC Contractor'
DE = 'Designer'
DG = 'Doors, Gates and Activating Devices'
CC = 'Carpentry Contractor'
COC = 'Concrete Contractor'
DC = 'Drywall Contractor'
EC = 'Electrical Contractor'
PDC = 'Painting And Decorating Contractor'
SMC = 'Sheet Metal Contractor'
ME = 'Meister'
AC = 'Architect'

PROFESSIONAL_SUBTYPE_CHOICES = (
    (GC, _('General Contractor')),
    (LC, _('Landscaping Contractor')),
    (SPC, _('Swimming Pool Contractor')),
    (KBR, _('Kitchen & Bath Remodeler')),
    (RG, _('Roofing Contractor')),
    (PL, _('Plumbing Contractor')),
    (FC, _('Fencing Contractor')),
    (HVAC, _('HVAC Contractor')),
    (DE, _('Designer')),
    (DG, _('Doors, Gates and Activating Devices')),
    (CC, _('Carpentry Contractor')),
    (COC, _('Concrete Contractor')),
    (DC, _('Drywall Contractor')),
    (EC, _('Electrical Contractor')),
    (PDC, _('Painting And Decorating Contractor')),
    (SMC, _('Sheet Metal Contractor')),
    (ME, _('Meister')),
    (AC, _('Architect')),
)


class Professional(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    csp = models.CharField(max_length=63, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    lic_status = models.CharField(max_length=30, blank=True, null=True)
    phone = models.TextField(blank=True)
    entity_type = models.CharField(
        max_length=63,
        choices=ENTITY_CHOICES
    )
    type = models.CharField(
        max_length=10,
        choices=PROFESSIONAL_CHOICES
    )
    state = models.CharField(max_length=63)
    lic_type = models.TextField(default='NO LIC TYPE')
    #TODO: need to change the name to pos_code later
    pos_code = models.CharField(max_length=63, blank=True, null=True)
    uuid = models.CharField(max_length=36, default='0')
""" 
class LicenseRelation(models.Model):
    name = models.CharField(max_length=63)
    #Do not use the reference below because it will requite name_id which is not necessary in this case
    #name = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, related_name='contractor')
    related_contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, related_name='related_contractor')

    class Meta:
        unique_together = ('name', 'contractor', 'related_contractor')
"""


#professional_type type,subtype: Contractor/Architect/Designer/
class ProfessionalType(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.DO_NOTHING,
        related_name='professional_types',
        related_query_name='professional_type'
    )
    type = models.CharField(max_length=10)
    subtype = models.CharField(
        max_length=255,
        choices=PROFESSIONAL_SUBTYPE_CHOICES
    )


class DataCollection(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.DO_NOTHING)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=0)
    object_id = models.PositiveIntegerField(default=0)
    lic_num = models.CharField(max_length=127, default='0')




