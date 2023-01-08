from django.contrib.auth.hashers import Argon2PasswordHasher as _Argon2PasswordHasher


class Argon2PasswordHasher(_Argon2PasswordHasher):
    time_cost = 1
    memory_cost = 1024 * 10
    parallelism = 12
