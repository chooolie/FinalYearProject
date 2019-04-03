from django.utils.translation import gettext as _
GENDER_CHOICES = (
    ("F", _("Female")),
    ("M", _("Male")),
    ("O", _("Other"))
)
AGE_CHOICES = (
    ("Under18", _("Under18")),
    ("18-24", _("18-24")),
    ("25-34", _("25-34")),
    ("35-44", _("35-44")),
    ("45-49", _("45-49")),
    ("50-55", _("50-55")),
    ("56+", _("56+"))
)

JOB_CHOICES = (
    ("K-12student", _("School Student")),
    ("self-employed", _("Self Employed")),
    ("scientist", _("Scientist")),
    ("executive/managerial", _("Executive or Managerial")),
    ("writer", _("Writer")),
    ("homemaker", _("Home maker")),
    ("academic/educator", _("Academic or educator")),
    ("scientist", _("Scientist")),
    ("doctor/health care", _("Doctor or Health care")),
    ("sales/marketing", _("Sales or Marketing")),
    ("clerical/admin", _("Clerical or Admin")),
    ("programmer", _("Programmer")),
    ("technician/engineer", _("Technician or Engineer")),
    ("college/grad student", _("College or Grad student")),
    ("artist", _("Artist")),
    ("tradesman/craftsman", _("Tradesman or Craftsman")),
    ("retired", _("Retired")),
    ("unemployed", _("Unemployed")),
    ("other", _("Other")),

)
