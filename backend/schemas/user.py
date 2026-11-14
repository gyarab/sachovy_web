from uuid import UUID

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
    "schema obsahuje udaje, ktere se zobrazi v odpovedi"
    id: UUID = Field(title="ID uzivatele", description="UUID uzivatele", examples=["123e4567-e89b-12d3-a456-426655440000"])

    name: str = Field(min_length=3, max_length=50, title="Jmeno",
                      description="3 < name < 50 znaku",
                      examples=["ahooj", "RRRRRRRR"])

    email: EmailStr = Field(title="Email",
                            description="prijima jakykoliv email, ktery obsahuje @",
                            examples=["abcde@gmail.com", "example@abcde.cz"], )

    ELO: int = Field(title="ELO", description="ELO uzivatele", examples=[1000, 10000])

    vyhry: int = Field(title="Vyhry", description="Pocet vyhranych her uzivatele", examples=[0, 1000])

    prohry: int = Field(title="Prohry", description="Pocet prohranych her uzivatele", examples=[0, 1000])
