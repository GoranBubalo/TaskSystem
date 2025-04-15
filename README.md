# TaskSystem
TaskFlow je distribuirani sustav za upravljanje zadacima koji omogućuje korisnicima dodavanje, ažuriranje, brisanje i pregledavanje zadataka putem REST API-ja.
 Aplikacija koristi distribuiranu obradu zadataka pomoću distribuiranih radnika, koji su odgovorni za obradu i ažuriranje statusa zadataka u sustavu. Korištenjem reda zadataka (queue), sustav omogućuje skalabilnost i visoku dostupnost, čime se omogućava učinkovito upravljanje velikim brojem korisnika i zadataka.

Tehnologije korištene u aplikaciji:
- FastAPI - Za izgradnju REST API-ja.
- Celery - Za raspodijeljenu obradu zadataka.
- Redis - Za pohranu podataka o zadacima i za red zadataka (task queue).
- PostgreSQL - Za pohranu podataka o korisnicima i zadacima.
- Docker - Za orkestraciju aplikacije i njenih komponenti (API, Celery radnici, Redis, PostgreSQL).
