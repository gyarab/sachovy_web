from pydantic import Field
from pydantic import BaseModel, EmailStr


class UserCredsSchema(BaseModel):
    "zakladni udaje o uzivateli"
    email: EmailStr = Field(title="Email",
                            description="prijima jakykoliv email, ktery obsahuje @",
                            examples=["abcde@gmail.com", "example@abcde.cz"], )

    password: str = Field(min_length=5,
                          title="Heslo",
                          description="Musi obsahovat >= 5 symbolu",
                          examples=["abcdef", "qwerty229"])


class UserRegistrationSchema(UserCredsSchema):
    "zakladni udaje o uzivateli + nutny nickname pro registraci"
    name: str = Field(min_length=3, max_length=50, title="Jmeno",
                      description="3 < name < 50 znaku",
                      examples=["ahooj", "RRRRRRRR"])


class UserResponseSchema(BaseModel):
    "schema obsahuje udaje, ktere se zobrazi v odpovedi na registraci"
    name: str = Field(min_length=3, max_length=50, title="Jmeno",
                      description="3 < name < 50 znaku",
                      examples=["ahooj", "RRRRRRRR"])

    email: EmailStr = Field(title="Email",
                            description="prijima jakykoliv email, ktery obsahuje @",
                            examples=["abcde@gmail.com", "example@abcde.cz"], )