Python 3.12.6 (v3.12.6:a4a2d2b0d85, Sep  6 2024, 16:08:03) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> import random
... 
... # Definizione dei prodotti che la linea di produzione gestisce
... prodotti = ['Prodotto_A', 'Prodotto_B', 'Prodotto_C']
... 
... def genera_quantita_prodotti(prodotti_list: list, min_max_quantita: dict) -> dict:
...     """
...     Genera casualmente le quantità da produrre per ogni tipologia di prodotto.
... 
...     Args:
...         prodotti_list (list): Lista dei nomi dei prodotti.
...         min_max_quantita (dict): Dizionario con gli intervalli (min, max) per le quantità di ciascun prodotto.
... 
...     Returns:
...         dict: Un dizionario dove le chiavi sono i nomi dei prodotti e i valori sono le quantità generate.
...     """
...     quantita = {}
...     for prodotto in prodotti_list:
...         if prodotto in min_max_quantita:
...             min_qta, max_qta = min_max_quantita[prodotto]
...             quantita[prodotto] = random.randint(min_qta, max_qta)
...         else:
...             # Gestione caso in cui un prodotto non abbia un range definito, assegnando un default o un errore
...             quantita[prodotto] = 0 # O sollevare un errore per coerenza
...     return quantita
... 
... def genera_parametri_produzione(prodotti_list: list, range_tempi: dict, range_capacita: dict) -> tuple:
...     """
...     Genera casualmente i parametri di configurazione del processo produttivo.
... 
...     Args:
...         prodotti_list (list): Lista dei nomi dei prodotti.
        range_tempi (dict): Dizionario con gli intervalli (min, max) per i tempi unitari (min/unità) di ciascun prodotto.
        range_capacita (dict): Dizionario con gli intervalli (min, max) per le capacità giornaliere (unità/giorno) di ciascun prodotto.

    Returns:
        tuple: Un tuple contenente:
               - dict: Tempi unitari generati per ogni prodotto.
               - dict: Capacità giornaliere generate per ogni prodotto.
               - int: Capacità totale giornaliera della linea (in minuti).
    """
    tempo_unitario = {}
    capacita_giornaliera = {}
    
    # Generazione dei tempi unitari e capacità per prodotto
    for prodotto in prodotti_list:
        if prodotto in range_tempi:
            min_t, max_t = range_tempi[prodotto]
            tempo_unitario[prodotto] = round(random.uniform(min_t, max_t), 2)
        else:
            tempo_unitario[prodotto] = 0.0 # Default o errore
        
        if prodotto in range_capacita:
            min_c, max_c = range_capacita[prodotto]
            capacita_giornaliera[prodotto] = random.randint(min_c, max_c)
        else:
            capacita_giornaliera[prodotto] = 0 # Default o errore
            
    # La capacità totale giornaliera è un parametro casuale globale per la linea
    # che rappresenta i minuti disponibili totali al giorno per la produzione complessiva.
    # Ho impostato un range realistico per i minuti disponibili in una giornata lavorativa (es. 8 ore = 480 minuti)
    # ma simuliamo una capacità "globale" che può essere superiore alla somma delle capacità specifiche
    # per riflettere un sistema con flessibilità o con più macchine non dedicate.
    capacita_totale_linea_minuti = random.randint(1000, 1500) # Minuti disponibili al giorno sulla linea

    return tempo_unitario, capacita_giornaliera, capacita_totale_linea_minuti

def simula_produzione(quantita: dict, tempo_unitario: dict, capacita_totale_giornaliera_min: int) -> tuple:
    """
    Simula il processo produttivo e calcola il tempo totale e i giorni necessari.

    Args:
        quantita (dict): Dizionario delle quantità da produrre per ogni prodotto.
        tempo_unitario (dict): Dizionario dei tempi unitari per ogni prodotto.
        capacita_totale_giornaliera_min (int): Capacità totale giornaliera della linea in minuti.

    Returns:
        tuple: Un tuple contenente:
               - float: Tempo totale di produzione dell'intero lotto in minuti.
               - int: Giorni necessari alla produzione (arrotondati per eccesso).
               - dict: Dettaglio della produzione per ciascun prodotto.
    """
    tempo_totale_lotto = 0.0
    dettagli_produzione = {}

    print("\n--- Calcolo del tempo per ciascun prodotto ---")
    for prodotto, qta in quantita.items():
        if prodotto in tempo_unitario:
            t_unit = tempo_unitario[prodotto]
            tempo_produzione_prodotto = qta * t_unit
            tempo_totale_lotto += tempo_produzione_prodotto
            dettagli_produzione[prodotto] = {
                'quantita_prodotta': qta,
                'tempo_unitario_min': t_unit,
                'tempo_totale_prodotto_min': tempo_produzione_prodotto
            }
            print(f"  {prodotto}: {qta} unità * {t_unit:.2f} min/unità = {tempo_produzione_prodotto:.2f} min")
        else:
            print(f"  Attenzione: Parametri tempo unitario mancanti per {prodotto}.")

    # Calcolo dei giorni necessari
    # Si arrotonda per eccesso: se anche una piccola frazione di giorno è necessaria, si conta come un giorno intero
    if capacita_totale_giornaliera_min > 0:
        giorni_necessari = tempo_totale_lotto / capacita_totale_giornaliera_min
        giorni_arrotondati = int(giorni_necessari)
        if giorni_necessari % 1 > 0: # Se c'è una frazione di giorno, si aggiunge un giorno intero
            giorni_arrotondati += 1
    else:
        giorni_arrotondati = float('inf') # Capacità zero, produzione infinita o impossibile
        print("Attenzione: Capacità totale giornaliera è zero. Impossibile calcolare i giorni.")

    return tempo_totale_lotto, giorni_arrotondati, dettagli_produzione

# --- Definizione dei range per la configurazione (Questi possono essere modificati per testare diversi scenari) ---
# Quantità da produrre per lotto: (min_quantità, max_quantità)
CONFIG_MIN_MAX_QUANTITA = {
    'Prodotto_A': (50, 200),
    'Prodotto_B': (30, 150),
    'Prodotto_C': (20, 100)
}

# Tempi di produzione unitari (minuti/unità): (min_tempo, max_tempo)
CONFIG_RANGE_TEMPI_UNITARI = {
    'Prodotto_A': (0.5, 1.5),   # Esempio: Giunto Omocinetico, veloce
    'Prodotto_B': (1.0, 2.0),   # Esempio: Supporto Motore, medio
    'Prodotto_C': (2.0, 3.0)    # Esempio: Albero di Trasmissione, lento e preciso
}

# Capacità massima giornaliera di produzione per prodotto (unità/giorno)
# Nota: questa capacità è "virtuale" e potrebbe non essere direttamente usata nel calcolo giorni se c'è
# una capacita_totale_giornaliera globale, ma serve per definire la "velocità massima" di ogni specifica lavorazione.
CONFIG_RANGE_CAPACITA_GIORNALIERA_PRODOTTO = {
    'Prodotto_A': (400, 600),
    'Prodotto_B': (300, 500),
    'Prodotto_C': (200, 400)
}

# --- Esecuzione della Simulazione ---
if __name__ == "__main__":
    print("=== Avvio Simulazione Processo Produttivo ===")

    # 1. Generazione delle quantità da produrre per il lotto
    quantita_da_produrre = genera_quantita_prodotti(prodotti, CONFIG_MIN_MAX_QUANTITA)
    print(f"\n1. Quantità generate per il lotto: {quantita_da_produrre}")

    # 2. Generazione dei parametri di produzione (tempi unitari, capacità per prodotto, capacità totale linea)
    tempi_unitari_generati, capacita_giornaliera_prodotto_generata, capacita_totale_linea_minuti_generata = \
        genera_parametri_produzione(prodotti, CONFIG_RANGE_TEMPI_UNITARI, CONFIG_RANGE_CAPACITA_GIORNALIERA_PRODOTTO)
    
    print(f"\n2. Parametri di produzione generati:")
    print(f"   Tempi unitari (min/unità): {tempi_unitari_generati}")
    print(f"   Capacità giornaliera per tipo di prodotto (unità): {capacita_giornaliera_prodotto_generata}")
    print(f"   Capacità totale giornaliera della linea (minuti): {capacita_totale_linea_minuti_generata}")

    # 3. Simulazione del processo e calcolo degli output
    tempo_totale_finale, giorni_necessari_finale, dettagli_prod = \
        simula_produzione(quantita_da_produrre, tempi_unitari_generati, capacita_totale_linea_minuti_generata)

    # 4. Output dei risultati finali
    print("\n--- Risultati Complessivi della Simulazione ---")
    print(f"Tempo totale di produzione dell'intero lotto: {tempo_totale_finale:.2f} minuti")
    print(f"Giorni necessari per completare la produzione: {giorni_necessari_finale} giorni")
    print("\n=== Simulazione Completata ===")
