La bozza è in `docs/methodology.md`, pronta da modificare. Il ticket 11.2 resta **needs-info**: secondo il ticket stesso e TRAINER.md, la metodologia la scrivi tu. Per questo ogni numero è segnato come proposta. Non ho fatto commit e non ho toccato codice né il brief del planner.

**Cosa contiene** (sette sezioni brevi, quasi solo tabelle):
1. **Serie allenante**: a 1-3 ripetizioni dal cedimento. Range predefinito 6-15. Se un esercizio regge più di 30 ripetizioni si passa a una variante più difficile, non si aggiungono ripetizioni.
2. **Quanto volume**:
   - 3-4 serie per esercizio;
   - 6-10 serie per muscolo nel singolo allenamento, 10-20 nel ciclo;
   - 1-3 esercizi per gruppo, a seconda di quanti gruppi allena l'allenamento;
   - 4-7 esercizi in tutto.
3. **Scelta degli esercizi**: prima si coprono i pattern, poi le varianti. Due varianti dello stesso esercizio contano come uno. I multiarticolari vengono prima dei monoarticolari.
4. **Recupero per obiettivo**: il recupero breve non serve a far stare il piano nel tempo.
5. **Struttura dei blocchi**: le serie singole sono la norma. Il superset va solo tra esercizi che non hanno muscoli primari in comune. Il circuito, da 3-4 esercizi, va solo in un allenamento ridotto o come finisher.
6. **Riempire il tempo**: si aggiungono serie, non esercizi. Ho messo un ordine esplicito per quando il piano è sotto il tempo e uno per quando è sopra.
7. **Mesociclo**: 4-6 cicli.

C'è anche un esempio costruito sullo stesso caso del ticket, cioè petto e braccia in 45 minuti con corpo libero ed elastici, e sette fonti in bibliografia. **Le fonti le ho citate a memoria e non le ho verificate** sugli articoli: vanno controllate prima di tenerle.

**Due cose che ho scoperto scrivendo l'esempio:**
- **La soglia del ticket 11.3 entra in conflitto con il tetto di volume.** Seguendo la bozza, quel piano arriva al tetto di serie per muscolo a circa 34 minuti, sotto la soglia di 40 che introduce 11.3. Così com'è scritta, la 11.3 lo rifiuterebbe. L'ho annotato anche nel ticket 03.
- **Nel catalogo non c'è nessun esercizio per i bicipiti a corpo libero o con elastici**, solo uno stretching. Con quell'attrezzatura, "braccia" vuol dire solo tricipiti.

**Le cinque domande aperte**, in fondo al documento, sono l'input che manca per scrivere la spec:
1. Quando si raggiunge il tetto prima della soglia, cosa cede?
2. Finché l'onboarding non sceglie un obiettivo, il default è ipertrofia o forza?
3. Il margine dal cedimento (RIR) va scritto nel `reason` del blocco, o aspetta un campo apposito?
4. Vuoi mai un circuito al di fuori di un allenamento ridotto?
5. Un muscolo che l'attrezzatura non raggiunge si lascia scoperto dicendolo, o lo si lavora come secondario?

Ho aggiunto una nota al ticket 02 e una al 03. Una volta sistemata la metodologia, nella spec restano da decidere due cose:
- come `PLANNING` e `MESOCYCLE_PLANNING` la riportano al modello;
- come si misura, perché i sei invarianti attuali controllano solo che il piano sia valido, non che sia buono.