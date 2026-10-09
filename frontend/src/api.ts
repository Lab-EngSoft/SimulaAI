/** Cliente HTTP único da API FastAPI. No desenvolvimento, /api passa pelo proxy do Vite. */
const API_BASE = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')
const STORAGE_KEY = 'simulaai_access_token'

export type Usuario = { id: number; nome: string; email: string; perfil: 'ALUNO' | 'ADMINISTRADOR' }
export type LoginResponse = { access_token: string; token_type: string; usuario: Usuario }
export type Materia = { id: number; nome: string; descricao: string | null }
export type Assunto = { id: number; materia_id: number; nome: string; descricao: string | null }
export type Alternativa = { id: number; texto: string; correta: boolean }
export type AlternativaInput = { texto: string; correta: boolean }
export type Questao = { id: number; assunto_id: number; enunciado: string; nivel_dificuldade: string | null; alternativas: Alternativa[] }
export type QuestaoInput = { assunto_id: number; enunciado: string; nivel_dificuldade: string | null; alternativas: AlternativaInput[] }
export type Simulado = { id: number; titulo: string; descricao: string | null; total_questoes: number }
export type SimuladoInput = { titulo: string; descricao: string | null; questao_ids: number[] }
export type SimuladoDetalhe = Simulado & { questao_ids: number[]; total_tentativas: number }
export type IAStatus = { disponivel: boolean; descricao: string }
export type Tentativa = { id: number; usuario_id: number; simulado_id: number; status: 'EM_ANDAMENTO' | 'FINALIZADO'; data_inicio: string; data_fim: string | null; acertos: number; erros: number; percentual_aproveitamento: number }
export type QuestaoJogo = { id: number; enunciado: string; nivel_dificuldade: string | null; alternativas: { id: number; texto: string }[]; respondida_alternativa_id: number | null }
export type Resultado = { tentativa: Tentativa; respostas: { questao_id: number; alternativa_id: number; correta: boolean; explicacao_ia: string | null }[] }

export class ApiError extends Error {
  readonly status: number
  constructor(status: number, message: string) { super(message); this.status = status; this.name = 'ApiError' }
}

export const sessao = {
  getToken: () => sessionStorage.getItem(STORAGE_KEY),
  setToken: (token: string) => sessionStorage.setItem(STORAGE_KEY, token),
  clear: () => sessionStorage.removeItem(STORAGE_KEY),
}

async function request<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${path}`, {
      method,
      headers: {
        ...(body === undefined ? {} : { 'Content-Type': 'application/json' }),
        ...(sessao.getToken() ? { Authorization: `Bearer ${sessao.getToken()}` } : {}),
      },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    })
  } catch {
    throw new ApiError(0, 'Não foi possível conectar ao backend. Verifique se o FastAPI está ativo na porta 8000.')
  }
  if (!response.ok) {
    const data: { detail?: string | { msg?: string }[] } = await response.json().catch(() => ({}))
    const detail = Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join('; ') : data.detail
    throw new ApiError(response.status, detail || `Erro HTTP ${response.status}`)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export const api = {
  login: (email: string, senha: string) => request<LoginResponse>('/auth/login', 'POST', { email, senha }),
  register: (nome: string, email: string, senha: string) => request<Usuario>('/auth/register', 'POST', { nome, email, senha }),
  me: () => request<Usuario>('/auth/me'),
  materias: () => request<Materia[]>('/materias'),
  criarMateria: (data: Pick<Materia, 'nome' | 'descricao'>) => request<Materia>('/materias', 'POST', data),
  editarMateria: (id: number, data: Pick<Materia, 'nome' | 'descricao'>) => request<Materia>(`/materias/${id}`, 'PUT', data),
  excluirMateria: (id: number) => request<void>(`/materias/${id}`, 'DELETE'),
  assuntos: () => request<Assunto[]>('/assuntos'),
  criarAssunto: (data: Omit<Assunto, 'id'>) => request<Assunto>('/assuntos', 'POST', data),
  editarAssunto: (id: number, data: Omit<Assunto, 'id'>) => request<Assunto>(`/assuntos/${id}`, 'PUT', data),
  excluirAssunto: (id: number) => request<void>(`/assuntos/${id}`, 'DELETE'),
  questoes: () => request<Questao[]>('/questoes'),
  criarQuestao: (data: QuestaoInput) => request<Questao>('/questoes', 'POST', data),
  editarQuestao: (id: number, data: QuestaoInput) => request<Questao>(`/questoes/${id}`, 'PUT', data),
  excluirQuestao: (id: number) => request<void>(`/questoes/${id}`, 'DELETE'),
  simulados: () => request<Simulado[]>('/simulados'),
  simulado: (id: number) => request<SimuladoDetalhe>(`/simulados/${id}`),
  criarSimulado: (data: SimuladoInput) => request<SimuladoDetalhe>('/simulados', 'POST', data),
  editarSimulado: (id: number, data: SimuladoInput) => request<SimuladoDetalhe>(`/simulados/${id}`, 'PUT', data),
  excluirSimulado: (id: number) => request<void>(`/simulados/${id}`, 'DELETE'),
  iaStatus: () => request<IAStatus>('/tentativas/ia/status'),
  resultado: (id: number) => request<Resultado>(`/tentativas/${id}/resultado`),
  gerarExplicacoes: (id: number) => request<Resultado>(`/tentativas/${id}/explicacoes`, 'POST'),
  tentativas: () => request<Tentativa[]>('/tentativas'),
  iniciar: (simulado_id: number) => request<Tentativa>('/tentativas', 'POST', { simulado_id }),
  questoesDaTentativa: (id: number) => request<QuestaoJogo[]>(`/tentativas/${id}/questoes`),
  responder: (id: number, questao_id: number, alternativa_id: number) => request<Tentativa>(`/tentativas/${id}/respostas`, 'POST', { questao_id, alternativa_id }),
  finalizar: (id: number) => request<Resultado>(`/tentativas/${id}/finalizar`, 'POST'),
}
