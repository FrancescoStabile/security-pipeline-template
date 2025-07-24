# 🛡️ DevSecOps Security Pipeline Template

> Una pipeline di sicurezza completa e **gratuita** per progetti JavaScript/TypeScript che utilizza solo tool open source senza richiedere licenze esterne.

## 📋 Obiettivi del Repository

Questo template dimostra l'implementazione di:
- **Security automation** nel CI/CD utilizzando solo tool gratuiti
- **Multi-layered security approach** con GitHub Actions
- **Best practices** per development sicuro
- **Beginner-friendly** setup per la prima pipeline DevSecOps

## ✅ Tool di Sicurezza Utilizzati (100% Gratuiti)

### 🔍 Static Analysis Security Testing (SAST)
- **CodeQL** - Analisi statica del codice (gratuito per repo pubblici)
- **ESLint Security Plugin** - Regole di sicurezza per JavaScript/TypeScript

### 📦 Software Composition Analysis (SCA)
- **npm audit** - Scanner integrato per vulnerabilità nelle dipendenze
- **OSV Scanner** - Scanner gratuito di Google per vulnerabilità open source

### 🔐 Secrets Detection
- **TruffleHog OSS** - Rilevamento di credenziali e segreti nel codice

### 🐳 Container Security
- **Trivy** - Scanner gratuito per vulnerabilità nei container
- **Hadolint** - Linter per Dockerfile

### 🤖 Automation
- **Dependabot** - Aggiornamenti automatici delle dipendenze
- **GitHub Security Advisories** - Integrazione nativa con GitHub

## 🏗️ Struttura del Repository

```
security-pipeline-template/
├── .github/
│   ├── workflows/
│   │   └── security-scan.yml           # Pipeline principale
│   ├── ISSUE_TEMPLATE/
│   │   └── security-vulnerability.md   # Template per security issues
│   └── dependabot.yml                  # Configurazione Dependabot
├── security/
│   └── scripts/
│       └── generate-report.py          # Generatore report semplificato
├── examples/
│   └── nodejs-basic/                   # Esempio di progetto Node.js
│       ├── package.json
│       ├── index.js
│       └── .eslintrc.security.js
├── Dockerfile                          # Esempio per container scanning
├── SECURITY.md                         # Policy di sicurezza
└── README.md                          # Documentazione principale
```

## 🚀 Quick Start

### 1. Clona il Repository
```bash
git clone https://github.com/FrancescoStabile/security-pipeline-template.git
cd security-pipeline-template
```

### 2. Testa la Pipeline (Opzionale)
```bash
# Copia l'esempio Node.js nella root per testare
cp -r examples/nodejs-basic/* .

# Installa le dipendenze
npm install

# Esegui un test locale di sicurezza
npm run lint:security
```

### 3. Personalizza per il Tuo Progetto
1. Modifica `.github/workflows/security-scan.yml` secondo le tue esigenze
2. Aggiorna `.github/dependabot.yml` con il tuo username GitHub
3. Personalizza `SECURITY.md` con i tuoi contatti
4. Rimuovi la cartella `examples/` se non necessaria

### 4. Commit e Push
```bash
git add .
git commit -m "feat: initial security pipeline setup"
git push origin main
```

La pipeline si attiverà automaticamente sui push e pull request!

## 📊 Come Funziona la Pipeline

### Stage 1: Static Analysis (SAST) 🔍
- **CodeQL**: Analizza il codice per vulnerabilità di sicurezza
- **ESLint Security**: Verifica regole di sicurezza specifiche per JavaScript/TypeScript

### Stage 2: Dependency Analysis (SCA) 📦
- **npm audit**: Controlla vulnerabilità note nelle dipendenze
- **OSV Scanner**: Scanner aggiuntivo per vulnerabilità open source

### Stage 3: Secrets Detection 🔐
- **TruffleHog**: Rileva credenziali, API keys e altri segreti nel codice

### Stage 4: Container Security 🐳
- **Trivy**: Scansiona immagini Docker per vulnerabilità
- **Hadolint**: Verifica best practice nei Dockerfile

### Stage 5: Report Generation 📊
- Aggrega tutti i risultati in report HTML e JSON
- Carica risultati SARIF nella GitHub Security tab
- Commenta automaticamente le PR con un riassunto dei risultati

## 🔧 Configurazione Avanzata

### Personalizzare ESLint Security Rules
Modifica `examples/nodejs-basic/.eslintrc.security.js`:

```javascript
module.exports = {
  // ... configurazione base
  rules: {
    // Aggiungi le tue regole personalizzate
    'security/detect-sql-injection': 'error',
    'your-custom-rule': 'warn'
  }
};
```

### Escludere File dalla Scansione
Crea un `.gitignore` nella root o modifica la pipeline per escludere cartelle:

```yaml
# In security-scan.yml, aggiungi --ignore-pattern
npx eslint . --ignore-pattern "node_modules/" --ignore-pattern "dist/"
```

### Configurare Soglie di Severità
Modifica `security/scripts/generate-report.py` per personalizzare il calcolo del security score:

```python
# Modifica i pesi delle penalità
penalties = {
    'critical': 25,  # Era 20
    'high': 15,      # Era 10
    'medium': 5,     # Invariato
    'low': 1         # Invariato
}
```

## 📈 Interpretare i Risultati

### Security Score
- **90-100**: Eccellente ✨
- **80-89**: Buono ✅
- **70-79**: Discreto ⚠️
- **60-69**: Miglioramento necessario 🔧
- **<60**: Attenzione urgente richiesta 🚨

### Tipi di Vulnerabilità

| Tipo | Descrizione | Esempio |
|------|-------------|---------|
| **SAST** | Problemi nel codice sorgente | SQL injection, XSS |
| **SCA** | Vulnerabilità nelle dipendenze | Librerie obsolete |
| **Secrets** | Credenziali esposte | API keys nel codice |
| **Container** | Problemi nei container | Immagini vulnerabili |

## 🛡️ Best Practices Implementate

### ✅ Cosa Fa Questa Pipeline
- 🔄 **Scansioni automatiche** su ogni commit e PR
- 📊 **Report dettagliati** con visualizzazione HTML
- 🔔 **Notifiche** automatiche su PR
- 📈 **Tracking** delle metriche di sicurezza nel tempo
- 🤖 **Aggiornamenti** automatici delle dipendenze
- 🔐 **Integrazione** con GitHub Security tab

### 🎯 Benefici
- **Zero configurazione** di tool esterni
- **Nessun costo** aggiuntivo
- **Facile da mantenere** e aggiornare
- **Ideale per beginners** nel DevSecOps
- **Scalabile** per progetti di ogni dimensione

## 🚫 Tool Rimossi (Richiedevano Licenze Esterne)

Per mantenere questa pipeline 100% gratuita, abbiamo rimosso:
- ❌ **Semgrep** (richiede SEMGREP_APP_TOKEN)
- ❌ **Snyk** (richiede SNYK_TOKEN) 
- ❌ **GitLeaks** (richiede GITLEAKS_LICENSE)
- ❌ **SonarQube** (servizio a pagamento)

## 📖 Guide e Risorse

### 📚 Documentazione
- 📋 [SECURITY.md](SECURITY.md) - Policy di sicurezza e reporting
- 🐛 [Security Issue Template](.github/ISSUE_TEMPLATE/security-vulnerability.md) - Come segnalare vulnerabilità
- 🤖 [Dependabot Config](.github/dependabot.yml) - Aggiornamenti automatici
- 🔍 [Pipeline Workflow](.github/workflows/security-scan.yml) - Configurazione completa

### 🛠️ Setup per Sviluppatori
1. **Pre-commit hooks** (opzionale):
   ```bash
   # Installa pre-commit
   pip install pre-commit
   
   # Abilita hooks per security linting
   pre-commit install
   ```

2. **Test locale della sicurezza**:
   ```bash
   # Esegui ESLint security check
   npm run lint:security
   
   # Test con TruffleHog (richiede Docker)
   docker run --rm -v "$(pwd):/pwd" trufflesecurity/trufflehog:latest filesystem /pwd
   ```

3. **Monitoraggio continuo**:
   - Abilita GitHub Security Advisories
   - Configura notifiche per Dependabot
   - Rivedi regolarmente i report di sicurezza

## 🔄 Aggiornamenti e Manutenzione

### Aggiornare la Pipeline
```bash
# Scarica gli ultimi aggiornamenti del template
git remote add upstream https://github.com/FrancescoStabile/security-pipeline-template.git
git fetch upstream
git merge upstream/main
```

### Monitorare le Prestazioni
- Controlla i tempi di esecuzione delle GitHub Actions
- Rivedi periodicamente i falsi positivi
- Aggiorna le regole di sicurezza secondo le best practice

## 🤝 Contribuire

Contributi benvenuti! Per migliorare questa pipeline:

1. **Fork** il repository
2. **Crea** un branch per la tua feature (`git checkout -b feature/amazing-security-improvement`)
3. **Testa** le modifiche con progetti reali
4. **Commit** le modifiche (`git commit -m 'Add amazing security feature'`)
5. **Push** al branch (`git push origin feature/amazing-security-improvement`)
6. **Apri** una Pull Request

### Aree di Miglioramento
- 🎯 **Nuovi scanner gratuiti** da integrare
- 📊 **Miglioramenti al report HTML** 
- 🔧 **Ottimizzazioni delle prestazioni**
- 📚 **Documentazione aggiuntiva**
- 🐛 **Fix di bug** e edge cases

## 📞 Supporto

- 🐛 **Bug e problemi**: Apri un [GitHub Issue](../../issues)
- 💡 **Feature request**: Usa il nostro [Issue Template](../../issues/new)
- 🔒 **Vulnerabilità di sicurezza**: Segui le istruzioni in [SECURITY.md](SECURITY.md)

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🙏 Ringraziamenti

- **GitHub** per CodeQL e GitHub Actions gratuite
- **Google** per OSV Scanner
- **TruffleHog** per la versione open source
- **Aqua Security** per Trivy
- **Hadolint** team per il Dockerfile linter
- La **community DevSecOps** per le best practices

---

⭐ **Se questo template ti è stato utile, considera di mettere una stella al repository!**

💡 **Suggerimento**: Inizia con questa pipeline base e personalizzala gradualmente secondo le esigenze del tuo progetto.