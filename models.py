
from sqlalchemy import (
    create_engine, Column, Integer, String, 
    ForeignKey, Date, Float, CheckConstraint, Text
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
import os

# Configuration de la connexion
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "universite")

# Création du moteur SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    pool_recycle=3600,
    echo=False  # Mettre à True pour voir les requêtes SQL
)

Session = sessionmaker(bind=engine)
Base = declarative_base()

class Etudiant(Base):
    __tablename__ = "ETUDIANT"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    date_naissance = Column(Date)
    telephone = Column(String(20))
    
    inscriptions = relationship("Inscription", back_populates="etudiant")
    examens = relationship("Examen", back_populates="etudiant")

class Professeur(Base):
    __tablename__ = "PROFESSEUR"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    specialite = Column(String(100))
    date_embauche = Column(Date, default=func.now())
    
    enseignements = relationship("Enseignement", back_populates="professeur")

class Cours(Base):
    __tablename__ = "COURS"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, unique=True)
    titre = Column(String(200), nullable=False)
    credits = Column(Integer, nullable=False, default=3)
    description = Column(Text)
    
    enseignements = relationship("Enseignement", back_populates="cours")
    inscriptions = relationship("Inscription", back_populates="cours")

class Enseignement(Base):
    __tablename__ = "ENSEIGNEMENT"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cours_id = Column(Integer, ForeignKey("COURS.id"), nullable=False)
    professeur_id = Column(Integer, ForeignKey("PROFESSEUR.id"), nullable=False)
    annee = Column(Integer, nullable=False)
    semestre = Column(String(10), nullable=False)
    salle = Column(String(20))
    
    cours = relationship("Cours", back_populates="enseignements")
    professeur = relationship("Professeur", back_populates="enseignements")

class Inscription(Base):
    __tablename__ = "INSCRIPTION"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    etudiant_id = Column(Integer, ForeignKey("ETUDIANT.id"), nullable=False)
    cours_id = Column(Integer, ForeignKey("COURS.id"), nullable=False)
    date_inscription = Column(Date, default=func.now())
    statut = Column(String(20), default="ACTIF")
    
    etudiant = relationship("Etudiant", back_populates="inscriptions")
    cours = relationship("Cours", back_populates="inscriptions")

class Examen(Base):
    __tablename__ = "EXAMEN"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    etudiant_id = Column(Integer, ForeignKey("ETUDIANT.id"), nullable=False)
    cours_id = Column(Integer, ForeignKey("COURS.id"), nullable=False)
    date_examen = Column(Date, nullable=False)
    note = Column(Float, nullable=False)
    type_examen = Column(String(50))
    
    # Contrainte de validation
    __table_args__ = (
        CheckConstraint('note >= 0 AND note <= 20', name='check_note_range'),
    )
    
    etudiant = relationship("Etudiant", back_populates="examens")

def create_tables():
    """Crée toutes les tables dans la base de données"""
    Base.metadata.create_all(engine)
    print(" Tables créées avec succès")

def drop_tables():
    """Supprime toutes les tables (à utiliser avec précaution)"""
    Base.metadata.drop_all(engine)
    print(" Tables supprimées")

def get_session():
    """Retourne une nouvelle session"""
    return Session()

if __name__ == "__main__":
    create_tables()