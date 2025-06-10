from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def __validate_input(self, **input_data):
        required_fields = {
            "номер телефона": input_data.get("phone"),
            "e-mail": input_data.get("email"),
            "пароль": input_data.get("password"),
        }
        
        for field, value in required_fields.items():
            if not value:
                raise ValueError(f"Необходимо ввести {field}")

    def create_user(self, phone: str, email: str, password: str = None, **kwargs):
        try:
            self.__validate_input(phone=phone, email=email,
                                password=password)
        except ValueError as err:
            print(f"Ошибка: {str(err)}")

        user = self.model(phone=phone,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, email, password, **kwargs):
        try:
            self.__validate_input(phone=phone, email=email,
                                password=password)
        except ValueError as err:
            print(f"Ошибка: {str(err)}")

        user = self.model(phone=phone,
                          email=self.normalize_email(email))
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user