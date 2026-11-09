# SDD STATE: Pulso do Céu

> Ledger de rastreabilidade da feature — **fonte única da verdade** do fluxo SDD.
> Criado na fase Define, atualizado ao final de cada fase, arquivado no Ship.
> Localização: `.sdd/features/PULSO_DO_CEU/state.md`

## Identidade

| Atributo | Valor |
|----------|-------|
| **Feature** | PULSO_DO_CEU |
| **Tamanho** | Complexo (confirmado em Q1.1) — domínio novo, Kafka externo com OAuth, vários formatos, PII com máscara, decisão de ingestão em aberto |
| **Jira Key** | KAN-1 |
| **Confluence URL** | Upstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/360450 ; Downstream: https://dltreinamentos-aidata-544385d7.atlassian.net/wiki/spaces/~71202015da5781da3d47a0badd62f9232c15e4/pages/557058 |
| **Gates** | `/Workspace/Users/dltreinamentos.data@gmail.com/sdd-gates/gates` — versão 0.4.0 (conferida em 2026-11-09: `sdd_gates 0.4.0`) |
| **Branch** | `feat/pulso-do-ceu` (criada a partir da `main` em 2026-11-09) |
| **Fase Atual** | Define |
| **Criado em** | 2026-11-09 |
| **Atualizado em** | 2026-11-09 |

---

## Aprovações

| Etapa | Versão | Aprovado em | Palavras do usuário |
|-------|--------|-------------|---------------------|
| Spec (Define) | — | — | pendente |
| Plano de tarefas (PO) | — | — | pendente |

---

## Status das Fases

| Fase | Status | Artefato | Gate | Concluída em |
|------|--------|----------|------|--------------|
| Define | aguardando aprovação da spec (Rodadas 1 e 2 respondidas) | `docs/specs/DEFINE_PULSO_DO_CEU.md` v1.0 | `sdd_gates define DEFINE_PULSO_DO_CEU.md: OK — 0 aviso(s)` (sem `--aprovado`) | — |
| ADR | pendente | `docs/adr/ADR_PULSO_DO_CEU.md` | — | — |
| Planejamento (PO) | pendente | `docs/planning/TASKS_PULSO_DO_CEU.md` | — | — |
| Design | pendente | `docs/designs/DESIGN_PULSO_DO_CEU.md` | — | — |
| Build | pendente | `.sdd/features/PULSO_DO_CEU/BUILD_REPORT.md` | — | — |
| Ship | pendente | `.sdd/archive/PULSO_DO_CEU/` | — | — |

---

## Log de Ações no Jira

| Fase | Comentário | Transição | Quando |
|------|------------|-----------|--------|
| Define | pendente | To Do → Em andamento | — |
| ADR | pendente | (mantém Em andamento) | — |
| Planejamento (PO) | pendente | (mantém Em andamento) | — |
| Design | pendente | (mantém Em andamento) | — |
| Build | pendente | Em andamento → Em revisão | — |
| Ship | pendente | Em revisão → Concluído | — |

---

## Histórico de Revisões

| Versão | Data | Fase | Mudança |
|--------|------|------|---------|
| 1.0 | 2026-11-09 | Define | State criado |
| 1.1 | 2026-11-09 | Define | Tamanho confirmado (Q1.1); Downstream v2 aprovado pelo usuário (Q1.2: "sim, aprovo o downstream v2 como está"); DEFINE v1.0 escrito; gate rodado |
| 1.2 | 2026-11-09 | Define | Rodada 2 respondida (Q2.1 A, Q2.2 sim, Q2.3 B com N = 5); gate OK com 0 aviso; aguardando aprovação |
