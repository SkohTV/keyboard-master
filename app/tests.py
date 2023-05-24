"""
Tests
===========

Ce module contient les tests pour vérifier que les fonctions utilitaires et de connexion au serveur fonctionnent correctement

Utilisation :
-------------
	Pour exécuter l'application, exécutez ce fichier directement à l'aide de l'interpréteur Python

	$ py tests.py

"""



from src.utils import export_gamemodes, threaded, User
from src.connect_server import user_connection, query_sentence



# Ne s'exéctue que si tests.py est lancé, pas importé
if __name__ == "__main__":
	print("Début des tests...")

	# Test du fichier utils.py
	assert export_gamemodes([]) == "", "Échec | utils.py | Test 1 : Liste vide"
	assert export_gamemodes(["a"]) == "a", "Échec | utils.py | Test 2 : Liste avec un élément"
	assert export_gamemodes(gmlst := ["easy", "insane"]) == "easy-insane", "Échec | utils.py | Test 3 : Liste avec plusieurs éléments"
	assert threaded(lambda: print("test")) is not None, "Échec | utils.py | Test 4 : Décorateur threaded"
	assert User().hashed_password is None, "Échec | utils.py | Test 5 : Objet User vide"
	assert (usr := User("a", "b")) and usr.name == "a" and usr.hashed_password == "b", "Échec | utils.py | Test 6 : Objet User avec un nom et password"

	# Test du fichier connect_server.py
	assert isinstance(usr := user_connection(False, "TestUser1", "abcde"), User), "Échec | connect_server.py | Test 7 : Connexion d'un utilisateur"
	assert isinstance(sentc := query_sentence(gmlst), str) and sentc != "Denied", "Échec | connect_server.py | Test 8 : Requête d'une phrase"
	#? On ne test pas toutes les fonctions car certaines écrivent dans la database, et on souhaite l'éviter
	#? Car si plusieurs personnes font le même tests, des conflits d'écriture risquent d'apparaitre

	# Test du fichier app.py & frames
	#? C'est difficile de tester une interface graphique via des asserts, on va donc éviter de le faire


	print("Tous les tests ont été effectués avec succès !")
