# 🛡️ Security Pipeline Template

Template minimale per integrare controlli di sicurezza in un progetto JS/TS senza tool a pagamento.

## Perché esiste
Mi serviva una base veloce: un solo workflow YAML che faccia analisi del codice, dipendenze, secrets e (se c'è) Docker image, tutto con tool open source.

## Cosa c'è dentro
SAST: CodeQL, ESLint con regole di sicurezza
SCA: npm audit, OSV Scanner
Secrets: TruffleHog
Container: Trivy, Hadolint
Report: script Python che aggrega e produce JSON/SARIF + commento in PR
Automazione: Dependabot (se configurato) + GitHub Security tab

## Struttura rapida
```
.github/workflows/security-scan.yml   # Pipeline
security/scripts/generate-report.py   # Merge dei risultati
examples/nodejs-basic/                # Esempio (rimuovibile)
Dockerfile                            # Per test container
```

## Provalo al volo
```bash
git clone https://github.com/FrancescoStabile/security-pipeline-template.git
cd security-pipeline-template
cp -r examples/nodejs-basic/* .   # opzionale
npm install
npx eslint . || true
```
Fai un commit e push: la workflow parte da sola.

## Personalizzazione minima
1. Modifica `.github/workflows/security-scan.yml` (puoi togliere parti che non usi)
2. Elimina `examples/` se non serve
3. Adatta `SECURITY.md` (contatti, disclosure)
4. Aggiungi eventuali regole custom ESLint

## Output
Artefatti caricati come zip: risultati singoli + `final-report/` con sommario, SARIF (se generato) e punteggio semplice.
Se è una PR: commento con tabella riassuntiva.

## Note pratiche
- CodeQL gira solo su repo pubblici senza configurazioni extra
- Se vuoi velocizzare rimuovi temporaneamente CodeQL nel matrix
- Trivy e OSV possono rallentare se la cache delle dipendenze è vuota

## Dipendenze principali
Node 18, Python 3.11, Docker (solo per lo stage container), nessun token necessario.

## Contribuire
Fork, branch, modifica, PR. Keep it pragmatic: niente feature gonfie se non servono.

## Licenza
MIT. Usa e adatta liberamente.

Se ti è utile: ⭐

Fine.