CREATE TABLE IF NOT EXISTS Hopital (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nom varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  service varchar(255) NOT NULL,
  specialite varchar(255) NOT NULL,
  date DATE NOT NULL,
  lieux varchar(255) NOT NULL,
  remuneration INTEGER NOT NULL
) 

CREATE TABLE IF NOT EXISTS Medecin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nom varchar(255) NOT NULL,
  prenom varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  specialite varchar(255) NOT NULL
  )

CREATE TABLE IF NOT EXISTS Reservation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  demande BOOL NOT NULL,
  disponibilite BOOL NOT NULL,
  id_medecin INTEGER NOT NULL,
  id_Hopital INTEGER NOT NULL
  )
  

  -- Remplir la table Hopital avec des donnees fictives
INSERT INTO Hopital (nom, email, password, service, specialite, date, lieux, remuneration)
VALUES 
('Hôpital Edouard Herriot', 'edouard_herriot@example.com', 'passwordA', 'Service de Cardiologie', 'Cardiologie', '2024-02-26', 'Place d''Arsonval, 69003 Lyon', 5500),
('Centre Hospitalier Lyon Sud', 'lyon_sud@example.com', 'passwordB', 'Service de Chirurgie Orthopedique', 'Chirurgie Orthopedique', '2024-02-27', '165 Chemin du Grand Revoyet, 69495 Pierre-Benite', 6000),
('Centre Hospitalier Lyon Sud-Est', 'lyon_sud_est@example.com', 'passwordC', 'Service de Pediatrie', 'Pediatrie', '2024-02-28', '59 Boulevard Pinel, 69500 Bron', 5800);

-- Remplir la table Medecin avec des donnees fictives
INSERT INTO Medecin (nom, prenom, email, password, specialite)
VALUES
('Dupont', 'Emmanuel', 'emmanuel_dupont@example.com', 'passwordEmmanuel', 'Cardiologie'),
('Nabil', 'Girard', 'nabil_girard@example.com', 'passwordNabil', 'Chirurgie Orthopedique'),
('Elfried', 'Leroy', 'elfried_leroy@example.com', 'passwordElfried', 'Pediatrie');

-- Remplir la table Reservation avec des donnees fictives
INSERT INTO Reservation (demande, disponibilite, id_medecin, id_Hopital)
VALUES
(1, 1, 1, 1),
(0, 1, 2, 1),
(1, 0, 3, 2);
ON CONFLICT
PRAGMA compile_options;
DROP TABLE medecins_enregistres;
-- Mettre à jour la table Reservation pour utiliser 'oui' et 'non' au lieu de 1 et 0
--ALTER TABLE Reservation
-- RENAME COLUMN demand to demande;
--UPDATE Reservation
--SET demande = 'oui'
--WHERE demande = 1;

--UPDATE Reservation
--SET demande = 'non'
--WHERE demande = 0;

--UPDATE Reservation
--SET disponibilite = 'oui'
--WHERE disponibilite = 1;

--UPDATE Reservation
--SET disponibilite = 'non'
--WHERE disponibilite = 0;
