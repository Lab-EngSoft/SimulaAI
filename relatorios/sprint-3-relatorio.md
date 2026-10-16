# Relatório de Entrega — Sprint 3 — SimulaAI

**Período:** 03/10/2026 a 16/10/2026
**Sprint Review:** [data da apresentação — confirmar com o grupo]

## 1. Planejado vs. entregue

| História (backlog) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #7 Como aluno, quero receber uma explicação da IA quando errar | Sim | Sim | Serviço de explicação em duas camadas: IA compatível com OpenAI (`AI_API_KEY`/`AI_BASE_URL`/`AI_MODEL`) com **fallback determinístico** usando os dados do banco. Explicação gerada para 100% dos erros na finalização e consultável em `GET /tentativas/{id}/explicacoes`. A correção objetiva segue independente da IA (regra da #6) |
| #8 Como aluno, quero consultar meu histórico de tentativas | Sim | Sim | `GET /tentativas` + `GET /tentativas/{id}` consolidados: tentativas de **diferentes simulados** com acertos, erros, percentual e status, associadas ao aluno autenticado (nada vaza para outro aluno) |
| #9 Como aluno, quero visualizar um dashboard do meu desempenho | Sim | Sim | `GET /dashboard`: total de tentativas, tentativas finalizadas, acertos, erros, média de aproveitamento, desempenho **por matéria** e **por assunto** — agregação com JOIN de 4 tabelas e GROUP BY no banco (requisito mínimo do Manual §3) |
| #4–#6 (Sprint 2) e #1–#3 (Sprint 1) | — | Mantidas | Suíte de regressão continua 100% aprovada |

## 2. Incremento funcional demonstrável

A camada de **estudo** do SimulaAI: depois de finalizar um simulado, o aluno recebe explicação de cada erro e acompanha o desempenho agregado.

- **Explicação do tutor (história #7):** ao finalizar, cada resposta errada recebe explicação. Com `AI_API_KEY` configurada o texto vem do provedor de IA; sem chave (ou com a IA fora do ar) o fallback gera a explicação a partir do enunciado, da alternativa correta, da escolhida e do assunto — o endpoint nunca falha por indisponibilidade externa.
- **Histórico (história #8):** lista das tentativas por simulado com resultados registrados pelo próprio sistema.
- **Dashboard (história #9):** média de aproveitamento e ranking de matérias/assuntos onde o aluno erra mais — insumo direto para o objetivo do produto ("identificar pontos fortes e dificuldades").
- **CI (GitHub Actions):** workflow `testes` roda o pytest a cada push/PR para a main — evidência de execução com link de run.

**Como reproduzir:** ver `README.md`. Roteiro rápido: login como `ana.aluno@simulaai.app` → iniciar/responder/finalizar uma tentativa → `GET /tentativas/{id}/explicacoes` → `GET /dashboard`. Para testar o modo IA: definir `AI_API_KEY` (opcional `AI_BASE_URL` e `AI_MODEL`) e refazer uma tentativa. Documentação interativa em `http://localhost:8000/docs`.

## 3. Backlog atualizado

- #7, #8, #9 — **concluídas** nesta sprint.
- #10 (evolução entre tentativas), #11 (deploy público e integração frontend↔backend) — Sprint 4.

## 4. Evidências de teste

CT09–CT12 do plano de testes (`docs/plano-de-testes.md`) implementados como testes automatizados pytest — **5 testes novos; suíte total: 36 testes, 100% aprovados** na execução local de 03/10/2026; o CT08 foi atualizado para a realidade da Sprint 3 (a correção continua funcionando sem IA e o erro sai com a explicação do fallback). Detalhe em `relatorios/sprint-3-evidencias-teste.md`.

## 5. Retrospectiva e contribuição individual

- Ata de retrospectiva: `relatorios/sprint-3-retrospectiva.md`
- Relatórios individuais: `relatorios/sprint-3-contribuicao-{gabriel,davi,vinicius,cesar}.md` *(cada integrante preenche o seu)*

## 6. Riscos/impedimentos para a próxima sprint

- **Integração frontend↔backend:** é o item central da Sprint 4 (história #11) — as telas React ainda consomem dados em memória; contrato disponível no Swagger (`/docs`).
- **Deploy público:** planejar Render/Railway + Vercel (ou backend servindo o build do frontend) e banco PostgreSQL/Supabase via `DATABASE_URL`.
- **Chave de IA em produção:** cadastrar `AI_API_KEY` como segredo do provedor de deploy; sem ela o sistema continua funcional (fallback).
- **Evolução entre tentativas (#10):** o histórico já persiste os dados necessários; a comparação entra na Sprint 4.
