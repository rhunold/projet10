# API - SoftDesk



| typeUser  | email                    | password    | user_id 
|-----------|--------------------------|-------------|
| SuperUser | raphael.hunold@gmail.com | Héà2flzizl! | 1
| User      | toto@gmail.com           | tatatiti    | 2
| User      | max@gmail.com            | maxpass8    | 3







http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/signup/
http://127.0.0.1:8000/token/refresh/
3.	Récupérer la liste de tous les projets (projects) rattachés à l'utilisateur (user) connecté	GET	http://127.0.0.1:8000/projects/
4.	Créer un projet	POST	http://127.0.0.1:8000/projects/
5.	Récupérer les détails d'un projet (project) via son id	GET	http://127.0.0.1:8000/projects/{id}/
6.	Mettre à jour un projet	PUT	http://127.0.0.1:8000/projects/{id}/
7.	Supprimer un projet et ses problèmes	DELETE	http://127.0.0.1:8000/projects/{id}/
8.	Ajouter un utilisateur (collaborateur) à un projet	POST	http://127.0.0.1:8000/projects/{id}/users/
9.	Récupérer la liste de tous les utilisateurs (users) attachés à un projet (project)	GET	http://127.0.0.1:8000/projects/{id}/users/
10.	Supprimer un utilisateur d'un projet	DELETE		http://127.0.0.1:8000/projects/{id}/users/{id}
11.	Récupérer la liste des problèmes (issues) liés à un projet (project)	GET		http://127.0.0.1:8000/projects/{id}/issues/
12.	Créer un problème dans un projet	POST		http://127.0.0.1:8000/projects/{id}/issues/
13.	Mettre à jour un problème dans un projet	PUT		http://127.0.0.1:8000/projects/{id}/issues/{id}
14.	Supprimer un problème d'un projet	DELETE		http://127.0.0.1:8000/projects/{id}/issues/{id}

15.	Créer des commentaires sur un problème	POST		http://127.0.0.1:8000/projects/{id}/issues/{id}/comments/
16.	Récupérer la liste de tous les commentaires liés à un problème (issue)	GET		http://127.0.0.1:8000/projects/{id}/issues/{id}/comments/
17.	Modifier un commentaire	PUT		http://127.0.0.1:8000/projects/{id}/issues/{id}/comments/{id}
18.	Supprimer un commentaire	DELETE		http://127.0.0.1:8000/projects/{id}/issues/{id}/comments/{id}
19.	Récupérer un commentaire (comment) via son id	GET		http://127.0.0.1:8000/projects/{id}/issues/{id}/comments/{id}
