* Run ./run.sh, then bin/pip install zope.component
* Start app with bin/python e01_zca_intro.py

Q: Care e problema pe care incercam sa o rezolvam?
---------------------------------------------------
A: extinderea (plugability).
A: compozitia in defavoarea mecanismului de inheritance => big fat objects

Mecanisme de extindere:

* fixed API - o povara pentru library maintainers
* setuptools entry points & plugins - recent addition
* python2.6+ - Abstract Base Classes (ABCs)
* middleware (WSGI, Django)
    - discovery through magic vars
    - PasteScript (.ini) apps + definition. Wsgi apps. Pyramid Project

Q: Cine are nevoie de mecanisme de extindere?
A: Orice librarie cu un nivel mai mare de functionalitate

E mai simplu sa faci de la inceput o librarie extensibila decat sa anticipezi
toate nevoile viitoare posibile. Dar trebuie evitata fragmentarea in mult
prea multe "plug points".

Exemplu eea.rdfmarshaller:

* http://<obj>/@@rdf este un aspect al obiectelor publicate prin Zope. 
* Nu toate obiectele publicate sunt de acelasi tip: 
    * exista derivate Archetypes, 
    * exista Dexterity, 
    * CMF objects, etc.
* Pentru derivate Archetypes, rdf foloseste Schema obiectului. 
    * un Field de tip String nu inseamna acelasi lucru pentru orice tip de context. 
        * putem folosi "named adapters" pentru discriminare
* Un alt mecanism de extindere sunt pluginurile ce modifica sesiunea, 
  implementate ca subscriberi.


Zope Component Architecture
---------------------------
- Asigura functionalitate prin obiecte mici cuplate, in contrast 
  cu designul clasic in care se folosesc obiecte uriase, cu 
  functionalitate multa atasata.
- componentele comunica intre ele prin API definit prin zope.interface.Interface
- interfetele descriu metodele si proprietatile pe care un obiect ar trebui sa le aiba
- un adapter foloseste un obiect drept context pentru a produce 
  un alt obiect, cu o interfata diferita.
- Folosind ZCA este o metoda simpla de a face o aplicatie 
  "pluggable" pana la cel mai mic nivel

Interfetele
-----------
zope.interface

Interfetele sunt obiecte care specifica si documenteaza comportamentul
"extern" al obiectelor care le "asigura (provide)". Interfetele descriu 
comportamentul prin:

* documentare informala
* definire de attribute
* invariante (validare a obiectelor)

Interfetele sunt un "contract informal" - nu este un sistem de static typing.

Interfata cea mai de baza e zope.interface.Interface. Absolut toate obiectele o asigura

>>> zope.interface.Interface.providedBy(object())
True

* Marker interfaces (marcam obiecte ca fiind de un anume "tip")
* interface "types"


Componentele
------------
Obiecte care asigura o interfata sunt denumite componente. In momentul folosirii
ZCA, toate obiectele pot fi considerate componente.

* un obiect "provides"
* un factory (o clasa) "implements"


Utilities
---------
* Paternul singleton
* Local utilities in local site manager


Adaptori
--------
* paternul "adapter" din Design Patterns (GoF)
* Reprezinta un aspect al unuia sau mai multe obiecte. Cel mai de baza mecanism de extindere
din ZCA.
* single adapters
* multiAdapter


Subscribers
-----------
Un adaptor special, cand ne intereseaza mai multi adaptori similari pentru o interfata. Subscriberii
pot sa intoarca un rezultat


Subscription (event) handlers
------------------------------
La fel ca subscriberii, dar nu se asteapta un rezultat. Exemplu: event handlers


Site manager
------------
Registrul ZCA. Exista registrul global (getGlobalSiteManager) si local sites (foldere ISite). La
nivelul local sites se pot inregistra local utilities - apoi 
getUtility(ISomething, context=persistentobj)


Overrides
---------
* zcml
* browser:view + layer
* local utils


ZCML
----
* namespaces
* includes
* conditions
* meta.zcml
