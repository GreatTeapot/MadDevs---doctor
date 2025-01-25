from common.schemas.responses import mixins as response
from modules.schemas.patients.schemas import PatientResponseSchema

PATIENT_CREATE_RESPONSES = {
    200: {"model": response.SuccessIdResponseSchema},
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    407: {"model": response.UserRolesForbidden},
    500: {"model": response.ServerErrorResponseSchema},
}

PATIENT_GET_RESPONSES = {
    200: {"model": PatientResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenResponseSchema},
    400: {"model": response.BadRequestResponseSchema},
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "Patient not found."}
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}

PATIENT_EDIT_RESPONSES = {
    200: {
        "description": "Successful Response",
        "content": {"application/json": {"example": True}},
    },
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenResponseSchema},
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "Patient record not found."}
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}
