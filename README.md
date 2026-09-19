# Fusionner les PDFs 

Placez tous les fichiers PDF à fusionner dans le dossier du projet, puis exécutez :

```bash
python3 -m pip install -r requirements.txt
python3 merge_pdfs.py --dir . --output resultat.pdf
```

Le script tri les fichiers par ordre naturel (ex: page1.pdf, page2.pdf, ...)
