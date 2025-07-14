from enum import Enum


class AppStatus(Enum):
    SUCCESS = "SUCCESS", 200, "SUCCESS."
    DELETE_SUCCESS = "DELETE_SUCCESS", 200, "Delete successfully."
    SEND_MAIL_SUCCESS = "SEND_MAIL_SUCCESS", 200, "Send email success."
    USER_LOGOUT_SUCCESS = 'USER_LOGOUT_SUCCESS', 200, "User logout successfully."
    DELETE_ACCOUNT_SUCCESS = "DELETE_ACCOUNT_SUCCESS", 200, "Delete account successfully."

    INVALID_ID = "INVALID_ID", 400, "Invalid ID."
    USER_NOT_EXIST = "USER_NOT_EXIST", 400, "User not exist."
    EMAIL_NOT_EXIST = "EMAIL_NOT_EXIST", 400, "Email not exist."
    NOT_REFRESH = "NOT_REFRESH", 400, "Refresh token is required."
    PERMISSION_DENIED = "PERMISSION_DENIED", 400, "Permission denied."
    STADIUM_NOT_EXIST = "STADIUM_NOT_EXIST", 400, "Stadium not exist."
    SOCCER_FIELD_NOT_EXIST = "SOCCER_FIELD_NOT_EXIST", 400, "Soccer field not exist."
    INVALID_VERIFY_CODE = "INVALID_VERIFY_CODE", 400, "Invalid verification code."
    EMAIL_ALREADY_EXIST = "EMAIL_ALREADY_EXIST", 400, "User with email already exists."
    USERNAME_ALREADY_EXIST = "USERNAME_ALREADY_EXIST", 400, "User with username already exists."

    ENTER_USERNAME_OR_EMAIL = "ENTER_USERNAME_OR_EMAIL", 400, "Please enter the username or email."
    USERNAME_OR_PASSWORD_INCORRECT = "USERNAME_OR_PASSWORD_INCORRECT", 400, "Username or password is incorrect."

    @property
    def message(self):
        return {
            'message': str(self.value[2]),
            'code': str(self.value[1]),
            'data': 'success' if self.value[1] in [200, 201] else 'failed'
        }
