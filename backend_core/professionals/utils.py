from django.utils.translation import ugettext_lazy as _

CONTRACTOR = 'CONTRACTOR'
ARCHITECT = 'ARCHITECT'
DESIGNER = 'DESIGNER'
MEISTER = 'MEISTER'
# TODO: take care
PROFESSIONAL_CHOICES = (
    (CONTRACTOR, _('Contractor')),
    (ARCHITECT, _('Architect')),
    (DESIGNER, _('Designer')),
    (MEISTER, _('Meister'))
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


def check_professional_type(request):
    for i in [j[0] for j in PROFESSIONAL_CHOICES]:
        if i.lower() in request.path:
            model_type = i.lower()
            return model_type
            break
        else:
            pass
