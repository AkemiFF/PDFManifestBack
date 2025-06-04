from sqlalchemy import (Column, Date, Float, ForeignKey, Integer, LargeBinary,
                        Numeric, String, Table, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Utilisateur(Base):
    __tablename__="utilisateur"
    
    id = Column(Integer,primary_key= True,autoincrement=True)
    identifiant = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    date_create = Column(Date,nullable=False)
    date_login = Column(Date,nullable = False)

class Vessel(Base) : 
    __tablename__= 'vessel'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),nullable=False,unique=True)
    flag = Column(String(255),nullable=False)
    
    voyages = relationship('Voyage',back_populates='vessel') 

class Voyage(Base) : 
    __tablename__ = 'voyage'

    id = Column(Integer,primary_key=True,autoincrement=True)
    vessel_id = Column(Integer,ForeignKey('vessel.id',ondelete='CASCADE'))
    code = Column(String(255),nullable=False,unique=True)
    date_arrive = Column(Date,nullable=False)

    vessel = relationship('Vessel',back_populates='voyages')
    cargos = relationship('Cargo',back_populates='voyage')
    voyage_pdf = relationship('PDF_Voyages',back_populates='voyages')

class PaysOrigine(Base):
    __tablename__ = "pays_origine"

    id = Column(Integer,primary_key=True,autoincrement=True)
    pays = Column(String,nullable = False)

    cargos = relationship('Cargo',back_populates='pays_origine')

class Cargo(Base) : 
    __tablename__ = 'cargo'

    id = Column(Integer,primary_key=True,autoincrement=True)
    voyage_id = Column(Integer,ForeignKey('voyage.id',ondelete='CASCADE'))
    port_depart = Column(String(255),nullable=False)
    shipper = Column(String(255),nullable=False)
    consignee = Column(String(255),nullable=True)
    bl_no = Column(String(50), nullable=False)
    pays_origine_id = Column(Integer,ForeignKey('pays_origine.id',ondelete='NULL'))
    quantite = Column(Integer)
    poid =  Column(Numeric(10, 2))
    volume = Column(Numeric(10,2))

    pays_origine = relationship('PaysOrigine',back_populates='cargos')
    cargo_produit = relationship('CargoProduit',back_populates='cargo')
    cargo_vin =relationship('VinProduit',back_populates= 'cargo')
    voyage = relationship('Voyage',back_populates='cargos')

class CargoProduit(Base):
    __tablename__ = 'cargo_produit'

    id = Column(Integer,primary_key=True,autoincrement=True)
    cargo_id = Column(Integer,ForeignKey('cargo.id',ondelete='CASCADE'))
    produit = Column(String(255),nullable=False)
    description_produit = Column(Text)

    cargo = relationship('Cargo',back_populates='cargo_produit')

class VinProduit(Base):
    __tablename__ = 'vin_produit'

    id = Column(Integer, primary_key = True, autoincrement= True)
    cargo_id = Column(Integer, ForeignKey('cargo.id',ondelete="CASCADE"))
    vin = Column(String(255),nullable=False)

    cargo = relationship("Cargo", back_populates= 'cargo_vin')

# Modèle pour la table `file_pdf`
class FilePDF(Base):
    __tablename__ = 'file_pdf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    pdf = Column(LargeBinary,nullable = False)
    date_ajout = Column(Date,nullable= False)
    page = Column(Integer,nullable= False)
        
    contenus = relationship("Contenu", back_populates="pdf")
    pdf_voyages = relationship("PDF_Voyages",back_populates= "pdf")



# Modèle pour la table `contenu`
class Contenu(Base):
    __tablename__ = 'contenu'
    pdf_id = Column(Integer, ForeignKey('file_pdf.id', ondelete='CASCADE'), primary_key=True)
    page = Column(Integer, primary_key=True)
    contenu = Column(Text, nullable=False)
    
    pdf = relationship("FilePDF", back_populates="contenus")


class PDF_Voyages(Base):

    __tablename__ = "pdf_voyages"

    pdf_id = Column(Integer,ForeignKey('file_pdf.id',ondelete= 'CASCADE'),primary_key=True)
    voyage_id = Column(Integer ,ForeignKey('voyage.id',ondelete='CASCADE'),primary_key= True)

    pdf = relationship("FilePDF", back_populates="pdf_voyages")
    voyages = relationship("Voyage",back_populates= "voyage_pdf")


class ManifestEntry(Base):
    __tablename__ = 'manifest_entry'

    id = Column(Integer, primary_key=True, autoincrement=False) 
    Name = Column(String(255), nullable=False)
    Flag = Column(String(10), nullable=True)
    Produits = Column(Text, nullable=True)
    Volume = Column(Float, nullable=True)
    Poids = Column(Float, nullable=False)
    Date = Column(Date, nullable=True)

    def to_dict(self) -> dict:
        return {
            "ID": self.id,
            "Name": self.Name,
            "Flag": self.Flag,
            "Produits": self.Produits,
            "Volume": self.Volume,
            "Poids": self.Poids,
            "DATE": self.Date.isoformat() if self.Date else None
        }
