from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class RoleName(str, Enum): 
    ADMIN = "ADMIN" 
    MEMBER = "MEMBER" 


@dataclass 
class Role:
    role_id: int 
    role_name: RoleName

    def __post_init__(self) -> None: 
        self._validate() 

    def _validate(self) -> None: 
        if not isinstance(self.role_id, int) or self.role_id <= 0: 
            raise ValueError("role_id phải là số nguyên dương (>0).") 
        
        if not isinstance(self.role_name, RoleName): 
            raise TypeError("role_name phải thuộc enum RoleName.")
    
    def is_admin(self) -> bool: 
        return self.role_name == RoleName.ADMIN
    
    def is_member(self) -> bool:
        return self.role_name == RoleName.MEMBER
    
    @classmethod
    def create_admin_role(cls, role_id: int = 1):
        return cls(role_id=role_id, role_name=RoleName.ADMIN)
    
    @classmethod
    def create_member_role(cls, role_id: int = 2):
        return cls(role_id=role_id, role_name=RoleName.MEMBER)
    
    def to_dict(self) -> dict: 
        return { 
            "role_id": self.role_id, 
            "role_name": self.role_name.value
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            role_id=data.get("role_id", 0),
            role_name=RoleName(data.get("role_name", "MEMBER"))
        )