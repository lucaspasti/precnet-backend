# PrecNet Backend Challenge

Projeto desenvolvido por **Lucas Pasti Ferreira** como parte do processo seletivo para a vaga de **Desenvolvedor Back-End (Júnior/Pleno)** na **PrecNet**.

---

## Descrição

Aplicação Flask responsável por:

- Extrair dados estruturados de documentos PDF oficiais;
- Calcular o valor líquido atualizado de requisições de pagamento;
- Aplicar o índice IPCA via API do Banco Central;
- Enviar o resultado automaticamente por e-mail ao usuário;
- Persistir os dados localmente com SQLAlchemy.

---

## Estrutura do Projeto

```
app/
├── app.py
├── database.py
├── models/
│   └── scraping_data_model.py
├── services/
│   ├── pdf_parser.py
│   ├── ipca_client.py
│   ├── calculator.py
│   └── email_sender.py
├── templates/
│   └── upload.html
└── uploads/
```

---

## Instalação e Execução

### Clonar o repositório

```bash
git clone https://github.com/lucaspasti/precnet-backend.git
cd precnet-backend
```

### 2️⃣ Criar e ativar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Criar arquivo `.env`

```bash
EMAIL_USER=seuemail@gmail.com
EMAIL_PASS=senhadeappdoGmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

> ⚠️ Use uma **senha de app** do Gmail, não a senha normal.
> Alternativamente, use credenciais SMTP de teste do [Mailtrap.io](https://mailtrap.io).

---

## ▶️ Executando o servidor

```bash
flask --app app run
```

Acesse: [http://localhost:5000](http://localhost:5000)

---

## 💡 Endpoints

| Método  | Rota                   | Descrição                                                       |
| -------- | ---------------------- | ----------------------------------------------------------------- |
| `GET`  | `/`                  | Página inicial (upload PDF + e-mail)                             |
| `POST` | `/`                  | Faz upload do PDF, calcula valores e envia e-mail automaticamente |
| `GET`  | `/debug/requisicoes` | Lista todas as requisições salvas                               |
| `GET`  | `/calcular/<id>`     | Recalcula manualmente um registro                                 |

---

## Lógica do cálculo

1. Extrai `Valor bruto` e `Data base do cálculo` do PDF;
2. Busca o índice IPCA acumulado via API BACEN:
   ```
   https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json
   ```
3. Atualiza o valor bruto até o último mês disponível;
4. Aplica desconto de **3% de IR**;
5. Retorna valor líquido atualizado.

---

## Exemplo de resposta JSON

```json
{
  "beneficiario": "Carmem Augusta Ramos Pelizon",
  "numero_oficio": "2025.07477/OFREQ",
  "valor_bruto": 629382.80,
  "fator_ipca": 1.149689,
  "valor_corrigido": 723594.21,
  "valor_liquido": 701886.38,
  "email": "usuario@exemplo.com",
  "status_email": "E-mail enviado com sucesso!"
}
```

---

## Execução com Docker

Você também pode rodar o projeto em container.

```bash
docker build -t precnet-backend .
docker run -p 5000:5000 --env-file .env precnet-backend
```

---

## Autor

**Lucas Pasti Ferreira**
lucas.pasti@gmail.com
Outubro de 2025
