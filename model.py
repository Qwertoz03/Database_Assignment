from dataclasses import dataclass

@dataclass
class Book:
    id: int             
    title: str
    isbn: str
    pub_year: int        
    genre_id: int        
    publisher_id: int    

@dataclass
class Publisher:
    id: int              
    name: str
    address: str
    phone: str
    email: str

@dataclass
class Member:
    id: int         
    first_name: str
    last_name: str
    address: str
    email: str
    membership_date: str