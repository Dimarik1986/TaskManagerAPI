from pydantic import BaseModel, Field, ConfigDict, model_validator, StrictBool, StrictStr

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str = Field(min_length=5)
    model_config = ConfigDict(str_strip_whitespace=True)
    done: bool = False



class TaskPatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: StrictStr | None = Field(default=None, min_length=5)
    done: StrictBool | None = None

    @model_validator(mode="after")
    def reject_null_values(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self