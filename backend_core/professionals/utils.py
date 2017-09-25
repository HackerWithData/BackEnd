CONTRACTOR = 'CONTRACTOR'
ARCHITECT = 'ARCHITECT'
DESIGNER = 'DESIGNER'

PROFESSIONAL_CHOICES = (
    (CONTRACTOR, 'Contractor'),
    (ARCHITECT, 'Architect'),
    (DESIGNER, 'Designer'),
)

# entity type
C = 'Corporation'
S = 'Sole Ownership'
P = 'Partnership'
ENTITY_CHOICES = (
    (C, 'Corporation'),
    (P, 'Partnership'),
    (S, 'Sole Ownership'),
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

PROFESSIONAL_SUBTYPE_CHOICES = (
    (GC, 'General Contractor'),
    (LC, 'Landscaping Contractor'),
    (SPC, 'Swimming Pool Contractor'),
    (KBR, 'Kitchen & Bath Remodelor'),
    (RG, 'Roofing Contractor'),
    (PL, 'Plumbing Contractor'),
    (FC, 'Fencing Contractor'),
    (HVAC, 'HVAC Contractor'),
    (DE, 'Designer'),
    (DG, 'Doors, Gates and Activating Devices'),
    (CC, 'Carpentry Contractor'),
    (COC, 'Concrete Contractor'),
    (DC, 'Drywall Contractor'),
    (EC, 'Electrical Contractor'),
    (PDC, 'Painting And Decorating Contractor'),
    (SMC, 'Sheet Metal Contractor')
)
