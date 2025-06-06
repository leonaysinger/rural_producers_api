from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, FieldValidationInfo, field_validator

from app.utils.validators import validate_cnpj, validate_cpf


class RuralProducerBase(BaseModel):
    name: str
    document_type: Literal["CPF", "CNPJ"]
    document: str

    @field_validator("document", mode="before")
    @classmethod
    def validate_document(cls, value: str, info: FieldValidationInfo) -> str:
        doc_type = info.data.get("document_type")
        clean = value.replace(".", "").replace("-", "").replace("/", "")

        if doc_type == "CPF":
            if not validate_cpf(clean):
                raise ValueError("Invalid CPF")
        elif doc_type == "CNPJ":
            if not validate_cnpj(clean):
                raise ValueError("Invalid CNPJ")

        return clean


class RuralProducerCreate(RuralProducerBase):
    pass


class RuralProducerUpdate(BaseModel):
    name: Optional[str] = None
    document_type: Optional[Literal["CPF", "CNPJ"]] = None
    document: Optional[str] = None

    @field_validator("document", mode="before")
    @classmethod
    def validate_document(cls, value: str, info: FieldValidationInfo) -> str:
        doc_type = info.data.get("document_type")
        if value is None or doc_type is None:
            return value
        clean = value.replace(".", "").replace("-", "").replace("/", "")

        if doc_type == "CPF" and not validate_cpf(clean):
            raise ValueError("Invalid CPF")
        if doc_type == "CNPJ" and not validate_cnpj(clean):
            raise ValueError("Invalid CNPJ")
        return clean


class RuralProducerRead(RuralProducerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
