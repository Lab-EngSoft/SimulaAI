
import {
  BookOpen,
  ChartNoAxesColumnIncreasing,
  CheckCircle2,
  ClipboardList,
  Target,
  TrendingUp,
  XCircle,
} from 'lucide-react'

import type {
  Dashboard,
  DesempenhoRotulo,
  Simulado,
  Tentativa,
} from './api'

import './StudentDashboard.css'

type Props = {
  dados: Dashboard
  historico: Tentativa[]
  simulados: Simulado[]
}

function porcentagem(valor: number): string {
  return `${valor.toLocaleString('pt-BR', {
    maximumFractionDigits: 1,
  })}%`
}

function DesempenhoLista({
  titulo,
  dados,
  vazio,
}: {
  titulo: string
  dados: DesempenhoRotulo[]
  vazio: string
}) {
  const ordenados = [...dados].sort(
    (a, b) =>
      a.percentual - b.percentual ||
      a.rotulo.localeCompare(b.rotulo, 'pt-BR'),
  )

  return (
    <article className="panel student-dashboard-panel">
      <div className="student-dashboard-panel-title">
        <h3>{titulo}</h3>
        <span>{dados.length} categorias</span>
      </div>

      {ordenados.length === 0 ? (
        <p className="student-dashboard-empty">{vazio}</p>
      ) : (
        <div className="student-dashboard-bars">
          {ordenados.map((item) => (
            <div className="student-dashboard-bar-row" key={item.rotulo}>
              <div className="student-dashboard-bar-label">
                <strong>{item.rotulo}</strong>
                <span>
                  {item.acertos} de {item.respondidas} corretas ·{' '}
                  {porcentagem(item.percentual)}
                </span>
              </div>

              <div
                className="student-dashboard-track"
                role="progressbar"
                aria-label={`Aproveitamento em ${item.rotulo}`}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-valuenow={item.percentual}
              >
                <div
                  className={
                    item.percentual < 60
                      ? 'student-dashboard-fill is-low'
                      : 'student-dashboard-fill'
                  }
                  style={{
                    width: `${Math.max(
                      0,
                      Math.min(100, item.percentual),
                    )}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </article>
  )
}

export default function StudentDashboard({
  dados,
  historico,
  simulados,
}: Props) {
  const finalizadas = historico
    .filter((t) => t.status === 'FINALIZADO')
    .sort(
      (a, b) =>
        new Date(a.data_fim ?? a.data_inicio).getTime() -
          new Date(b.data_fim ?? b.data_inicio).getTime() ||
        a.id - b.id,
    )

  const recentes = finalizadas.slice(-8)
  const semDados = dados.tentativas_finalizadas === 0

  const assuntosRevisar = [...dados.por_assunto]
    .filter((item) => item.respondidas > 0 && item.percentual < 70)
    .sort(
      (a, b) =>
        a.percentual - b.percentual ||
        b.respondidas - a.respondidas,
    )
    .slice(0, 3)

  return (
    <div className="student-dashboard">
      <div className="student-dashboard-metrics">
        <article className="student-dashboard-metric">
          <ClipboardList size={21} />
          <span>Simulados concluídos</span>
          <strong>{dados.tentativas_finalizadas}</strong>
          <small>{dados.total_tentativas} tentativas iniciadas</small>
        </article>

        <article className="student-dashboard-metric">
          <Target size={21} />
          <span>Média de aproveitamento</span>
          <strong>{porcentagem(dados.media_aproveitamento)}</strong>
          <small>Média das tentativas concluídas</small>
        </article>

        <article className="student-dashboard-metric">
          <CheckCircle2 size={21} />
          <span>Acertos</span>
          <strong>{dados.total_acertos}</strong>
          <small>Nas tentativas concluídas</small>
        </article>

        <article className="student-dashboard-metric">
          <XCircle size={21} />
          <span>Erros</span>
          <strong>{dados.total_erros}</strong>
          <small>Nas tentativas concluídas</small>
        </article>
      </div>

      {semDados ? (
        <div className="panel student-dashboard-welcome">
          <BookOpen size={30} />
          <h3>Seu desempenho começa com um simulado</h3>
          <p>
            Conclua uma avaliação para visualizar seus resultados
            por matéria, assunto e sua evolução.
          </p>
        </div>
      ) : (
        <>
          <div className="student-dashboard-columns">
            <DesempenhoLista
              titulo="Desempenho por matéria"
              dados={dados.por_materia}
              vazio="Ainda não há respostas por matéria."
            />

            <DesempenhoLista
              titulo="Desempenho por assunto"
              dados={dados.por_assunto}
              vazio="Ainda não há respostas por assunto."
            />
          </div>

          <article className="panel student-dashboard-panel">
            <div className="student-dashboard-panel-title">
              <div>
                <h3>
                  <TrendingUp size={18} />
                  Evolução entre tentativas
                </h3>
                <p>Últimas oito tentativas concluídas.</p>
              </div>
              <ChartNoAxesColumnIncreasing size={22} />
            </div>

            <div
              className="student-dashboard-trend"
              role="list"
              aria-label="Aproveitamento das tentativas concluídas"
            >
              {recentes.map((tentativa, index) => {
                const titulo =
                  simulados.find(
                    (s) => s.id === tentativa.simulado_id,
                  )?.titulo ?? `Simulado #${tentativa.simulado_id}`

                const nota = Math.max(
                  0,
                  Math.min(100, tentativa.percentual_aproveitamento),
                )

                const data = new Date(
                  tentativa.data_fim ?? tentativa.data_inicio,
                )

                return (
                  <div
                    className="student-dashboard-trend-item"
                    role="listitem"
                    key={tentativa.id}
                    title={`${titulo} · ${porcentagem(nota)}`}
                  >
                    <strong>{porcentagem(nota)}</strong>

                    <div className="student-dashboard-trend-track">
                      <div
                        className="student-dashboard-trend-fill"
                        style={{ height: `${nota}%` }}
                      />
                    </div>

                    <span>
                      T{finalizadas.length - recentes.length + index + 1}
                    </span>

                    <small>
                      {data.toLocaleDateString('pt-BR')}
                    </small>
                  </div>
                )
              })}
            </div>

            <p className="student-dashboard-footnote">
              Cada barra representa uma tentativa. Os resultados
              podem variar conforme as questões e a dificuldade.
            </p>
          </article>

          {assuntosRevisar.length > 0 && (
            <article className="panel student-dashboard-panel student-dashboard-review">
              <h3>
                <BookOpen size={18} />
                Assuntos para revisar
              </h3>

              <p>
                Conteúdos com aproveitamento abaixo de 70%
                nas questões respondidas.
              </p>

              <ul>
                {assuntosRevisar.map((item) => (
                  <li key={item.rotulo}>
                    <strong>{item.rotulo}</strong>
                    <span>
                      {porcentagem(item.percentual)} ·{' '}
                      {item.respondidas} respostas
                    </span>
                  </li>
                ))}
              </ul>
            </article>
          )}
        </>
      )}

      <p className="student-dashboard-footnote">
        Os percentuais por matéria e assunto consideram as questões
        respondidas nas tentativas concluídas. Questões em branco
        não entram nesses agrupamentos.
      </p>
    </div>
  )
}
