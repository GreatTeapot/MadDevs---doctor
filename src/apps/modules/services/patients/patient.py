from datetime import datetime
from typing import TypeAlias, Union

from common.services.mixins import PaginatedPageService

EditData: TypeAlias = dict[str, Union[ str, bool, datetime, int, None]]



class PatientService(PaginatedPageService):
    """service for working with patients"""


    pass