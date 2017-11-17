from django.utils.translation import ugettext_lazy as __

CONTRACTOR = 'CONTRACTOR'
ARCHITECT = 'ARCHITECT'
DESIGNER = 'DESIGNER'
MEISTER = 'MEISTER'
#TODO: take care
PROFESSIONAL_CHOICES = (
    (CONTRACTOR, __('Contractor')),
    (ARCHITECT, __('Architect')),
    (DESIGNER, __('Designer')),
    (MEISTER, __('Meister'))
)

# entity type
C = 'Corporation'
S = 'Sole Ownership'
P = 'Partnership'
ENTITY_CHOICES = (
    (C, __('Corporation')),
    (P, __('Partnership')),
    (S, __('Sole Ownership')),
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
ME = 'MEISTER'

PROFESSIONAL_SUBTYPE_CHOICES = (
    (GC, __('General Contractor')),
    (LC, __('Landscaping Contractor')),
    (SPC, __('Swimming Pool Contractor')),
    (KBR, __('Kitchen & Bath Remodeler')),
    (RG, __('Roofing Contractor')),
    (PL, __('Plumbing Contractor')),
    (FC, __('Fencing Contractor')),
    (HVAC, __('HVAC Contractor')),
    (DE, __('Designer')),
    (DG, __('Doors, Gates and Activating Devices')),
    (CC, __('Carpentry Contractor')),
    (COC, __('Concrete Contractor')),
    (DC, __('Drywall Contractor')),
    (EC, __('Electrical Contractor')),
    (PDC, __('Painting And Decorating Contractor')),
    (SMC, __('Sheet Metal Contractor')),
    (ME, __('MEISTER'))
)


def check_professional_type(request):
    for i in [j[0] for j in PROFESSIONAL_CHOICES]:
        if i in request.path:
            model_type = i
    return model_type