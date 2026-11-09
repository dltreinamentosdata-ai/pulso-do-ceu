# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Genie Code

# COMMAND ----------

# MAGIC %sh cd /tmp && PYTHONPATH=/Workspace/Users/dltreinamentos.data@gmail.com/sdd-gates/gates python3 -m sdd_gates --version
# MAGIC

# COMMAND ----------

# MAGIC %sh cd /tmp && PYTHONPATH=/Workspace/Users/dltreinamentos.data@gmail.com/sdd-gates/gates python3 -m sdd_gates selftest

# COMMAND ----------

# DBTITLE 1,Leitura das páginas Confluence — Pulso do Céu
# MAGIC %md
# MAGIC ## Leitura das páginas Confluence confirmada
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Upstream — Pulso do Céu (v5 · 08/11/2026 · Status: Pronto para o Define)
# MAGIC
# MAGIC **Contexto e problema**
# MAGIC O NASA GCN distribui alertas de eventos astronômicos transientes em tempo real via Kafka (explosões de raios gama, ondas gravitacionais, neutrinos, FRBs etc.), com 15+ missões e 20+ schemas em formatos heterogêneos. Não existe hoje uma visão unificada de "o que está acontecendo no céu agora" nem correlação entre instrumentos.
# MAGIC
# MAGIC **Objetivo**
# MAGIC Entregar uma visão unificada e confiável dos alertas do GCN, atualizada em até 5 minutos, consultável via dashboard ou linguagem natural (Genie Space).
# MAGIC
# MAGIC **Fontes de dados**
# MAGIC - GCN Kafka: notices em JSON (Unified Schema), LVK JSON próprio, VOEvent XML (Classic/SVOM) e Circulars JSON
# MAGIC - Arquivo histórico de Circulars (~46 mil desde 1997, baixado 1x/dia)
# MAGIC - Heartbeat (gcn.heartbeat, ~1 msg/s, apenas para saúde operacional)
# MAGIC
# MAGIC **Entregas**
# MAGIC - P1: histórico bruto, visão unificada de eventos, visão de Circulars, quarentena, controle de acesso com máscara de email, métricas 1 a 4 e dashboard
# MAGIC - P2: Genie Space e métricas de coincidência multiinstrumento e resposta da comunidade
# MAGIC
# MAGIC **Acesso e PII**
# MAGIC - Credencial GCN (client ID + secret) gerenciada em secrets; desativa após 30 dias sem uso
# MAGIC - Email de autores das Circulars é PII, mascarado para todos exceto pulso-ceu-admins
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Downstream — Pulso do Céu (v2 · 08/11/2026 · Aguardando aprovação do engenheiro)
# MAGIC
# MAGIC **Levantamento técnico**
# MAGIC Documento produzido pela engenharia a partir do upstream; registra fatos verificados e o mapeamento de dados decidido (colunas D1 a D12). Arquitetura (ingestão, compute, camadas, deploy) será decidida no ADR.
# MAGIC
# MAGIC **Conexão com a fonte**
# MAGIC - Brokers: kafka.gcn.nasa.gov e 3 brokers alternativos, porta 9092
# MAGIC - Autenticação: SASL_SSL + OAUTHBEARER (OIDC client credentials), token via auth.gcn.nasa.gov
# MAGIC - Restricao critica: o conector Kafka do Lakeflow Connect nao suporta OAuth M2M, que é a unica autenticacao aceita pelo GCN. A documentacao do Azure Databricks confirma que OAuth com client ID/secret nao funciona em pipelines Lakeflow com Unity Catalog. A arquitetura de ingestao precisara de solucao alternativa a definir no ADR.
# MAGIC
# MAGIC **Inventário de tópicos (situação 07/11/2026)**
# MAGIC - JSON ativo: IGWN/LVK (entre corridas, IR1 prevista para fim de 2026), IceCube, Einstein Probe, CHIME (em upgrade), DSA-110, MAXI, BOOM, Super-K
# MAGIC - VOEvent ativo: SVOM, Fermi GBM (principal fonte de GRB), Fermi LAT, GECAM, CALET, Konus-Wind
# MAGIC - Swift encerrado em 20/10/2026 (volume zero)
# MAGIC - Circulars: ~8/dia; heartbeat: ~86.400/dia
# MAGIC
# MAGIC **Mapeamento de dados**
# MAGIC - Schema JSON do GCN é permissivo: campos como mission, messenger, alert_type, alert_datetime frequentemente ausentes
# MAGIC - Regras D1 a D12 decidem de onde sai cada coluna e o comportamento quando o campo nao vem
# MAGIC - Nenhuma mensagem real foi lida ainda; sondagem ao vivo agendada antes do Build (secao 8 do Downstream)