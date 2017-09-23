CONTRACTOR = 'CONTRACTOR'
ARCHITECT = 'ARCHITECT'
DESIGNER = 'DESIGNER'

PROFESSIONAL_CHOICES = (
    (CONTRACTOR, 'Contractor'),
    (ARCHITECT, 'Architect'),
    (DESIGNER, 'Designer'),
)

# entity type
FIRM = 'FIRM'
INDIVIDUAL = 'INDIVIDUAL'
ENTITY_CHOICES = (
    (FIRM, 'Firm'),
    (INDIVIDUAL, 'Individual'),
)

# TODO: load static file into professional subtype
# professional subtype
GC = 'GC'
LC = 'LC'
SPC = 'SPC'
KBR = 'KBR'
RG = 'RG'
PL = 'PL'
FC = 'FC'
HA = 'HA'
DE = 'DE'
PROFESSIONAL_SUBTYPE_CHOICES = (
    (GC, 'General Contractors'),
    (LC, 'Landscape Contractors'),
    (SPC, 'Swimming Pool Contractors'),
    (KBR, 'Kitchen & Bath Remodelor'),
    (RG, 'Roofing & Gutters'),
    (PL, 'Plumbers'),
    (FC, 'Fence Contractors'),
    (HA, 'HV & AC'),
    (DE, 'Designers')
)
