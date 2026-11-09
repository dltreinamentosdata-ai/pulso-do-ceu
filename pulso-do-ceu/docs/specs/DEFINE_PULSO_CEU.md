# DEFINE: Pulso do Céu

> Produto de dados unificado sobre alertas astronômicos transientes do NASA GCN: ingestão em tempo real de múltiplos tópicos Kafka, histórico bruto, visão unificada de eventos, visão das Circulars, quarentena, controle de acesso com máscara de PII, métricas 1–6, Genie Space e dashboard.

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | PULSO_CEU |
| **Tamanho** | Complexo — ingestão multi-formato em tempo real (JSON Unified, JSON LVK, VOEvent XML, Circulars), múltiplas camadas de saída, restrição OAuth na plataforma, controle de acesso com PII e ADR necessário |
| **Jira** | pendente |
| **Data** | 2026-11-09 |
| **Status** | Rascunho |

---

## Fontes

| Fonte | Link | O que foi usado |
|-------|------|-----------------|
| Confluence: Upstream — Pulso do Céu v5 | https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/360450 | Seções 1–12 e Anexo A |
| Confluence: Downstream — Pulso do Céu v2 | https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/557058 | Seções 1–9 (mapeamento decidido; aprovado pelo engenheiro em Q1.1) |

---

## Registro do pedido e das respostas

### Pedido original

> "Especifique o Pulso do Céu. Projeto: /Workspace/Users/dltreinamentos.data@gmail.com/projetos/pulso-do-ceu. Upstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/360450. Downstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/557058."

### Rodada 1

| ID | Pergunta, com a recomendação | Resposta do usuário |
|----|------------------------------|---------------------|
| Q1.1 | O documento Downstream v2 está com aprovação pendente pelo engenheiro responsável. Como engenheiro responsável, você aprova a v2 do Downstream para servir de base ao Define? Caso discorde de alguma decisão de mapeamento da seção 5, liste os pontos. (Recomendo: aprovar v2 integralmente, para desbloqueio do Define.) | "sim, aprovo o downstream v2 como está" |
| Q1.2 | O escopo desta spec deve ser P1 (histórico bruto, visão unificada, Circulars, quarentena, grupos de acesso e máscara, métricas 1–4 e dashboard) ou P1 + P2 (acrescenta Genie Space e métricas 5–6)? (Recomendo: somente P1, com P2 como feature separada.) | "P1+P2, a prioridade de cada requisito segue o upstream item 6" |
| Q1.3 | Há chave de Jira para este épico ou feature (ex.: PDC-1)? | "pendente" |
| Q1.4 | O nome da feature para os artefatos (arquivo DEFINE, branch e state) deve ser `PULSO_CEU` ou `PULSO_CEU_P1`? (Recomendo: `PULSO_CEU_P1` se o escopo for só P1; `PULSO_CEU` se cobrir o produto completo.) | "PULSO_CEU" |

---

## Problema

Quem acompanha o céu transiente precisa consultar dezenas de tópicos Kafka do GCN, cada um num formato diferente, para saber o que acontece. Não existe visão unificada de "o que está acontecendo no céu agora", nem de quais eventos foram vistos por mais de um instrumento, nem sinal claro de quais missões pararam de transmitir. (Fonte: Upstream §1)

## Quem usa o dado

| Quem | Para quê | Dor hoje |
|------|----------|----------|
| Astrônomo de plantão (follow-up) | Decidir se aponta um telescópio para um evento | Precisa abrir vários tópicos e converter formatos na mão |
| Coordenação científica | Acompanhar a rede de observatórios | Não sabe o volume, a latência nem quais missões estão ativas |
| Divulgação científica | Contar os eventos notáveis da semana | Não sabe o que a comunidade está comentando |
| Engenharia de dados (operação) | Manter o produto de pé | Não tem sinal de saúde do stream |

(Fonte: Upstream §2)

---

## Escopo

### Dentro do escopo

**P1 — primeira entrega**

- Ingestão contínua de todos os tópicos do Anexo A
- Histórico bruto: toda mensagem dos tópicos do Anexo A, menos o heartbeat, guardada como chegou
- Heartbeat (`gcn.heartbeat`) guardado à parte, para operação
- Visão unificada de eventos: modelo comum para notices de todas as missões e formatos (Downstream §5.2)
- Visão das Circulars: versão válida de cada Circular, unindo arquivo histórico e Kafka (Downstream §5.4)
- Quarentena: guarda mensagens não parseáveis com motivo, por 90 dias (Downstream §5.6)
- Controle de acesso: grupos `pulso-ceu-consumidores`, `pulso-ceu-engenharia` e `pulso-ceu-admins` (Upstream §5)
- Máscara do email das Circulars para não-admins (Upstream §4)
- Métricas 1–4: alertas por missão, latência, saúde das missões, ciclo de vida do evento (Upstream §6)
- Dashboard cobrindo as métricas 1–4 (Upstream §6)
- Alertas de teste guardados, marcados e excluídos das métricas de negócio (Upstream §7)

**P2 — segunda entrega**

- Métrica 5: coincidências multimensageiro — eventos de missões diferentes próximos no tempo e no céu (Upstream §6)
- Métrica 6: resposta da comunidade — Circulars por evento e tempo até a primeira Circular (Upstream §6)
- Genie Space em cima das métricas 1–6 (Upstream §6)

### Fora do escopo

- Arquitetura de ingestão (escolha entre opções A, B1, B2, C do Downstream §7) — decisão do ADR
- Leitura de sondagem do Kafka — pré-Build (Downstream §8)
- Lista de sinônimos do GCN (`/api/synonym/circulars`) — Downstream §5.5
- Mapas do céu (`event.skymap`, `combined_skymap`, `healpix_file`) na visão unificada — ficam só no histórico bruto
- BOOM na visão unificada — só no histórico bruto (Upstream §12, Downstream tabela 5.1)
- Classic do IceCube (ASTROTRACK GOLD/BRONZE) e MAXI Classic na visão unificada — mesmos eventos chegam em JSON (Downstream §5.3 regra 2)
- Tipos SVOM `eclairs-catalog`, `slewing` e `not-slewing` na visão unificada — só no histórico bruto

---

## Requisitos

### R1: Ingestão contínua do GCN — P1

**Por quê:** o histórico bruto é a única cópia do passado; o Kafka do GCN não guarda o histórico para sempre. (Upstream §6)

**Critérios de aceite (EARS):**

- **R1.1** QUANDO uma mensagem chegar num tópico do Anexo A ENTÃO o pipeline DEVE gravá-la no histórico bruto com tópico, partição, offset e horário do Kafka, sem modificação.
- **R1.2** ENQUANTO o produto estiver ligado, o pipeline DEVE guardar toda mensagem do `gcn.heartbeat` à parte, fora do histórico bruto de notices.
- **R1.3** O pipeline DEVE ignorar tópicos com `.test.` no nome e tipos Classic terminados em `_TEST` ou `TEST_COORDS`.
- **R1.4** SE o produto parar por falha ENTÃO, ao voltar, DEVE continuar exatamente de onde parou, sem reprocessar mensagens já guardadas.
- **R1.5** QUANDO o produto ligar ENTÃO DEVE baixar o arquivo histórico de Circulars (`archive.json.tar.gz`) e guardá-lo com o horário do download.
- **R1.6** O pipeline DEVE usar a credencial do GCN (client ID e client secret) armazenada em secret scope; nunca exposta no código.
- **R1.7** ENQUANTO o produto estiver ligado, SE o heartbeat ficar mais de 5 minutos sem chegar ENTÃO o time de engenharia DEVE receber aviso por email no endereço configurável.

### R2: Visão unificada de eventos — P1

**Por quê:** a visão unificada é a entrega central para os astrônomos de plantão e para as métricas operacionais.

**Critérios de aceite (EARS):**

- **R2.1** ENQUANTO o produto estiver ligado, QUANDO um alerta chegar ao Kafka do GCN ENTÃO a visão unificada de eventos DEVE refleti-lo em até 5 minutos a partir do horário de chegada.
- **R2.2** O pipeline DEVE mapear cada notice ao modelo comum de acordo com o mapeamento da seção 5.2 do Downstream (aprovado em Q1.1).
- **R2.3** QUANDO uma mensagem não puder ser lida no formato esperado OU a coordenada estiver fora da faixa (RA fora de 0–360 ou Dec fora de −90 a 90) ENTÃO o pipeline DEVE gravá-la na quarentena com motivo, sem interromper o processamento.
- **R2.4** O pipeline DEVE marcar todo alerta de teste como `is_test = true` e excluí-lo das métricas de negócio.
- **R2.5** A mesma mensagem recebida duas vezes DEVE aparecer uma única vez na visão unificada.
- **R2.6** QUANDO o GCN acrescentar um campo novo num schema ENTÃO o produto NÃO DEVE parar; o campo novo DEVE ficar preservado no histórico bruto.
- **R2.7** QUANDO a missão retratar um evento ENTÃO a visão unificada DEVE mantê-lo marcado como `is_retraction = true`, fora das contagens de eventos.
- **R2.8** QUANDO a LIGO/Virgo/KAGRA, o IceCube (ASTROTRACK) ou o MAXI enviarem um alerta em dois formatos (JSON + Classic) para o mesmo evento ENTÃO o pipeline DEVE alimentar a visão unificada pelo formato JSON e guardar o Classic só no histórico bruto.
- **R2.9** Um tópico do Anexo A indisponível no GCN NÃO DEVE parar o produto.
- **R2.10** Reprocessar a visão unificada de eventos a partir do histórico bruto NÃO DEVE duplicar nenhuma linha.
- **R2.11** Reprocessar NÃO DEVE apagar nenhuma linha do histórico bruto.

### R3: Visão das Circulars — P1

**Por quê:** as Circulars são o canal de comunicação científica associado aos eventos; precisam de deduplicação por versão e de junção com o arquivo histórico.

**Critérios de aceite (EARS):**

- **R3.1** A carga histórica DEVE trazer todas as Circulars do arquivo histórico do GCN.
- **R3.2** QUANDO a mesma Circular estiver no arquivo histórico e também chegar pelo Kafka ENTÃO DEVE aparecer uma única vez na visão das Circulars.
- **R3.3** QUANDO o GCN publicar uma nova versão de uma Circular ENTÃO a visão das Circulars DEVE refletir a versão de maior `version`; no empate, a última recebida.
- **R3.4** O pipeline DEVE mapear as colunas da visão das Circulars conforme a seção 5.4 do Downstream (aprovado em Q1.1).
- **R3.5** Reprocessar a visão das Circulars a partir do histórico bruto NÃO DEVE duplicar nenhuma linha.

### R4: Controle de acesso e máscara de PII — P1

**Por quê:** as Circulars contêm emails de astrônomos (dado pessoal); a política do produto exige visibilidade restrita por grupo. (Upstream §4–5)

**Critérios de aceite (EARS):**

- **R4.1** O email das Circulars (`submitter_email`, `edited_by_email`) DEVE aparecer mascarado para os grupos `pulso-ceu-consumidores` e `pulso-ceu-engenharia`.
- **R4.2** Somente o grupo `pulso-ceu-admins` DEVE ver o email sem máscara.
- **R4.3** A máscara DEVE valer em todo lugar onde o email aparece, inclusive no histórico bruto e na quarentena.
- **R4.4** Fora dos grupos `pulso-ceu-engenharia` e `pulso-ceu-admins`, nenhum usuário DEVE ver o histórico bruto.
- **R4.5** O produto DEVE criar os grupos `pulso-ceu-consumidores`, `pulso-ceu-engenharia` e `pulso-ceu-admins` como grupos do Unity Catalog, com os acessos da tabela do Upstream §5.

### R5: Métricas e dashboard — P1

**Por quê:** os indicadores de saúde e operação são a superfície de consumo principal para coordenação científica e engenharia.

**Critérios de aceite (EARS):**

- **R5.1** O dashboard DEVE exibir alertas por dia, missão, instrumento e mensageiro.
- **R5.2** O dashboard DEVE exibir a latência por missão (tempo do disparo ao alerta e do alerta ao Kafka), com mediana e p95.
- **R5.3** O dashboard DEVE exibir a situação de cada missão (ativa, em silêncio, encerrada) e o último alerta.
- **R5.4** O dashboard DEVE exibir o ciclo de vida do evento: quantos alertas cada evento teve e quais foram retratados.
- **R5.5** O dashboard DEVE mostrar o horário da última mensagem recebida.
- **R5.6** O dashboard DEVE deixar o usuário mudar o limite de boa localização (padrão: erro ≤ 1 grau).
- **R5.7** Para cada pergunta de referência da seção 10 do Upstream, a resposta do dashboard DEVE bater com a consulta direta nas métricas.
- **R5.8** Alertas de teste NÃO DEVEM entrar nas métricas de negócio; a operação DEVE ver a contagem de alertas de teste por missão numa métrica própria.

### R6: Coincidências multimensageiro — P2

**Por quê:** a detecção de eventos simultâneos de múltiplos mensageiros é o principal sinal de astrofísica multimessenger. (Upstream §6)

**Critérios de aceite (EARS):**

- **R6.1** QUANDO dois eventos de missões diferentes tiverem horários de disparo a até 500 segundos um do outro E a distância angular entre eles for menor que a soma dos erros de localização ENTÃO a métrica DEVE registrá-los como coincidência multimensageiro.
- **R6.2** QUANDO um dos eventos não tiver posição ou não tiver erro de localização ENTÃO a coincidência DEVE ser avaliada só pelo tempo e marcada como temporal.
- **R6.3** SE um evento não tiver horário de disparo, ou for retratado, ou for de teste ENTÃO DEVE ser excluído do cálculo de coincidências.

### R7: Resposta da comunidade — P2

**Por quê:** o volume de Circulars e o tempo até a primeira Circular medem o engajamento científico com cada evento. (Upstream §6)

**Critérios de aceite (EARS):**

- **R7.1** A métrica DEVE contar as Circulars por evento pelo `event_id` da Circular, sem exigir ligação a uma notice.
- **R7.2** A métrica DEVE calcular o tempo até a primeira Circular para eventos da LIGO/Virgo/KAGRA e do IceCube, medido do horário do disparo do evento até o `created_on` da primeira Circular com o `event_id` correspondente.

### R8: Genie Space — P2

**Por quê:** o Genie Space torna as métricas 1–6 consultáveis em linguagem natural para usuários sem SQL. (Upstream §6)

**Critérios de aceite (EARS):**

- **R8.1** O Genie Space DEVE responder perguntas em linguagem natural sobre as métricas 1–6.
- **R8.2** Para cada pergunta de referência da seção 10 do Upstream, a resposta do Genie DEVE bater com a consulta direta nas métricas.
- **R8.3** O Genie Space DEVE ser acessível ao grupo `pulso-ceu-consumidores`.

---

## Requisitos implícitos de dados

| Dimensão | Como fica nesta feature |
|----------|-------------------------|
| Idempotência e reprocessamento | R2.10, R2.11, R3.5: reprocessar a partir do histórico bruto não duplica nem apaga |
| Dado atrasado ou fora de ordem | S-1 (Downstream §5.3 regra 4): estado do evento vem do alerta de maior `alert_time`; empate por `kafka_time`, depois por partição e offset |
| Duplicidade | Chave do evento = `event_uid` (Downstream §5.3 regra 1); R2.5: mesma mensagem recebida duas vezes aparece uma vez só; chave da Circular = `circular_id` + maior `version` |
| Evolução de schema | R2.6: campo novo fica no histórico bruto e não para o produto |
| Backfill e carga histórica | R3.1: arquivo histórico das Circulars baixado ao ligar; Kafka sem retenção garantida — histórico bruto é a única cópia |
| Qualidade (nulos, chaves, faixas de valor) | R2.3: coordenada fora da faixa → quarentena; valor fora da faixa em `error_deg`, `far` ou `p_astro` → nulo na coluna, mensagem segue (Downstream §5.3 regra 11) |
| Falha parcial e retomada | R1.4: ao voltar de uma falha, continua de onde parou |
| PII, grants e Unity Catalog | R4.1, R4.2, R4.3, R4.4, R4.5: grupos de acesso e máscara do email; Unity Catalog requerido |
| Freshness e SLA | R2.1: alerta na visão unificada em até 5 minutos da chegada ao Kafka do GCN |
| Volume, custo e compute | não se aplica a critérios nesta fase: volume baixo (~centenas de notices/dia, ~8 Circulars/dia, ~86.400 heartbeats/dia); compute e trigger são decisões do ADR |
| Observabilidade e alerta | R1.7: alerta de email se heartbeat parar >5 min; R5.5: dashboard mostra horário da última mensagem |

---

## Contrato de dados

### Fontes de dados

| Fonte | Tipo | Volume | Freshness | Dono |
|-------|------|--------|-----------|------|
| GCN Kafka — notices (Anexo A) | Kafka (SASL_SSL, OAUTHBEARER) | ~centenas/dia | tempo real | NASA GCN |
| GCN Kafka — heartbeat (`gcn.heartbeat`) | Kafka | ~86.400/dia | tempo real | NASA GCN |
| GCN Kafka — Circulars (`gcn.circulars`) | Kafka | ~8/dia | tempo real | NASA GCN |
| Arquivo histórico de Circulars (`archive.json.tar.gz`) | HTTP → S3 (1x ao ligar) | ~46.000 registros | 1x/dia | NASA GCN |

### Schema de saída — Visão unificada de eventos

| Coluna | Tipo | Regra | PII? |
|--------|------|-------|------|
| `event_uid` | STRING | não nulo | não |
| `source_topic` | STRING | não nulo | não |
| `source_partition` | INT | não nulo | não |
| `source_offset` | BIGINT | não nulo | não |
| `source_format` | STRING | `json` ou `voevent` | não |
| `mission` | STRING | não nulo (tabela 5.1 do Downstream) | não |
| `instrument` | STRING | nulo quando não se aplica | não |
| `messenger` | STRING | `EM`, `GW` ou `Neutrino` | não |
| `alert_type` | STRING | valor como a missão manda; nulo quando ausente | não |
| `is_retraction` | BOOLEAN | não nulo | não |
| `is_test` | BOOLEAN | não nulo | não |
| `is_archival` | BOOLEAN | não nulo | não |
| `event_name` | STRING | nulo quando a missão não manda | não |
| `trigger_time` | TIMESTAMP | nulo quando a missão não informa | não |
| `alert_time` | TIMESTAMP | nulo quando a missão não informa | não |
| `kafka_time` | TIMESTAMP | não nulo | não |
| `ra` | DOUBLE | 0–360 graus; nulo quando não manda posição | não |
| `dec` | DOUBLE | −90 a 90 graus; nulo quando não manda posição | não |
| `error_deg` | DOUBLE | >0; nulo quando ausente ou fora da faixa | não |
| `far` | DOUBLE | ≥0 Hz; nulo quando ausente ou fora da faixa | não |
| `p_astro` | DOUBLE | 0–1; nulo quando ausente ou fora da faixa | não |

### Schema de saída — Visão das Circulars

| Coluna | Tipo | Regra | PII? |
|--------|------|-------|------|
| `circular_id` | BIGINT | chave, não nulo | não |
| `version` | INT | vale a maior; empate: a última recebida | não |
| `event_id` | STRING | nome do evento dado pelo GCN | não |
| `subject` | STRING | não nulo | não |
| `body` | STRING | não nulo | não |
| `created_on` | TIMESTAMP | não nulo | não |
| `submitter_name` | STRING | pode ser nulo | sim (autoria pública, visível) |
| `submitter_affiliation` | STRING | pode ser nulo | não |
| `submitter_email` | STRING | mascarado para não-admins | **sim** |
| `edited_by_email` | STRING | mascarado para não-admins | **sim** |

---

## Contexto técnico

| Aspecto | Valor |
|---------|-------|
| **Onde fica no projeto** | `pulso-do-ceu/pulso-do-ceu/` (bundle raiz) |
| **Skills Databricks** | A definir no ADR (`@sdd-staff-engineer`) |
| **Infraestrutura nova** | Credencial GCN em secret scope; grupos Unity Catalog; recursos no bundle (job ou pipeline, warehouse, dashboard, Genie Space) |
| **Trigger** | Ingestão deve ser contínua — o GCN proíbe cron e cliente curto repetido (Upstream §4) |
| **Compute** | A definir no ADR — restrição de OAuth na plataforma (Downstream §6) |

---

## Áreas cinzentas

| Área | Opções consideradas | Decisão | Quem decidiu |
|------|---------------------|---------|--------------|
| Escopo da spec: P1 ou P1+P2 | A. Spec única P1+P2; B. Spec P1 agora, P2 como feature separada | Spec única P1+P2; prioridade segue Upstream §6 (Q1.2) | usuário |
| Nome da feature para artefatos | `PULSO_CEU`; `PULSO_CEU_P1` | `PULSO_CEU`, por cobrir P1+P2 (Q1.4) | usuário |
| Aprovação do Downstream v2 | Aprovado integralmente; aprovado com ressalvas na seção 5 | Aprovado integralmente (Q1.1) | usuário |
| Decomposição em sub-features | Feature única cobrindo P1+P2; split em ingestão + processamento + métricas + dashboard | Feature única PULSO_CEU: o PO quebra em histórias no TASKS (Q1.2 + Q1.4) | usuário |

## Diferenças em relação à fonte

| O que a fonte diz | O que esta spec faz | Por quê | Aprovado por |
|-------------------|---------------------|---------|--------------|
| Confluence › Downstream §7–8: opções de ingestão e riscos | Não entram como critérios | A arquitetura de ingestão não é decidida no Define — é insumo do ADR, conforme o próprio Downstream | n/a |

---

## Suposições

| ID | Padrão escolhido | Motivo | Origem | Se estiver errada |
|----|------------------|--------|--------|-------------------|
| S-1 | Mapeamento de dados conforme Downstream v2, seção 5 | Documento preparado pelo engenheiro com base nos schemas e exemplos oficiais do GCN | usuário delegou (Q1.1): "sim, aprovo o downstream v2 como está" | Algum critério R2.x ou R3.x precisa ser revisado |
| S-2 | A leitura de sondagem (Downstream §8) confirmará as regras de mapeamento antes do Build | Nenhuma mensagem real foi lida durante o Define | usuário delegou (Q1.1) | Alguma regra da seção 5.3 precisa de atualização e o Downstream ganha versão nova |

## Perguntas em aberto

- Q1.3: chave Jira (pendente)

---

## Rastreabilidade

| Critério | Origem |
|----------|--------|
| pedido | pedido: "Especifique o Pulso do Céu" → spec PULSO_CEU cobre P1+P2 (R1–R8) |
| pedido | pedido: "Projeto: /Workspace/.../pulso-do-ceu" → Contexto técnico: Onde fica no projeto |
| R1.1 | Confluence › Upstream §6: "toda mensagem dos tópicos do Anexo A, menos o heartbeat, fica guardada como chegou" + Confluence › Upstream §10 critério 1 |
| R1.2 | Confluence › Upstream §6: "O heartbeat fica guardado à parte, só para a operação" + Confluence › Upstream §10 critério 2 |
| R1.3 | Confluence › Upstream §4: "Tópicos de teste não entram: os que têm `.test.` no nome e os tipos Classic terminados em `_TEST`, além de `TEST_COORDS`" |
| R1.4 | Confluence › Upstream §9: "Se o produto parar por falha, ao voltar ele continua de onde parou" |
| R1.5 | Confluence › Upstream §4 + Downstream §5.4: "O arquivo histórico é baixado de novo toda vez que o produto liga" |
| R1.6 | Confluence › Upstream §4: "A credencial é segredo e nunca aparece no código" |
| R1.7 | Confluence › Upstream §9: "se o heartbeat ficar mais de 5 minutos sem chegar, o time de engenharia recebe um aviso por email" |
| R2.1 | Confluence › Upstream §3: "um alerta publicado no GCN aparece no dashboard em até 5 minutos, contados a partir do horário em que a mensagem chegou ao Kafka do GCN" |
| R2.2 | Confluence › Downstream §5.2 (aprovado em Q1.1) |
| R2.3 | Confluence › Upstream §9: "Mensagem que não for lida no formato esperado vai para a quarentena, com o motivo" + "Coordenada fora da faixa vai para a quarentena" |
| R2.4 | Confluence › Upstream §7: "Alerta de teste não entra nas métricas de negócio" |
| R2.5 | Confluence › Upstream §9: "A mesma mensagem recebida duas vezes aparece uma vez só" |
| R2.6 | Confluence › Upstream §9: "Um campo novo num schema do GCN não para o produto" |
| R2.7 | Confluence › Upstream §7: "Um evento retratado não entra nas contagens de eventos" + "ele continua na visão unificada de eventos, marcado como retratado" |
| R2.8 | Confluence › Downstream §5.3 regra 2: "O JSON alimenta a visão unificada. Os tipos Classic que repetem o mesmo evento ficam só no histórico bruto" |
| R2.9 | Confluence › Upstream §9: "Um tópico do Anexo A indisponível no GCN não para o produto" |
| R2.10 | Confluence › Upstream §10 critério 5 |
| R2.11 | Confluence › Upstream §10 critério 6 |
| R3.1 | Confluence › Upstream §10 critério 7 |
| R3.2 | Confluence › Upstream §10 critério 8 |
| R3.3 | Confluence › Upstream §7: "Circular editada: vale a versão de maior version de cada Circular. Com o mesmo version, vale a última mensagem recebida" |
| R3.4 | Confluence › Downstream §5.4 (aprovado em Q1.1) |
| R3.5 | Confluence › Upstream §10 critério 5 |
| R4.1 | Confluence › Upstream §4: "O email é dado pessoal e deve aparecer mascarado para quem não é do grupo de administradores" |
| R4.2 | Confluence › Upstream §5: "Só o grupo de administradores vê o email sem máscara" |
| R4.3 | Confluence › Upstream §4: "A máscara vale em todo lugar onde o email aparece, inclusive no histórico bruto e na quarentena" |
| R4.4 | Confluence › Upstream §5: "Fora dos grupos de engenharia e de administradores, ninguém vê o histórico bruto" |
| R4.5 | Confluence › Upstream §5 (tabela de grupos de acesso) |
| R5.1 | Confluence › Upstream §6 métrica 1 |
| R5.2 | Confluence › Upstream §6 métrica 2 |
| R5.3 | Confluence › Upstream §6 métrica 3 |
| R5.4 | Confluence › Upstream §6 métrica 4 |
| R5.5 | Confluence › Upstream §9: "O dashboard mostra o horário da última mensagem recebida" |
| R5.6 | Confluence › Upstream §7: "O dashboard deixa a pessoa mudar o limite de boa localização" |
| R5.7 | Confluence › Upstream §3: indicadores de sucesso |
| R5.8 | Confluence › Upstream §7: alertas de teste fora das métricas + métrica própria para operação |
| R6.1 | Confluence › Upstream §7: "Coincidência multimensageiro: dois eventos de missões diferentes, com os horários de disparo a até 500 segundos um do outro e distância no céu menor que a soma dos erros de localização" |
| R6.2 | Confluence › Upstream §7: "Evento sem posição ou sem erro de localização entra na coincidência só pelo tempo. A coincidência só pelo tempo fica marcada como temporal" |
| R6.3 | Confluence › Upstream §7: "Evento sem horário do disparo fica fora da coincidência" + "Evento retratado ou de teste fica fora da coincidência" |
| R7.1 | Confluence › Upstream §7: "Circulars por evento: contadas pelo nome do evento que o GCN dá à Circular, sem precisar ligar a Circular a uma notice" |
| R7.2 | Confluence › Upstream §7: "Tempo até a primeira Circular: vai do horário do disparo do evento até a primeira Circular com o nome dele. O tempo até a primeira Circular vale só para eventos da LIGO/Virgo/KAGRA e do IceCube" |
| R8.1 | Confluence › Upstream §6: "Consumo: um dashboard e um Genie Space em cima das métricas" |
| R8.2 | Confluence › Upstream §3: "Para cada pergunta de referência da seção 10, a resposta do Genie bate com a consulta direta nas métricas" |
| R8.3 | Confluence › Upstream §5 (tabela de grupos de acesso: `pulso-ceu-consumidores` acessa métricas, dashboard e Genie Space) |

---

## Aprovação

<!-- A ser preenchido quando o usuário aprovar -->

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-11-09 | Versão inicial — Rascunho |
