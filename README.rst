Italian PostgreSQL Localization
===============================

This project contains the current state of the PostgreSQL Italian translation
files, together with a few development tools.

Questo progetto contiene lo stato corrente della traduzione italiana di
PostgreSQL e alcuni tool di sviluppo.


Note per il prossimo traduttore
-------------------------------

Usa poedit almeno versione 1.5: le versioni precedenti si prendono la libertà
di riformattare i commenti, creando diff spuri.

Usa una versione di poedit con lo spellcheck. Se non ce l'ha, compilatelo tu:
non è difficile.

Usa un carattere non proporzionale per la finestre di input, altrimenti è
impossibile verificare che l'output sia allineato dove serve.

Disattiva l'opzione View -> Untranslated entries first, altrimenti ad ogni
salvataggio il lavoro fatto viene mescolato a quello da fare ed usare i
segnalibri diventa inutile.


Commandi per lo sviluppo
------------------------

make [all]
    compila tutti i .po in .mo

make check
    Effettua controlli sulla traduzione (consistenza segnaposti, spaziatura,
    traduzione dei parametri ecc.)

make dlpots
    Scarica da babel.postgresql.org la versione più recente dei file .pot

make updatepots
    Unisci le traduzioni correnti ai file .pot scaricati

make update
    Riporta gli aggiornamenti fatti all'ultima versione sulla versione
    precedente ecc.

make popack
    Crea un archivio per version con i file ``.po``, utile per l'invio a
    PostgreSQL NLS.

make mopack
    Crea un archivio per versione con i file ``.mo`` utile per testare con
    PostgreSQL.


Sulla traduzione
----------------

Non tradurre il plurale delle parole inglesi: file e non files.

La traduzione di directory è directory, non cartella. "Cartella" è un
microsoftismo.

La versione maiuscola di "è" è "È" e non "E'". Il modo più facile di digitarla
su Linux è di scrivere è col Caps Lock attivo.

Se hai un dubbio, su qualche parola, controlla come è stata fatta in passato.
Per esempio, come è tradotto "database cluster"? ::

	grep -i -A1 "database cluster" *.po

Otterrai i messaggi che usano la stringa e le relative traduzioni e potrai
fartene un'idea.

Sei il futuro Gadda e il linguaggio te lo manipoli come vuoi? Grande, siamo
felici tu sia con noi. Ma la consistenza è più importante di altri fattori in
questa traduzione, per consentire all'utente di capire se due messaggi si
riferiscono agli stessi elementi. Quindi se sei convinto che "cluster di
database" sia meglio tradotto come "ammasso di database", cambia *tutte* le
occorrenze, non solo l'ultima che trovi.

In inglese, nelle liste, si usa una virgola `anche prima dell'ultimo
elemento`__. In italiano no. Quindi la traduzione di:

	The three little pigs are Browny, Whitey, and Blacky

è:

	I tre porcellini sono Timmi, Tommi e Gimmi.

.. __: http://en.wikipedia.org/wiki/Serial_comma

Per descrivere comandi dati dall'utente al database, usa l'imperativo. Per
esempo negli help della riga di comando. traduci "read the password from the
file" come "leggi la password dal file".

Quando il database si rivolge all'utente, usa l'imperativo.  "Esegui fixdb se
non vuoi perdere tutti i tuoi dati", non "eseguite" o "eseguire".

Se il programma ha un output allineato (es. i messaggi di --help) rispetta
l'allineamento e non far andare le stringhe a zig zag.

Gli autori di postgres fanno molta attenzione alla distinzione tra i messaggi
d'errore dovuti a qualcosa che è assolutamente impossibile fare, per i quali
usano la forma *cannot*:

    cannot build the roof before the floor

e qualcosa che è fallito per cause momentanee e può riuscire se le condizioni
cambiano, con *could not*:

    could not find the socks in the drawer

La traduzione scelta è stata rispettivamente:

    non è possibile costruire il tetto prima del pavimento

    non è stato possibile trovare i calzini nel cassetto

Ovviamente sono possibili variazioni per un concetto così generico; sarebbe
auspicabile comunque mantenere la distinzione tra i due sensi degli errori.

Se le stringhe originali hanno un segnaposto alla fine, questo non dovrebbe
essere spostato. Non tradurre:

    file not found: %s

con:

    il file %s non è stato trovato

Il segnaposto alla fine è usato per rendere più evidente il valore, o più
leggibile l'intera frase se la variabile può essere arbitrariamente lunga.


Traduzioni di termini abbastanza comuni
---------------------------------------

* bug: bug, non bachi (e neanche errori: non sono quelli da segnalare alla
  mailing list.)
* client-side: lato client
* collate: ordinamento
* constraint: vincolo
* database cluster: cluster di database
* default: predefinito
* encoding: codifica
* error code: codice errore
* exit code: codice di uscita (inteso di processi e thread)
* false (is false): è disabilitato
* get: ottenere, trovare (a seconda del contesto: ottenere informazioni, trovare un valore)
* identifier: identificativo, non identificatore
* invalid: non valido (non "invalido")
* line: riga (di un file)
* location: posizione
* log file: file di log
* owenership: il proprietario, non la proprietà (quest'ultimo è ambiguo)
* return: restituire, non tornare o ritornare
* server-side: lato server
* set: impostare, non settare (non c'è puttare o gettare, no?)
* shell (tipo di dato): non completamente definito
* subquery: sottoquery
* superuser: superutente
* stat: ottenere informazioni
* true (is true): è abilitato
* unrecognized: sconosciuto


Termini non tradotti
--------------------

Se esiste un modo ragionevole di tradurli, ok per me.

* advisory lock
* backslash
* code point (Unicode)
* commit
* escape
* inline, inlining
* join
* large object
* log
* pipe (forse coda?)
* standby
* stream (forse flusso -- solo per i WAL?)
* tablespace
* thread
* timeline
* wrapper
