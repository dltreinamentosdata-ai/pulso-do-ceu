# DEFINE: Pulso do Céu

> Visão unificada e confiável dos alertas do NASA GCN, atualizada em minutos, para astrônomos de plantão, coordenação científica, divulgação científica e a operação de dados.

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | PULSO_DO_CEU |
| **Tamanho** | Complexo (confirmado em Q1.1) — domínio novo, Kafka externo com OAuth, 4 formatos e 20+ schemas, PII com máscara, decisão de arquitetura de ingestão em aberto |
| **Jira** | KAN-1 |
| **Data** | 2026-11-09 |
| **Status** | Aguardando aprovação |

---

## Fontes

| Fonte | Link | O que foi usado |
|-------|------|-----------------|
| Pedido do usuário | n/a | Pedido original (abaixo) |
| Confluence: Upstream - Pulso do Céu (versão 5, 08/11/2026; página v6 no Confluence) | https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/360450 | Seções 1 a 14 e Anexo A (lida inteira; sem subpáginas) |
| Confluence: Downstream - Pulso do Céu (v2, 08/11/2026; aprovado pelo usuário em Q1.2: Aprovado: 2026-11-09 — v2 — usuário: "sim, aprovo o downstream v2 como está") | https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/557058 | Seções 1 a 9 (lida inteira; sem subpáginas). Seção 5 = mapeamento; seções 6 a 8 = contexto do ADR |
| Ticket Jira | https://dltreinamentos-aidata-544385d7.atlassian.net/jira/browse/KAN-1 | Épico KAN-1 (status To Do), descrição e links das fontes |
| Repo do projeto | /Workspace/Users/dltreinamentos.data@gmail.com/projetos/pulso-do-ceu | Varredura: só `pulso-do-ceu/databricks.yml` (bundle com targets dev/prod, sem recursos), README e notebook `ambiente`; nenhum pipeline, teste ou tabela ainda |

---

## Registro do pedido e das respostas

### Pedido original

> "Especifique o Pulso do Céu. Projeto: /Workspace/Users/dltreinamentos.data@gmail.com/projetos/pulso-do-ceu 
> Upstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/360450. 
> Downstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/557058.
> Jira: https://dltreinamentos-aidata-544385d7.atlassian.net/jira/browse/KAN-1"

### Rodada 1

| ID | Pergunta, com a recomendação | Resposta do usuário |
|----|------------------------------|---------------------|
| Q1.1 | Tamanho da feature: classifico como **Complexo** (domínio novo, Kafka externo com OAuth, JSON/VOEvent/Circulars, PII com máscara e a decisão de ingestão em aberto no Downstream §7). Fluxo: Define com áreas cinzentas → Staff Engineer (ADR) → PO → Design → Build → Ship. Recomendação: Complexo. Você confirma Complexo? | "sim" |
| Q1.2 | O cabeçalho do Downstream v2 diz "Aprovação: Pendente" e a seção 5 só vira critério sem pergunta nova com a v2 aprovada. Você aprova o Downstream v2 (seção 5, mapeamento de dados) como regra desta spec? Responder "sim" = a seção 5 vira critério de aceite tal como está. Recomendação: sim, no formato `Aprovado: 2026-11-09 — v2 — usuário: "<suas palavras>"`, que eu registro aqui (e você atualiza no Confluence). | "sim, aprovo o downstream v2 como está" |
| Q1.3 | Escopo deste DEFINE: incluir P1 e P2 do Upstream §6 (P2 = Genie Space e métricas 5 e 6) num só DEFINE, com P2 marcado como prioridade P2, ou só P1 (P2 vai para Fora do escopo)? Recomendação: P1 e P2 no mesmo DEFINE, com prioridades, porque as métricas 5 e 6 usam as mesmas visões e o critério 17 do Upstream §10 depende do Genie. | "P1 e P2 no mesmo DEFINE, com prioridades" |
| Q1.4 | Retenção do histórico bruto: o Upstream §6 diz que ele é "a única cópia do passado", mas não diz por quanto tempo fica. Opções: A) sem expurgo, guardado indefinidamente; B) expurgo após N anos. Recomendação: A (volume de algumas centenas de mensagens por dia; os mapas da LVK pesam ~1,3 MB cada, ainda assim baixo). | "A" |
| Q1.5 | Retenção do heartbeat ("guardado à parte, só para a operação", ~86.400 mensagens/dia): Opções: A) 30 dias; B) 90 dias; C) sem expurgo. Recomendação: A (30 dias): cobre o aviso de 25 dias desligado e a investigação de falhas, sem acumular ~31 milhões de linhas/ano. | "A" |
| Q1.6 | Reprocessamento da quarentena (Upstream §9: "fica fora da visão unificada e das métricas até ser reprocessada"): Opções: A) manual, disparado pela operação depois de corrigir o leitor; B) automático a cada vez que o produto liga. Recomendação: A (manual), porque a mensagem só sai da quarentena quando o leitor muda; o reprocessamento não duplica linhas (Upstream §10 critério 5). | "A" |
| Q1.7 | Formato da máscara do email para quem não é `pulso-ceu-admins`: Opções: A) string fixa `***` no lugar do email inteiro; B) manter só o domínio (`***@nasa.gov`); C) nulo. Recomendação: A (sem vazamento parcial e fácil de testar). | "A" |
| Q1.8 | Email dentro de texto livre: no histórico bruto e na quarentena a mensagem é guardada "como chegou" (inclui o `body` das Circulars, que pode citar emails). Opções: A) para quem não é admin, todo trecho com formato de email no conteúdo da mensagem bruta/quarentena aparece mascarado, e na visão das Circulars só as colunas de email são mascaradas (o `body` fica como vem, o contrato do Upstream §8 diz `body` PII = não); B) mascarar emails também no `body` da visão das Circulars; C) mascarar só os campos `submitter`, `editedBy` e `email`, sem varrer texto livre. Recomendação: A. | "C" |
| Q1.9 | Endereço dos avisos por email (Upstream §9: "Na primeira entrega, o endereço é o do responsável pela engenharia"): recomendação `dltreinamentos.data@gmail.com` (o reporter do KAN-1, Douglas). Você confirma esse endereço? | "sim" |
| Q1.10 | Aviso de 25 dias desligado (Upstream §11): a contagem começa em quê? Opções: A) no horário da última mensagem do heartbeat gravada; B) no fim da última execução do produto (horário da última parada). Recomendação: A (é o sinal mais próximo da última conexão ao GCN, que é o que conta para os 30 dias da credencial). | "A" |
| Q1.11 | "Dias sem evento novo" (métrica 3, saúde das missões): Opções: A) dias inteiros completos = parte inteira de (agora − horário do último evento novo) ÷ 24 h, em UTC; B) diferença de datas de calendário UTC (hoje − data do último evento). Recomendação: A. | "A" |

### Rodada 2

| ID | Pergunta, com a recomendação | Resposta do usuário |
|----|------------------------------|---------------------|
| Q2.1 | Com Q1.7 = A (`***` no lugar do email inteiro) e Q1.8 = C (só os campos `submitter`, `editedBy` e `email`): no histórico bruto, na quarentena e no arquivo histórico guardado, o campo `submitter` vem como `Nome at Afiliação <email>`. Opções: A) trocar só o email por `***` (fica `Nome at Afiliação <***>`; no `editedBy` com "on behalf of", os dois emails viram `***`); B) trocar o valor inteiro do campo por `***`. Recomendação: A, porque o Upstream §4 diz que nome e afiliação "podem ficar visíveis". | "A" |
| Q2.2 | A opção C de Q1.8 difere do Upstream §4, que diz "A máscara vale em todo lugar onde o email aparece, inclusive no histórico bruto e na quarentena": um email citado no `body` de uma Circular (ou em outro texto livre) fica sem máscara no histórico bruto e na quarentena. Você aprova essa diferença em relação ao Upstream? Responder "sim" = a spec mascara só os três campos e registra a diferença como aprovada por você. Recomendação: se quiser seguir o Upstream à risca, responda "não" e eu troco para a opção A de Q1.8; se "sim", fica C. | "sim" |
| Q2.3 | Retenção dos downloads do arquivo histórico de Circulars (o Downstream §5.4 manda guardar "cada download", um por vez que o produto liga, ~46 mil Circulars cada, e não dá retenção). Opções: A) sem expurgo, como o histórico bruto (Q1.4); B) manter só os últimos N downloads (ex.: 5); C) manter só o mais recente. Recomendação: B com N = 5: o reprocessamento usa só o mais recente e as Circulars já ficam na visão e no histórico bruto do Kafka. | "B, com N = 5" |

---

## Problema

Quem acompanha o céu transiente precisa olhar dezenas de tópicos do GCN, cada um num formato, e não tem uma visão única do que está acontecendo, de quais eventos foram vistos por mais de um instrumento, da latência de cada missão nem de quais missões pararam (Upstream §1). Exemplo do custo: o Swift encerrou em 20/10/2026 e em 07/11/2026 o GCN ainda o listava como operacional.

## Quem usa o dado

| Quem | Para quê | Dor hoje |
|------|----------|----------|
| Astrônomo de plantão (follow-up) | Decidir se aponta um telescópio para um evento | Precisa abrir vários tópicos e converter formatos na mão (Upstream §2) |
| Coordenação científica | Acompanhar a rede de observatórios | Não sabe o volume, a latência nem quais missões estão ativas (Upstream §2) |
| Divulgação científica | Contar os eventos notáveis da semana | Não sabe o que a comunidade está comentando (Upstream §2) |
| Engenharia de dados (operação) | Manter o produto de pé | Não tem sinal de saúde do stream (Upstream §2) |

---

## Escopo

### Dentro do escopo

- P1: histórico bruto (com heartbeat à parte), visão unificada de eventos, visão das Circulars (arquivo histórico + Kafka), quarentena, grupos de acesso e máscara do email, métricas 1 a 4, métrica de alertas de teste, dashboard, operação (avisos por email), disponibilidade (liga/desliga à mão) e reprocessamento (Upstream §6, Prioridade).
- P2: Genie Space e métricas 5 (coincidências multimensageiro) e 6 (resposta da comunidade), no mesmo DEFINE (Q1.3).
- Tópicos: exatamente os do Anexo A do Upstream; mapeamento de colunas conforme o Downstream v2 §5 (aprovado em Q1.2).

### Fora do escopo

- Tudo o que o Upstream §12 lista: área do céu a partir dos mapas HEALPix; mapas do céu na visão unificada (ficam só no histórico bruto); visão própria do BOOM (só histórico bruto); notices `eclairs-catalog`, `slewing` e `not-slewing` do SVOM na visão; tipos Classic `ICECUBE_ASTROTRACK_GOLD`, `ICECUBE_ASTROTRACK_BRONZE`, `MAXI_KNOWN` e `MAXI_UNKNOWN` na visão; agente de perguntas sobre o texto das Circulars; envio de alertas astronômicos a usuários finais; formatos Classic de texto e binário e HTML antigo; tipos `*_POINTDIR`, `*_SC_SLEW`, `SWIFT_TOO_*`; publicar no GCN.
- Tópicos de teste do GCN (`.test.`, Classic `_TEST`, `TEST_COORDS`) e os tópicos `gcn.circulars.<tipo>` (Upstream §4).
- Mensagens que o GCN descartou enquanto o produto estava desligado (Upstream §11: "o produto aceita essa perda").
- Sinônimos de `eventId` do GCN (Downstream §5.5).
- Decisão de ingestão, compute, trigger, camadas e deploy: fica para o ADR (Downstream §7). Esta spec diz o que o dado faz, não como é construído.
- Leitura de sondagem do GCN: é ação de antes do Build (Downstream §8). Se ela contrariar a seção 5 do Downstream, o Downstream ganha versão nova e esta spec passa pelo `@sdd-iterate`.

---

## Requisitos

### R1: Histórico bruto — P1

**Por quê:** o Kafka do GCN não guarda o passado para sempre; o histórico bruto é a única cópia e a base de todo reprocessamento.

**Critérios de aceite (EARS):**

- **R1.1** QUANDO chegar uma mensagem de um tópico do Anexo A que não seja `gcn.heartbeat` ENTÃO o produto DEVE gravá-la no histórico bruto com o conteúdo byte a byte como chegou e com tópico, partição, offset e `kafka_time` não nulos, inclusive as mensagens que ficam fora da visão unificada e os mapas do céu dentro delas.
- **R1.2** O histórico bruto DEVE ter no máximo uma linha por (tópico, partição, offset), mesmo que a mesma mensagem seja recebida duas vezes.
- **R1.3** QUANDO chegar uma mensagem de `gcn.heartbeat` ENTÃO o produto DEVE gravá-la numa tabela de heartbeat separada do histórico bruto, e o histórico bruto NÃO DEVE ter nenhuma linha de `gcn.heartbeat`.
- **R1.4** O produto DEVE manter as linhas do histórico bruto sem expurgo: nenhuma linha é apagada por idade.
- **R1.5** O produto DEVE manter na tabela de heartbeat só as mensagens com `kafka_time` dos últimos 30 dias; mensagem com mais de 30 dias DEVE ser apagada.
- **R1.6** O produto DEVE assinar só os tópicos do Anexo A: nenhuma linha do histórico bruto vem de tópico com `.test.` no nome, de tipo Classic terminado em `_TEST`, de `TEST_COORDS` ou de `gcn.circulars.<tipo>`.
- **R1.7** SE uma mensagem trouxer um campo que o schema conhecido não tem ENTÃO o produto DEVE guardar o campo no histórico bruto, continuar rodando e não mudar as colunas das visões.
- **R1.8** SE um tópico do Anexo A estiver indisponível no GCN (aviso `Subscribed topic not available`) ENTÃO o produto DEVE continuar lendo os outros tópicos sem parar.

### R2: Visão unificada de eventos — P1

**Por quê:** todos os alertas, de todas as missões e formatos, num modelo comum, para responder "o que está acontecendo no céu agora".

**Critérios de aceite (EARS):**

- **R2.1** QUANDO uma mensagem de um tópico marcado "sim" na tabela 5.1 do Downstream for lida sem erro ENTÃO a visão unificada DEVE ter exatamente uma linha para ela, com as colunas do contrato preenchidas pelas regras da tabela 5.2 do Downstream para o formato dela (JSON Unified, JSON da LVK ou VOEvent).
- **R2.2** A visão unificada DEVE preencher `mission`, `instrument` e `messenger` pela tabela 5.1 do Downstream, mesmo quando a mensagem traz o campo; a exceção é o `instrument` da LIGO/Virgo/KAGRA, que é `event.instruments` unido por vírgula na ordem em que vem, e nulo na retração.
- **R2.3** A visão unificada DEVE montar `event_uid` como a missão da tabela 5.1, dois-pontos e o ID do disparo nas formas da tabela 5.2 do Downstream (`id` em lista unido por vírgula; LVK `LIGO/Virgo/KAGRA:<superevent_id>`; IceCube `IceCube:<run_id>_<event_id>`; SVOM `SVOM:<Burst_Id>`; Classic sem `TrigID`: `<mission>:<ISOTime>`).
- **R2.4** A visão unificada NÃO DEVE ter linhas de `gcn.notices.boom.alert`, de `ICECUBE_ASTROTRACK_GOLD`, `ICECUBE_ASTROTRACK_BRONZE`, `MAXI_KNOWN`, `MAXI_UNKNOWN`, nem dos notices SVOM `eclairs-catalog`, `slewing` e `not-slewing`; essas mensagens ficam só no histórico bruto.
- **R2.5** A visão unificada DEVE marcar `is_test = true` quando: JSON com `alert_tense` em `test`, `planned`, `injection` ou `commanded`; LVK com `superevent_id` que não começa com `S`; busca do IceCube para a LVK com `ref_ID` que não começa com `S`; VOEvent com `role = test`, Fermi GBM com `Test_Submission` verdadeiro, ou IceCube com a marca `Test` ou `InternalTest`. Em qualquer outro caso, inclusive sem o campo, `is_test = false`.
- **R2.6** A visão unificada DEVE marcar `is_retraction = true` quando: JSON com `alert_type = retraction`; LVK com `alert_type = RETRACTION`; VOEvent com `Citations/EventIVORN` `cite="retraction"` ou IceCube com a marca `Retraction`. Em qualquer outro caso, inclusive sem o campo e com `Def_NOT_a_GRB` do Fermi GBM, `is_retraction = false`.
- **R2.7** A visão unificada DEVE marcar `is_archival = true` só em JSON Unified com `alert_tense = archival`; em todo o resto, `false`.
- **R2.8** O estado atual de cada `event_uid` DEVE vir do alerta de maior `alert_time`; sem `alert_time`, ou no empate, desempata o maior `kafka_time`, depois a maior partição e o maior offset — independentemente da ordem de chegada.
- **R2.9** QUANDO chegar uma mensagem de `gcn.notices.icecube.lvk_nu_track_search` ENTÃO a visão unificada DEVE gravá-la como alerta com `event_uid = LIGO/Virgo/KAGRA:<ref_ID>` e `mission = IceCube`, e ela NÃO DEVE mudar o estado atual do evento da LVK, NÃO DEVE contar como evento novo do IceCube e DEVE contar nas métricas de alertas do IceCube; os neutrinos de `coincident_events` ficam só no histórico bruto.
- **R2.10** A visão unificada DEVE gravar `error_deg` como: número = o próprio valor; lista = o maior entre os dois primeiros valores (o 3º não entra); `rectangular_error_corners` ou sem erro = nulo; VOEvent = `Error2Radius`; LVK = nulo.
- **R2.11** A visão unificada DEVE gravar `far` em Hz (IceCube Classic: `FAR` ÷ 31.557.600) e `p_astro` como `p_astro` do JSON, `1 − event.classification.Terrestrial` na LVK quando `event.group = CBC`, `signalness` no IceCube Classic, e nulo nos outros casos.
- **R2.12** SE `error_deg` não for maior que 0, `far` for menor que 0, ou `p_astro` estiver fora de 0 a 1 ENTÃO a visão unificada DEVE gravar aquele valor como nulo e manter a linha.
- **R2.13** A visão unificada DEVE gravar todos os horários em UTC, lendo o `ISOTime` do VOEvent (sem `Z`) como UTC.
- **R2.14** A visão unificada DEVE ter no máximo uma linha por (`source_topic`, `source_partition`, `source_offset`).
- **R2.15** ENQUANTO o produto estiver ligado, uma mensagem lida sem erro DEVE aparecer na visão unificada em até 5 minutos depois do seu `kafka_time`.
- **R2.16** QUANDO a missão retratar um evento ENTÃO o evento DEVE continuar na visão unificada, com o estado atual marcado como retratado.

### R3: Quarentena — P1

**Por quê:** mensagem que não pôde ser lida não some e não para o produto.

**Critérios de aceite (EARS):**

- **R3.1** SE uma mensagem não for lida no formato esperado, tiver RA fora de 0–360 ou Dec fora de −90 a 90, ou não permitir montar o `event_uid` ENTÃO o produto DEVE gravá-la na quarentena como chegou, com tópico, partição, offset, `kafka_time`, motivo (um destes três) e horário da entrada, e ela NÃO DEVE aparecer na visão unificada nem nas métricas.
- **R3.2** SE uma mensagem for para a quarentena ENTÃO o produto DEVE continuar processando as mensagens seguintes sem parar.
- **R3.3** O produto DEVE manter na quarentena só as entradas dos últimos 90 dias; entrada com mais de 90 dias DEVE ser apagada.
- **R3.4** QUANDO a operação disparar manualmente o reprocessamento da quarentena ENTÃO cada mensagem que agora for lida sem erro DEVE entrar na visão unificada (no máximo uma linha por tópico, partição e offset) e sair da quarentena; a que ainda falhar DEVE continuar na quarentena. Não há reprocessamento automático da quarentena.

### R4: Visão das Circulars — P1

**Por quê:** a versão que vale de cada Circular, do arquivo histórico desde 1997 e do Kafka, num só lugar.

**Critérios de aceite (EARS):**

- **R4.1** QUANDO o produto ligar ENTÃO ele DEVE baixar `https://gcn.nasa.gov/circulars/archive.json.tar.gz`, guardar o download como veio, à parte do histórico bruto do Kafka, com o horário do download, e a visão das Circulars DEVE passar a ter todo `circularId` desse arquivo.
- **R4.2** A visão das Circulars DEVE ter exatamente uma linha por `circular_id`, com a versão de maior `version`; no empate de `version`, a mais recente entre o `kafka_time` (Kafka) e o horário do download (arquivo).
- **R4.3** SE a Circular vier sem `version` ENTÃO a visão das Circulars DEVE tratar `version = 1`.
- **R4.4** A visão das Circulars DEVE separar o `submitter`: `Nome at Afiliação <email>` preenche nome, afiliação e email; `Nome <email>` deixa a afiliação nula; só o email deixa nome e afiliação nulos.
- **R4.5** A visão das Circulars DEVE gravar em `edited_by_email` o email de quem editou; em `<moderador> on behalf of <solicitante>`, o do moderador.
- **R4.6** A visão das Circulars DEVE converter `createdOn` (milissegundos UNIX) em `created_on` TIMESTAMP UTC, e `event_id`, `subject` e `body` vêm como estão na versão que vale.
- **R4.7** A visão das Circulars DEVE ler só o tópico `gcn.circulars` do Kafka, e ler os campos da mensagem real (`version`, `editedBy`, `editedOn`, `bibcode`, `email`), não só os do schema publicado.
- **R4.8** O produto DEVE manter guardados só os 5 downloads mais recentes do arquivo histórico de Circulars; QUANDO um 6º download for guardado ENTÃO o mais antigo DEVE ser apagado.

### R5: Acesso e máscara do email — P1

**Por quê:** o email das Circulars é dado pessoal; o resto do produto tem público definido por grupo.

**Critérios de aceite (EARS):**

- **R5.1** O produto DEVE dar ao grupo `pulso-ceu-consumidores` leitura só das métricas, do dashboard e do Genie Space; esse grupo NÃO DEVE ler o histórico bruto, a visão unificada, a visão das Circulars, a quarentena nem o heartbeat.
- **R5.2** O produto DEVE dar ao grupo `pulso-ceu-engenharia` leitura do histórico bruto, da visão unificada, da visão das Circulars, da quarentena e das métricas, com o email mascarado.
- **R5.3** O produto DEVE dar ao grupo `pulso-ceu-admins` leitura de tudo, com o email sem máscara.
- **R5.4** Para quem não é de `pulso-ceu-admins`, a visão das Circulars DEVE mostrar `***` em `submitter_email` e `edited_by_email` (não nulos na origem); `submitter_name` e `submitter_affiliation` ficam visíveis.
- **R5.5** Para quem não é de `pulso-ceu-admins`, no histórico bruto, na quarentena e no arquivo histórico guardado, o produto DEVE mostrar `***` no lugar de cada email dos campos `submitter`, `editedBy` e `email` das Circulars, trocando só o email (ex.: `Nome at Afiliação <***>`; no `editedBy` com "on behalf of", os dois emails viram `***`); o resto do conteúdo, inclusive o `body`, fica como chegou.
- **R5.6** A credencial do GCN (client ID e client secret) DEVE ficar num segredo do Databricks e nunca aparecer no código, no bundle nem em logs.

### R6: Métricas de negócio 1 a 4 e métrica de testes — P1

**Por quê:** volume, latência, saúde das missões e ciclo de vida dos eventos, para o dashboard e o Genie.

**Critérios de aceite (EARS):**

- **R6.1** O produto DEVE calcular as métricas de negócio só com linhas de `is_test = false`, contar cada `event_uid` uma vez nas métricas de eventos, sem os eventos cujo estado atual é retratado, e contar cada mensagem nas métricas de alertas.
- **R6.2** Nos períodos (dia, últimos 7 dias, mês corrente, em UTC), o produto DEVE contar o evento pelo `trigger_time` do estado atual (sem ele, pelo `kafka_time` do primeiro alerta) e o alerta pelo `kafka_time`.
- **R6.3** A métrica 1 DEVE dar a contagem de alertas por dia, `mission`, `instrument` e `messenger`.
- **R6.4** A métrica 2 DEVE dar, por missão, a mediana e o p95 de (`alert_time` − `trigger_time`) e de (`kafka_time` − `alert_time`), excluindo `is_archival = true` e linhas com o horário necessário nulo; missão sem nenhum valor fica com latência nula.
- **R6.5** A métrica 3 DEVE dar, por missão da lista de referência: horário do último alerta, dias sem evento novo (parte inteira de (agora − horário do último evento novo) ÷ 24 h, UTC) e situação `ativa`, `em silêncio` ou `encerrada`.
- **R6.6** A situação DEVE ser `encerrada` para as missões encerradas da lista de referência, com a data de fim: Swift 20/10/2026, INTEGRAL 28/02/2025, BurstCube 13/09/2024, AGILE 18/01/2024 e MOA com o ano 2021, sem dia.
- **R6.7** Uma missão ativa DEVE ficar `em silêncio` quando estiver sem evento novo há mais de 3 vezes o intervalo mediano entre os eventos novos dela nos últimos 90 dias; com menos de 5 eventos novos nos últimos 90 dias, depois de mais de 30 dias sem evento novo. SNEWS e Super-Kamiokande NÃO entram na regra de silêncio e ficam `ativa` enquanto não encerradas; o BOOM fica fora da métrica 3.
- **R6.8** A métrica 4 DEVE dar, por `event_uid`, o número de alertas e se o estado atual é retratado.
- **R6.9** O produto DEVE dar à operação uma métrica própria com a contagem de alertas de teste (`is_test = true`) por missão e por dia.

### R7: Dashboard — P1

**Por quê:** a visão de "o que está acontecendo no céu agora" para quem não escreve SQL.

**Critérios de aceite (EARS):**

- **R7.1** O dashboard DEVE mostrar alertas por missão ao longo do tempo, a latência por missão (com "não informado" quando nula), a situação de cada missão com a data de fim das encerradas, os eventos retratados e o mapa do céu (RA × Dec) dos eventos com posição.
- **R7.2** O dashboard DEVE mostrar o horário da última mensagem recebida.
- **R7.3** O dashboard DEVE ter um filtro de boa localização com `error_deg` até 1 grau por padrão, que a pessoa pode mudar.
- **R7.4** ENQUANTO o produto estiver ligado, um alerta DEVE aparecer no dashboard em até 5 minutos depois do seu `kafka_time`.

### R8: Operação, disponibilidade e reprocessamento — P1

**Por quê:** o produto liga e desliga à mão, não pode perder a credencial do GCN e precisa ser reconstruível.

**Critérios de aceite (EARS):**

- **R8.1** QUANDO o produto ligar pela primeira vez ENTÃO ele DEVE ler cada tópico do Anexo A desde o offset mais antigo que o GCN ainda guarda.
- **R8.2** QUANDO o produto religar, depois de uma parada manual ou de uma falha, ENTÃO ele DEVE continuar de onde parou, sem duplicar linhas e trazendo as mensagens do período parado que o GCN ainda guarda.
- **R8.3** O cliente do GCN DEVE ser de longa duração, ligado e desligado à mão pela operação, e NÃO DEVE ser disparado por agendamento periódico.
- **R8.4** SE, enquanto o produto estiver ligado, passarem mais de 5 minutos sem chegar mensagem de `gcn.heartbeat` ENTÃO o produto DEVE mandar um aviso por email ao endereço configurável, que na primeira entrega é `dltreinamentos.data@gmail.com`.
- **R8.5** QUANDO se completarem 25 dias desde o `kafka_time` da última mensagem de heartbeat gravada ENTÃO o produto DEVE mandar um aviso por email ao mesmo endereço configurável.
- **R8.6** QUANDO a visão unificada, a visão das Circulars e as métricas forem reprocessadas a partir do histórico bruto e do download mais recente do arquivo de Circulars ENTÃO o resultado NÃO DEVE ter linha duplicada e DEVE ser igual ao de antes para as mesmas entradas, e o histórico bruto DEVE manter todas as suas linhas.

### R9: Genie Space — P2

**Por quê:** perguntar em linguagem natural sem saber SQL.

**Critérios de aceite (EARS):**

- **R9.1** O Genie Space DEVE ficar em cima das métricas e, para cada uma das 7 perguntas de referência do Upstream §10 critério 17, DEVE dar a mesma resposta que a consulta direta nas métricas.

### R10: Coincidências multimensageiro (métrica 5) — P2

**Por quê:** saber quais eventos foram vistos por mais de um instrumento.

**Critérios de aceite (EARS):**

- **R10.1** A métrica 5 DEVE listar como coincidência cada par de eventos de missões diferentes com `trigger_time` do estado atual a até 500 segundos um do outro e distância angular menor que a soma dos `error_deg` dos dois.
- **R10.2** SE um dos eventos do par não tiver posição ou `error_deg` ENTÃO a métrica 5 DEVE aceitar o par só pelo critério de tempo e marcá-lo como coincidência temporal.
- **R10.3** A métrica 5 NÃO DEVE incluir eventos sem `trigger_time`, retratados ou de teste, nem formar par entre a busca do IceCube para a LVK e o evento da LVK que ela acompanha.

### R11: Resposta da comunidade (métrica 6) — P2

**Por quê:** saber o que a comunidade está comentando.

**Critérios de aceite (EARS):**

- **R11.1** A métrica 6 DEVE contar Circulars por `event_id` da visão das Circulars, sem ligar a Circular a uma notice.
- **R11.2** A métrica 6 DEVE dar o tempo até a primeira Circular (menor `created_on` − `trigger_time` do estado atual) só para eventos da LIGO/Virgo/KAGRA (`event_id` = `LIGO/Virgo/KAGRA ` + `event_name`) e do IceCube Gold/Bronze em JSON (`event_id` = `event_name`); os outros eventos ficam fora dessa medida.

---

## Requisitos implícitos de dados

| Dimensão | Como fica nesta feature |
|----------|-------------------------|
| Idempotência e reprocessamento | R8.6, R1.2, R2.14, R3.4 |
| Dado atrasado ou fora de ordem | R2.8 (estado pelo `alert_time`, não pela chegada); R8.2; mensagem já descartada pelo GCN: fora do escopo |
| Duplicidade | R1.2, R2.14, R4.2 |
| Evolução de schema | R1.7 |
| Backfill e carga histórica | R8.1, R4.1 |
| Qualidade (nulos, chaves, faixas de valor) | R3.1, R2.12 |
| Falha parcial e retomada | R8.2, R3.2, R1.8 |
| PII, grants e Unity Catalog | R5.1, R5.2, R5.3, R5.4, R5.5, R5.6 |
| Freshness e SLA | R2.15, R7.4 |
| Volume, custo e compute | fora do escopo: volume do Upstream §4 e Downstream §3 vai como insumo do ADR, que decide compute e trigger (Downstream §7); retenções em R1.4, R1.5, R3.3 e R4.8 |
| Observabilidade e alerta | R8.4, R8.5, R7.2, R6.9 |

---

## Contrato de dados

### Fontes de dados

| Fonte | Tipo | Volume | Freshness | Dono |
|-------|------|--------|-----------|------|
| GCN Kafka — notices JSON e VOEvent (Anexo A) | Kafka (SASL_SSL, OAUTHBEARER) | dezenas a centenas por dia | tempo real (segundos) | NASA GCN / cada missão |
| GCN Kafka — `gcn.circulars` | Kafka | ~8 por dia | tempo real | NASA GCN |
| GCN Kafka — `gcn.heartbeat` | Kafka | ~86.400 por dia | tempo real | NASA GCN |
| Arquivo histórico de Circulars (`archive.json.tar.gz`) | Arquivo HTTPS (redireciona para S3) | ~46 mil Circulars desde 1997 | gerado 1x por dia; baixado a cada vez que o produto liga | NASA GCN |
| Exemplos oficiais (`nasa-gcn/gcn-schema`, `*.example.json`) | Arquivos | ~50 arquivos | estático | NASA GCN (massa de teste) |

### Schema de saída — visão unificada de eventos

| Coluna | Tipo | Regra | PII? |
|--------|------|-------|------|
| `event_uid` | STRING | não nulo (R2.3) | não |
| `source_topic` | STRING | não nulo | não |
| `source_partition` | INT | não nulo | não |
| `source_offset` | BIGINT | não nulo; (tópico, partição, offset) único | não |
| `source_format` | STRING | `json` ou `voevent` | não |
| `mission` | STRING | não nulo (tabela 5.1) | não |
| `instrument` | STRING | tabela 5.1; nulo quando "—" | não |
| `messenger` | STRING | `EM`, `GW` ou `Neutrino` | não |
| `alert_type` | STRING | como a missão manda (R2.1) | não |
| `is_retraction` | BOOLEAN | não nulo (R2.6) | não |
| `is_test` | BOOLEAN | não nulo (R2.5) | não |
| `is_archival` | BOOLEAN | não nulo (R2.7) | não |
| `event_name` | STRING | nulo quando a missão não manda | não |
| `trigger_time` | TIMESTAMP | UTC; nulo quando não informado | não |
| `alert_time` | TIMESTAMP | UTC; nulo quando não informado | não |
| `kafka_time` | TIMESTAMP | não nulo, UTC | não |
| `ra` | DOUBLE | 0 a 360; nulo sem posição; fora da faixa vai para a quarentena | não |
| `dec` | DOUBLE | −90 a 90; nulo sem posição; fora da faixa vai para a quarentena | não |
| `error_deg` | DOUBLE | maior que 0; fora da faixa = nulo | não |
| `far` | DOUBLE | ≥ 0, Hz; fora da faixa = nulo | não |
| `p_astro` | DOUBLE | 0 a 1; fora da faixa = nulo | não |

### Schema de saída — visão das Circulars

| Coluna | Tipo | Regra | PII? |
|--------|------|-------|------|
| `circular_id` | BIGINT | chave, não nulo, único | não |
| `version` | INT | maior vence; sem o campo = 1 | não |
| `event_id` | STRING | como vem na versão que vale | não |
| `subject` | STRING | não nulo | não |
| `body` | STRING | não nulo | não |
| `created_on` | TIMESTAMP | não nulo, UTC | não |
| `submitter_name` | STRING | pode ser nulo | sim (autoria pública, visível) |
| `submitter_affiliation` | STRING | pode ser nulo | não |
| `submitter_email` | STRING | `***` para quem não é admin | sim |
| `edited_by_email` | STRING | `***` para quem não é admin | sim |

### Outras saídas

| Saída | Conteúdo mínimo | Retenção |
|-------|-----------------|----------|
| Histórico bruto | conteúdo como chegou, tópico, partição, offset, `kafka_time` | sem expurgo (R1.4) |
| Heartbeat | `kafka_time` e conteúdo | 30 dias (R1.5) |
| Quarentena | conteúdo como chegou, tópico, partição, offset, `kafka_time`, motivo, horário da entrada | 90 dias (R3.3) |
| Downloads do arquivo de Circulars | arquivo como veio, horário do download | os 5 mais recentes (R4.8); o reprocessamento usa só o mais recente |
| Lista de referência de missões | missão, situação, data de fim | mantida pelo produto |

---

## Contexto técnico

| Aspecto | Valor |
|---------|-------|
| **Onde fica no projeto** | bundle `pulso-do-ceu/` (`databricks.yml`, `resources/*.yml`); código e testes a definir no Design |
| **Skills Databricks** | @databricks-pipelines, @databricks-spark-structured-streaming, @databricks-dabs, @databricks-jobs, @databricks-unity-catalog, @databricks-aibi-dashboards, @databricks-genie-agents |
| **Infraestrutura nova** | segredo com a credencial do GCN; grupos `pulso-ceu-consumidores`, `pulso-ceu-engenharia`, `pulso-ceu-admins`; saída de rede para os brokers do GCN (9092), `auth.gcn.nasa.gov:443`, `gcn.nasa.gov:443` e o host S3 (Downstream §2) — cada um exige "ok" explícito no Build |
| **Trigger** | ligado e desligado à mão; contínuo enquanto ligado (Upstream §11); a forma fica para o ADR |
| **Compute** | decisão do ADR (Downstream §6 e §7: OAuth M2M e Unity Catalog) |

---

## Áreas cinzentas

| Área | Opções consideradas | Decisão | Quem decidiu |
|------|---------------------|---------|--------------|
| Escopo P1 × P2 | um DEFINE com P1 e P2; só P1 | um DEFINE, com prioridades (R9 a R11 são P2) | usuário (Q1.3) |
| Retenção do histórico bruto | sem expurgo; expurgo após N anos | sem expurgo (R1.4) | usuário (Q1.4) |
| Retenção do heartbeat | 30 dias; 90 dias; sem expurgo | 30 dias (R1.5) | usuário (Q1.5) |
| Reprocessamento da quarentena | manual; automático ao ligar | manual (R3.4) | usuário (Q1.6) |
| Formato da máscara | `***`; só o domínio; nulo | `***` (R5.4, R5.5) | usuário (Q1.7) |
| Email em texto livre | varrer o conteúdo bruto; mascarar também o `body`; só os campos de email | só `submitter`, `editedBy` e `email` (R5.5); diferença do Upstream em Q2.2 | usuário (Q1.8) |
| Forma do campo mascarado no bruto | trocar só o email; trocar o campo inteiro | trocar só o email (R5.5) | usuário (Q2.1) |
| Retenção dos downloads de Circulars | sem expurgo; últimos N; só o mais recente | últimos 5 (R4.8) | usuário (Q2.3) |
| Endereço dos avisos | `dltreinamentos.data@gmail.com` | confirmado (R8.4, R8.5) | usuário (Q1.9) |
| Início da contagem dos 25 dias | última mensagem de heartbeat; última parada | última mensagem de heartbeat (R8.5) | usuário (Q1.10) |
| "Dias sem evento novo" | dias inteiros de 24 h; diferença de datas | dias inteiros de 24 h, UTC (R6.5) | usuário (Q1.11) |

## Diferenças em relação à fonte

| O que a fonte diz | O que esta spec faz | Por quê | Aprovado por |
|-------------------|---------------------|---------|--------------|
| Upstream §4: "A máscara vale em todo lugar onde o email aparece, inclusive no histórico bruto e na quarentena." | mascara só os campos `submitter`, `editedBy` e `email`; email citado em texto livre (ex.: `body`) fica sem máscara no histórico bruto e na quarentena | escolha do usuário em Q1.8 (opção C) | usuário, 2026-11-09 (Q2.2: "sim") |

---

## Suposições

Nenhuma.

## Perguntas em aberto

Nenhuma.

---

## Rastreabilidade

| Critério | Origem |
|----------|--------|
| R1.1 | pedido: "Especifique o Pulso do Céu"; pedido: "Projeto: /Workspace/Users/dltreinamentos.data@gmail.com/projetos/pulso-do-ceu Upstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/360450"; Confluence › Upstream §6: "toda mensagem dos tópicos do Anexo A, menos o heartbeat, fica guardada como chegou" |
| R1.2 | Confluence › Upstream §9: "A mesma mensagem recebida duas vezes aparece uma vez só." |
| R1.3 | Confluence › Upstream §6: "O heartbeat fica guardado à parte, só para a operação." |
| R1.4 | Q1.4: "A" |
| R1.5 | Q1.5: "A" |
| R1.6 | Confluence › Upstream §4: "Tópicos de teste não entram" |
| R1.7 | Confluence › Upstream §9: "O campo novo fica preservado no histórico bruto." |
| R1.8 | Confluence › Upstream §9: "Um tópico do Anexo A indisponível no GCN não para o produto." |
| R2.1 | Q1.2: "sim, aprovo o downstream v2 como está"; pedido: "Downstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/557058"; Confluence › Downstream §5.2 |
| R2.2 | Confluence › Downstream §5.1: "Missão, instrumento e mensageiro saem sempre desta tabela" |
| R2.3 | Confluence › Downstream §5.3, regra 1 (Chave do evento) |
| R2.4 | Confluence › Upstream §12 (Fora do escopo); Confluence › Downstream §5.3, regras 2 e 8 |
| R2.5 | Confluence › Upstream §7 (Alerta de teste); Confluence › Downstream §5.2 (`is_test`) |
| R2.6 | Confluence › Downstream §5.3, regra 7 (Retração no VOEvent); Confluence › Downstream §5.2 (`is_retraction`) |
| R2.7 | Confluence › Upstream §7: "Alerta de arquivo fica marcado como de arquivo" |
| R2.8 | Confluence › Downstream §5.3, regra 4 (Estado do evento) |
| R2.9 | Confluence › Upstream §7: "Essa busca não conta como evento novo do IceCube."; Confluence › Downstream §5.3, regra 3 |
| R2.10 | Confluence › Downstream §5.3, regra 6 (Erro de localização) |
| R2.11 | Confluence › Downstream §5.2 (`far`, `p_astro`) |
| R2.12 | Confluence › Upstream §9: "A mensagem com esse valor segue para a visão." |
| R2.13 | Confluence › Upstream §7: "todos os horários do produto são em UTC" |
| R2.14 | Confluence › Upstream §7: "uma mensagem é identificada pelo tópico, pela partição e pelo offset do Kafka" |
| R2.15 | Confluence › Upstream §10, critério 3 |
| R2.16 | Confluence › Upstream §7: "ele continua na visão unificada de eventos, marcado como retratado" |
| R3.1 | Confluence › Upstream §9: "Mensagem que não for lida no formato esperado vai para a quarentena, com o motivo."; Confluence › Downstream §5.6 |
| R3.2 | Confluence › Upstream §9: "Uma mensagem na quarentena não para o produto." |
| R3.3 | Confluence › Upstream §9: "A quarentena guarda cada mensagem por 90 dias." |
| R3.4 | Q1.6: "A" |
| R4.1 | Confluence › Upstream §10, critério 7; Confluence › Downstream §5.4 (Arquivo histórico) |
| R4.2 | Confluence › Downstream §5.4 (Arquivo × Kafka); Confluence › Upstream §10, critério 8 |
| R4.3 | Confluence › Downstream §5.4 (`version`: sem o campo, vale 1) |
| R4.4 | Confluence › Downstream §5.4 (`submitter`) |
| R4.5 | Confluence › Downstream §5.4 (`edited_by_email`) |
| R4.6 | Confluence › Downstream §5.4 (`created_on`) |
| R4.7 | Confluence › Upstream §4: "Das Circulars, entra só o tópico `gcn.circulars`."; Confluence › Downstream §5.4 |
| R4.8 | Q2.3: "B, com N = 5" |
| R5.1 | Confluence › Upstream §5 (`pulso-ceu-consumidores`) |
| R5.2 | Confluence › Upstream §5 (`pulso-ceu-engenharia`) |
| R5.3 | Confluence › Upstream §5: "Só o grupo de administradores vê o email sem máscara." |
| R5.4 | Q1.7: "A" |
| R5.5 | Q1.8: "C"; Q1.7: "A"; Q2.1: "A"; Q2.2: "sim" |
| R5.6 | Confluence › Upstream §4: "A credencial é segredo e nunca aparece no código." |
| R6.1 | Confluence › Upstream §7: "Alerta de teste não entra nas métricas de negócio." |
| R6.2 | Confluence › Upstream §7 (Período) |
| R6.3 | Confluence › Upstream §6, métrica 1 |
| R6.4 | Confluence › Upstream §6, métrica 2; Confluence › Upstream §7: "Alerta de arquivo fica fora da métrica de latência." |
| R6.5 | Q1.11: "A"; Confluence › Upstream §6, métrica 3 |
| R6.6 | Confluence › Upstream §10, critérios 15 e 16 |
| R6.7 | Confluence › Upstream §7 (Missão em silêncio) |
| R6.8 | Confluence › Upstream §6, métrica 4 |
| R6.9 | Confluence › Upstream §7: "A operação vê a contagem de alertas de teste por missão numa métrica própria." |
| R7.1 | Confluence › Upstream §10, critérios 10 a 14 |
| R7.2 | Confluence › Upstream §9: "O dashboard mostra o horário da última mensagem recebida." |
| R7.3 | Confluence › Upstream §7: "O dashboard deixa a pessoa mudar o limite de boa localização." |
| R7.4 | Confluence › Upstream §10, critério 4 |
| R8.1 | Confluence › Upstream §11: "Na primeira vez que liga, o produto traz tudo o que o GCN ainda guarda." |
| R8.2 | Confluence › Upstream §9: "Se o produto parar por falha, ao voltar ele continua de onde parou." |
| R8.3 | Confluence › Upstream §4: "O GCN pede que o cliente não seja disparado periodicamente por agendamento." |
| R8.4 | Q1.9: "sim"; Confluence › Upstream §9 (heartbeat mais de 5 minutos) |
| R8.5 | Q1.10: "A"; Confluence › Upstream §11 (25 dias desligado) |
| R8.6 | Confluence › Upstream §10, critérios 5 e 6 |
| R9.1 | Q1.3: "P1 e P2 no mesmo DEFINE, com prioridades"; Confluence › Upstream §10, critério 17 |
| R10.1 | Confluence › Upstream §7 (Coincidência multimensageiro) |
| R10.2 | Confluence › Upstream §7: "A coincidência só pelo tempo fica marcada como temporal." |
| R10.3 | Confluence › Upstream §7: "Evento retratado ou de teste fica fora da coincidência." |
| R11.1 | Confluence › Upstream §7 (Circulars por evento); Confluence › Downstream §5.5 |
| R11.2 | Confluence › Downstream §5.5 (Tempo até a primeira Circular) |

---

## Aprovação

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-11-09 | Versão inicial: Rodadas 1 e 2 respondidas, requisitos R1 a R11 |
