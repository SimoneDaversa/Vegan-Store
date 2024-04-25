
"""
    Si vuole gestire un negozio di prodotti vegani.
    Questo programma ha come funzioni:
        - elenca: per avere l'elenco dei prodotti nel magazzino, le quantità, e i prezzi
        - aggiungi: aggiungere nuovi prodotti al magazzno o aggiungre nuove quantita di prodotto se esso è gia disponibile
        - vendita: per vendere un singolo prodotto al cliente e registrare tale vendita nel relativo registro cumulato 
        - profitti: restituire i relativi profitti del negozio in vari livelli di dettaglio ( totale negozio, tutti i prodotti uno ad uno e per un singolo prodotto)
"""
"""
    ho scelto di usare come file di salvattaggio un tipo json per avere la comodita di risalire alle due sezioni anche a livello visivo:
        - magazzino: mantenere le informazioni relative al magazzino
        - vendita aggregata: mantenere le informazioni relative alle vendita e i profitti
    in ognuna di queste sezioni vi è ogni prodotto
    il tipo di struttura scelto è il dizionario cosi da poter modificare qualsiasi dato interno ad esso compresi i prezzi. 
    L'idea sarebbe in futuro di aggiungere una sezione per programmare sconti e modificare i prezzi in vista di aumenti di costo
"""

"""
    importo i moduli necessari:
    - json per operare sul tipo di file scelto come base di salvataggio
    - os per verificare se esiste gia il file nella directory di lavoro
"""
import json
import os

# uso una variabile che terrà traccia se trovo il file json predisposto al salvataggio delle informazioni
trova = False

def scrivi_file( negozio):
    with open("inventory.json", "w") as json_file :
        json.dump( negozio, json_file, indent = 3)
        
def leggi_file ():
    with open("inventory.json", "r") as json_file :
        negozio = json.load(json_file)
    return negozio

# avvio un ciclo che scorre tutti i file della workdirectory e controllo se trovo il file di salvataggio
for i in range (len ( os.listdir())) :
    if os.listdir()[i] == "inventory.json":
        trova = True

# se non trovo il file di salvataggio lo creo
if not trova:
    negozio = {"magazzino":{},"vendita_aggregata":{}}
    scrivi_file( negozio)
    





# questa funzione verrà usata per verificare se un inserimento che deve essere numerico è effettivamente numerico
# si il parametro floor è quello sotto al quale il nuovo inserimento non puo andare, di default 0
def convalida_numero( floor = 0):
    
    goodinput = False
    while not goodinput:
        try:
            valore_input = float( input())
            if valore_input > floor:
                goodinput = True
            else:
                print( f"Il numero deve essere maggiore di {floor}. Riprova: ")
        except ValueError:
            print("Si richiede l'inserimento di un numero. Riprova: ")
    
    return (valore_input)

# questa funzione verrà usata per verificare se un inseriomento rispetta i comandi disponibili
def convalida_scelta( opzione_1 = True, opzione_2 = True, opzione_3 = True):
    
    goodinput = False
    while not goodinput:
        comando = input( )
        if comando == opzione_1 or comando == opzione_2 or comando == opzione_3:
            goodinput = True
        else:
            print("il comando inserito non è tra le opzioni concesse. Riprova: ")
    
    return comando

















def aggiungi():
    
    print( "\nbenvenuto nella funzione per aggiungere nuovi prodotti o aggiungere quantità ai prodotti gia esistenti\n")
    
    # apro il file in lettura e assegno il tutto ad una variabile
    negozio = leggi_file()
    
    # creo una variabile di controllo per il continuo inserimento di prodotti
    continua = "y"
    
    # con questo ciclo continuo ad aggiungere prodotti finche l'utente risponde di si (yes)
    while continua != "n":
        
        #ottengo tutti i nomi dei prodotti gia registrati nel magazzino 
        prodotti_registrati = list( negozio["magazzino"].keys())
    
        # input nel nome del prodotto da registrare o aggiornare
        nome_prodotto = input( "inserisci il nome del prodotto da aggiungere al magazzino o da aggiornare per quantita: ")
        
        """
            dopo aver ottenuto il nome del prodotto controllo se gia esiste
            se esite aggiorno la quantita in magazzino 
            se non esiste aggiungo in nuovo prodotto
        """
        if nome_prodotto in prodotti_registrati:
            
            """
                il prodotto è già registrato
                ottengo la quantita di prodotto da aggiungere
                controllo che la quantita inserita sia positiva, maggiore di 0 
                altrimenti stampo un'eccezzione su schermo e faccio rinserire il valore
            """
            print( "inserisci la quantita di prodotto da aggiungere a quella gia esistente")
            quantita_da_aggiungere = convalida_numero( floor = 0)
            
            # aggiungo la quantita nuova a quella che avevamo gia in magazzino
            quantita_prodotto = quantita_da_aggiungere + negozio["magazzino"][nome_prodotto]["quantita"]
            
            # lascio i prezzi di acquisto e vendita invariati
            prezzo_acquisto_prodotto = negozio["magazzino"][nome_prodotto]["prezzo_acquisto"]
            prezzo_vendita_prodotto = negozio["magazzino"][nome_prodotto]["prezzo_vendita"]
            
        else: 
            
            """
                il prodotto scelto non esiste ancora
                ottengo in input le altre variabili del magazzino: quantita, prezzo_acquisto, prezzo_vendita
                su ognuna di esse controllo che siano positive e maggiori di 0
                in particolare si richiede che il prezzo di vendita sia maggiore di quello di acquisto cosi da non andare in perdita
                se non conformi alle regole stampo un messaggio d'errore e faccio rinserire
            """
            # input della quantita
            print( "inserisci la quantita del prodotto da aggiungere al magazzino")
            quantita_prodotto = int( convalida_numero ( floor = 0))
             
            # input del prezzo acquisto per il negozio       
            print( "inserisci il prezzo di acquisto del prodotto")
            prezzo_acquisto_prodotto = round( convalida_numero ( floor = 0), 2)
            
            # input del prezzo di vendita       
            print( "inserisci il prezzo di vendita del prodotto")
            prezzo_vendita_prodotto = round( convalida_numero( floor = prezzo_acquisto_prodotto), 2)
            
        # inserisco le variabili perse in input nel dizionario
        negozio["magazzino"][nome_prodotto.lower()] = { "quantita": quantita_prodotto, "prezzo_acquisto": prezzo_acquisto_prodotto, "prezzo_vendita":prezzo_vendita_prodotto}
        
        """
            chiedo all'utente se vuole inserire nuovi prodotti
            e verifico se è tra le due possibilita di scelta.
            se si sbaglia inserire faccio continuare fino a quando
            non sceglie tra y e n
        """
        print( "scegli y per continuare ad inserire e n per smettere di inserire")
        continua = convalida_scelta( opzione_1 = "y", opzione_2 = "n")
    
    # alla fine degli inserimenti salvo tutto sul file 
    scrivi_file(negozio)
    

    
def elenca():
    
    print( "\n benvenuto nella funzione di elenco dei prodotti persenti in magazzino, qui portrai elencare i soli nomi dei prodotti o tutto il dettaglio del magazzino \n")
    
    # apro il file in lettura
    negozio = leggi_file()
    
    # ottengo la lista delle chiavi (nomi dei prodotti) del magazzino
    prodotti = list( negozio["magazzino"].keys())
    
    # ottengo in input che tipo di elenco vuole l'utente
    print( "inserisci:\n - 'prodotti' se vuoi i solo elenco dei prodotti presenti in magazzino\n - 'dettaglio' se vuoi il dettaglio magazzino con prodotti, quantita e prezzi\n")
    scelta = convalida_scelta( opzione_1= "prodotti", opzione_2= "dettaglio")
    
    # controllo la scelta di elenco fatta dall'utente e in base a quella stampo su schermo le diverse informazioni ottenute
    if scelta.lower() == "prodotti":
        print( "ecco l'elenco di tutti i prodotti presenti in magazzino:\n")
        
        # con un ciclo for scorro tutte le chiavi del magazzino per stamparle essendo i nomi dei relativi prodotti
        for i in range( 0, len (prodotti)):
            print(prodotti[i])
            
    else:
        print ("ecco il dettaglio di tutto il magazzino:\n")
        
        # con un ciclo for scorro tutte le chiavi del magazzino per stampare i relativi dettagli dei prodotti registrati
        for i in range( 0, len (prodotti)):
            
            # ottengo i relativi dettagli di quantita e prezzi per ogni prodotto
            quantita = negozio["magazzino"][prodotti[i]]["quantita"]
            prezzo_acquisto = negozio["magazzino"][prodotti[i]]["prezzo_acquisto"]
            prezzo_vendita = negozio["magazzino"][prodotti[i]]["prezzo_vendita"]
            
            # stampo una frase user friendly per comunicare i dettagli del magazzino
            print( f" il prodotto '{prodotti[i]}' è presente in magazzino con una quantita: {quantita} è stato acquistato a {prezzo_acquisto} e viene venduto a {prezzo_vendita}")
    
    
    
    
def vendita():
    
    print("\nbenvenuto nel reparto di vendita del negozio \nqui potrai vendere i prodotti scelti dal cliente:\n")
    
    # apro il file in lettura
    negozio = leggi_file()
        
    # ottengo tutti i prodotti, sotto forma di chiave, del magazzino
    prodotti_registrati = list( negozio["magazzino"].keys())
    
    # ottengo tutti i prodotti, sotto forma di chiave, delle vendite aggregate
    prodotti_venduti = list( negozio["vendita_aggregata"].keys())
    
    # effettuo un controllo sull'input del prodotto da comprare
    goodinput = False
    while not goodinput:
        try:
            # ottengo in input che prodotto si ha intenzione di comprere
            nome_prodotto = input( "inserisci il nome del prodotto da comprare: ")
            
            # mi ricavo la relativa quantita presente in magazzino
            quantita_magazzino = negozio["magazzino"][nome_prodotto]["quantita"]
            
            # se il prodotto è presente in magazzino e ha una quantita maggiore di 0 si puo acquistare 
            # altrimenti stampo dei messaggi di errore in base alla scelta effettuata dall'utente
            if nome_prodotto in prodotti_registrati and quantita_magazzino > 0:
                goodinput = True
            else:
                print( "il prodotto non è attualmente disponibile. \nti chiediamo di sceglierne un'alto\n")
        except KeyError:
            # creo un messaggio sull'errore 'keyerror' preche uso l'inserimento come chiave di ricerca
            # se questa chiave non corrisponde con quelle disponibili stampo un messaggio di errore personalizzato al caso
            print("prodotto inesistente. \nrichiedi la lista dei prodotti e riprova l'acquisto\n")
    
    
    # ottengo in input la quantita di prodotto desiderata e controllo che rispetta le seguenti caratteristiche
    # - sia un numeropositivo
    # - sia maggiore o uguale alla quantita del prodotto disponibile in magazzino
    goodinput = False
    while not goodinput:
        try:
            quantita_prodotto = int( input( "inserisci la quantita di prodotto da comprare: "))
            if quantita_prodotto > 0:
                if quantita_prodotto <= quantita_magazzino:
                    goodinput = True
                else:
                    print( f"puoi scegliere una quantita massima di {quantita_magazzino}")
            else:
                print("Il numero deve essere positivo e maggiore di 0. Riprova: ")
        except ValueError:
            print("Si richiede l'inserimento di un numero. Riprova: ")
    
    # mi calcolo la nuova quantita di prodotto disponibile in magazzino        
    quantita_magazzino = quantita_magazzino - quantita_prodotto
    
    
    
    
    # ottengo dal magazzino i prezzi relativi al prodotto selezionato
    prezzo_acquisto_prodotto = negozio["magazzino"][nome_prodotto]["prezzo_acquisto"]
    prezzo_vendita_prodotto = negozio["magazzino"][nome_prodotto]["prezzo_vendita"]
    
    # aggiorno la il magazzino con la nuova quantita
    negozio["magazzino"][nome_prodotto.lower()] = { "quantita": quantita_magazzino, "prezzo_acquisto": prezzo_acquisto_prodotto, "prezzo_vendita":prezzo_vendita_prodotto}
    
    # mi calcolo il profitto lordo che si realizzano dalla vendita del prodotto facevdo quantita*prezzo_vendita (lordo perche non ho ancora tolto le spese del prodotto)
    profitto_lordo = round( prezzo_vendita_prodotto * quantita_prodotto, 2)
    
    # mi calcolo il profitto netto ottenuto dalla differenza dei prezzi di venidta e acquisto per la relativa quantita venduta
    profitto_netto = round( ( prezzo_vendita_prodotto - prezzo_acquisto_prodotto) * quantita_prodotto, 2)

    # controllo del i prodotto che il cliente sta comprando è gia disponibile nel registro vendite
    if nome_prodotto in prodotti_venduti:
        
        # il prodotto è gia presente nel registro vendite
        # ottengo la vecchia quantita di prodotto venduta e aggiungo la nuova venduta
        vecchia_quantita = negozio["vendita_aggregata"][nome_prodotto.lower()]["quantita"]
        nuova_quantita = vecchia_quantita + quantita_prodotto
        
        # ottengo il vecchio profitto lordo del prodotto venduto e aggiungo il nuovo 
        vecchio_profitto_lordo = negozio["vendita_aggregata"][nome_prodotto.lower()]["profitto_lordo"]
        nuova_profitto_lordo = vecchio_profitto_lordo + profitto_lordo
        
        # ottengo il vecchio profitto netto del prodotto venduto e aggiungo il nuovo 
        vecchio_profitto_netto = negozio["vendita_aggregata"][nome_prodotto.lower()]["profitto_netto"]
        nuova_profitto_netto = vecchio_profitto_netto + profitto_netto
        
        # aggiungo tutto al dizionario
        negozio["vendita_aggregata"][nome_prodotto.lower()] = { "quantita": nuova_quantita, "profitto_lordo": nuova_profitto_lordo, "profitto_netto":nuova_profitto_netto}
    else:
        
        # il prodotto non era presente tra vendite quindi lo inserisco
        negozio["vendita_aggregata"][nome_prodotto.lower()] = { "quantita": quantita_prodotto, "profitto_lordo": profitto_lordo, "profitto_netto":profitto_netto}
    
    # stampo un messaggio all'utente conil resoconto della vendita
    print (f"il signore ha comprato il prodotto {nome_prodotto} con una quantita di {quantita_prodotto} per un valore totale di {profitto_lordo}\n")
    
    
    if quantita_magazzino == 0:
        negozio["magazzino"].pop(nome_prodotto)
    
    # alla fine degli inserimenti salvo tutto sul file 
    scrivi_file(negozio)
    
    
    
    
    
            
    
            
    
    
def profitti():
    print("benvenuto nella funzione dei profitti")
    
    # apro il file in lettura
    negozio = leggi_file()
    
    # ottengo le chiavi dei singoli prodotti che sono registrati come venduti
    prodotti_vendita = list( negozio["vendita_aggregata"].keys())
    
    # ottengo in input che tipo di dettaglio si vuole del reparto vendita
    # controllo che l'inserimento risepetta i comandi permessi, 
    # in caso contrario richiedo un nuovo inserimento finche il comando inserito rispetta quelli permessi
    print( "inserisci: \n - 'aggregato' se vuoi l'aggregato di tutto il negozio  \n - 'dettaglio' se vuoi i profitti di ogni singolo prodotto \n - 'singolo prodotto': se vuoi i profitti di un singolo prodotto\n")       
    scelta = convalida_scelta( opzione_1 = "aggregato", opzione_2= "dettaglio", opzione_3 = "singolo prodotto")
    
    # controllo che scelta di dettaglio ha fatto l'utente
    if scelta.lower() == "aggregato":
        
        # inizializzo delle variabili per ottenere i dati registrati
        profitti_lordi_totali = 0
        profitti_netti_totali = 0
        quantita_vendita_totale = 0

        # itero su tutti i prodotti 
        for i in range(0, len(prodotti_vendita)):
            
            # ottengo tutti i dati dei del registro di vendita aggregandoli per avere il totale del negozio
            profitti_lordi_totali = profitti_lordi_totali + negozio["vendita_aggregata"][prodotti_vendita[i]]["profitto_lordo"]
            profitti_netti_totali = profitti_netti_totali + negozio["vendita_aggregata"][prodotti_vendita[i]]["profitto_netto"]
            quantita_vendita_totale = quantita_vendita_totale + negozio["vendita_aggregata"][prodotti_vendita[i]]["quantita"]
        
        # stampo un messaggio per fornire i valori di vendita del negozio all'utente
        print( f"il negozio ha venduto una quantita totale di prodotti pari a {quantita_vendita_totale}, incassando {profitti_lordi_totali} e guadagnando {profitti_netti_totali}")
            
    elif scelta.lower() == "dettaglio":
        
        for i in range( 0, len (prodotti_vendita)):
            
            #per ogni prodotto ottengo i dati dei profitti e quantita
            quantita = negozio["vendita_aggregata"][prodotti_vendita[i]]["quantita"]
            profitto_lordo = negozio["vendita_aggregata"][prodotti_vendita[i]]["profitto_lordo"]
            profitto_netto = negozio["vendita_aggregata"][prodotti_vendita[i]]["profitto_netto"]
            
            # stampo su schermo i dati di ogni prodotto
            print( f"del prodotto '{prodotti_vendita[i]}' è stata venduta una quantita pari a: {quantita} incassando {profitto_lordo} e guadagnando {profitto_netto}")
    else:
        
        goodinput = False
        while not goodinput:
            
            # chiedo all'utente di che prodotto vuole sapere le vendite cosi da poter capire se sta vendendo o no
            prodotto_scelto = input( "scegli un prodotto del quale vuoi sapere i profotti: \n")
            if prodotto_scelto in prodotti_vendita:
                goodinput = True
            else:
                print("il prodotto scelto non è mai stato venduto")
        
        # ottengo i dattagli del prodotto scelto
        quantita = negozio["vendita_aggregata"][prodotto_scelto.lower()]["quantita"]
        profitto_lordo = negozio["vendita_aggregata"][prodotto_scelto.lower()]["profitto_lordo"]
        profitto_netto = negozio["vendita_aggregata"][prodotto_scelto.lower()]["profitto_netto"]
        
        # comunico all'utente i dettagli del prodotto scelto
        print( f"del prodotto '{prodotto_scelto.lower()}' è stata venduta una quantita pari a: {quantita} incassando {profitto_lordo} e guadagnando {profitto_netto}")
            
            
            

    
    
    
    
def chiudi():
    print("\nil programma si sta chiudento \ngrazie e arrivederci\n")
    
    
    
def aiuto():
    print("""questi sono tutti i comandi disponibili e le loro funzionalita: 
          - aggiungi: aggiungi un prodotto al magazzino  
          - elenca: elenca i prodotto in magazzino  
          - vendita: registra una vendita effettuata  
          - profitti: mostra i profitti totali  
          - chiudi: esci dal programma""")



# variabile di controlo del ciclo while e sul quale faccio dei confronti per accedere ai vari menu
comando = ""

while comando.lower() != "chiudi":
    
    comando = input( "se non conosci i comandi inserisci 'aiuto'\nprego inserire il comando scelto: \n")

    if comando.lower() == "aggiungi":
        aggiungi()
    elif comando.lower() == "elenca":
        elenca()
    elif comando.lower() == "vendita":
        vendita()
    elif comando.lower() == "profitti":
        profitti()
    elif comando.lower() == "aiuto":
        aiuto()
    elif comando.lower() == "chiudi":
        chiudi()
    else:
        print( "comando insierito non valido")