import { useCallback, useEffect, useMemo, useState } from 'react'
import type { FormEvent, ReactNode } from 'react'
import { ArrowLeft, BookOpen, Check, ChevronRight, ClipboardList, Edit3, GraduationCap, LayoutDashboard, LibraryBig, LogOut, Menu, Plus, Search, ShieldCheck, Trash2, X, ArrowUp, ArrowDown, Sparkles } from 'lucide-react'
import { api, ApiError, sessao } from './api'
import type { Assunto, Materia, Questao, QuestaoInput, QuestaoJogo, Resultado, Simulado, SimuladoDetalhe, SimuladoInput, IAStatus, Tentativa, Usuario } from './api'
import './App.css'

type AdminScreen = 'admin-dashboard' | 'subjects' | 'questions' | 'simulados'
type Notify = (message: string) => void
type Perform = (task: () => Promise<unknown>, success: string) => Promise<boolean>

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'Não foi possível concluir a operação.'
}

function App() {
  const [user, setUser] = useState<Usuario | null>(null)
  const [checking, setChecking] = useState(true)
  const [screen, setScreen] = useState<AdminScreen>('admin-dashboard')
  const [subjects, setSubjects] = useState<Materia[]>([])
  const [topics, setTopics] = useState<Assunto[]>([])
  const [questions, setQuestions] = useState<Questao[]>([])
  const [simulados, setSimulados] = useState<Simulado[]>([])
  const [loadingContent, setLoadingContent] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [notice, setNotice] = useState('')
  const [error, setError] = useState('')

  const flash: Notify = (message) => setNotice(message)
  const logout = () => { sessao.clear(); setUser(null); setNotice(''); setError(''); setSidebarOpen(false) }

  const loadContent = useCallback(async () => {
    setLoadingContent(true)
    try {
      const [materias, assuntos, questoes, listaSimulados] = await Promise.all([api.materias(), api.assuntos(), api.questoes(), api.simulados()])
      setSubjects(materias)
      setTopics(assuntos)
      setQuestions(questoes)
      setSimulados(listaSimulados)
      setError('')
    } finally { setLoadingContent(false) }
  }, [])

  useEffect(() => {
    let active = true
    const restore = async () => {
      if (!sessao.getToken()) { if (active) setChecking(false); return }
      try {
        const validatedUser = await api.me()
        if (active) setUser(validatedUser)
      } catch (err) {
        if (err instanceof ApiError && err.status === 401) sessao.clear()
        if (active) setError(errorMessage(err))
      } finally { if (active) setChecking(false) }
    }
    void restore()
    return () => { active = false }
  }, [])

  useEffect(() => {
    if (user?.perfil !== 'ADMINISTRADOR') return
    void loadContent().catch((err: unknown) => {
      if (err instanceof ApiError && err.status === 401) logout()
      else setError(errorMessage(err))
    })
    // loadContent has stable identity; auth changes retrigger loading.
  }, [user?.id, user?.perfil, loadContent])

  const perform: Perform = async (task, success) => {
    setError('')
    try {
      await task()
      await loadContent()
      flash(success)
      return true
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) logout()
      else setError(errorMessage(err))
      return false
    }
  }

  if (checking) return <main className="startup-screen"><Brand /><p>Validando sua sessão...</p></main>
  if (!user) return <Login onEnter={(validated) => { setUser(validated); setError(''); setNotice('') }} />
  if (user.perfil === 'ALUNO') return <StudentArea user={user} onLogout={logout} />

  const pages: Record<AdminScreen, ReactNode> = {
    'admin-dashboard': <AdminDashboard user={user} subjects={subjects} topics={topics} questions={questions} simulados={simulados} goTo={setScreen} />,
    subjects: <SubjectsPage subjects={subjects} topics={topics} perform={perform} />,
    questions: <QuestionsPage subjects={subjects} topics={topics} questions={questions} perform={perform} />,
    simulados: <SimuladosPage subjects={subjects} topics={topics} questions={questions} simulados={simulados} perform={perform} onError={setError} />,
  }

  return <div className="app-shell">
    <Sidebar user={user} active={screen} onNavigate={(next) => { setScreen(next); setSidebarOpen(false) }} onLogout={logout} isOpen={sidebarOpen} />
    {sidebarOpen && <button className="backdrop" aria-label="Fechar menu" onClick={() => setSidebarOpen(false)} />}
    <main className="main-content">
      <Topbar onMenu={() => setSidebarOpen(true)} onLogout={logout} />
      <div className="page-content">
        {error && <div className="api-banner error" role="alert">{error} <button onClick={() => setError('')}>Fechar</button></div>}
        {loadingContent && <p className="content-loading" role="status">Sincronizando dados com a API...</p>}
        {pages[screen]}
      </div>
    </main>
    {notice && <div className="toast" role="status"><Check size={18} /> {notice}<button aria-label="Fechar aviso" onClick={() => setNotice('')}><X size={16}/></button></div>}
  </div>
}

function Brand() { return <div className="brand"><div className="brand-mark"><GraduationCap size={23} /></div><span>Simula<span>AI</span></span></div> }

function Login({ onEnter }: { onEnter: (user: Usuario) => void }) {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    if (!email.trim() || !password.trim() || (mode === 'register' && !name.trim())) {
      setError('Preencha os campos obrigatórios.')
      return
    }
    setBusy(true)
    try {
      if (mode === 'register') await api.register(name.trim(), email.trim(), password)
      const session = await api.login(email.trim(), password)
      sessao.setToken(session.access_token)
      onEnter(session.usuario) // a API define o perfil; o navegador nunca promove aluno a administrador.
    } catch (err) { setError(errorMessage(err)) }
    finally { setBusy(false) }
  }

  return <main className="login-page">
    <section className="login-hero"><Brand /><div><span className="eyebrow light">PLATAFORMA DE ESTUDOS</span><h1>Prepare-se para<br/>o seu próximo desafio.</h1><p>Faça simulados, acompanhe resultados e transforme seus erros em aprendizado.</p></div><div className="login-benefits"><span><Check size={16}/> Simulados organizados por assunto</span><span><Check size={16}/> Análise clara do seu desempenho</span><span><Check size={16}/> Correção automática</span></div></section>
    <section className="login-panel"><form className="login-card" onSubmit={(event) => void submit(event)}>
      <div><span className="eyebrow">BEM-VINDO</span><h2>{mode === 'login' ? 'Acesse sua conta' : 'Crie sua conta de aluno'}</h2><p>{mode === 'login' ? 'A autenticação é validada pelo servidor.' : 'O cadastro público cria somente contas do tipo Aluno.'}</p></div>
      {mode === 'register' && <label>Nome completo<input value={name} onChange={(e) => setName(e.target.value)} minLength={2} maxLength={150} autoComplete="name" required /></label>}
      <label>E-mail<input value={email} onChange={(e) => setEmail(e.target.value)} type="email" autoComplete="email" placeholder="voce@email.com" required /></label>
      <label>Senha<input value={password} onChange={(e) => setPassword(e.target.value)} type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'} minLength={8} placeholder="Mínimo de 8 caracteres" required /></label>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button disabled={busy} className="button primary full" type="submit">{busy ? 'Conectando...' : mode === 'login' ? 'Entrar' : 'Criar conta'} <ChevronRight size={18}/></button>
      <button className="auth-link" type="button" onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}>{mode === 'login' ? 'Não tem conta? Cadastre-se como aluno' : 'Já tem uma conta? Entrar'}</button>
      {import.meta.env.DEV && <p className="demo-hint">Teste local — Admin: carlos.admin@simulaai.app / admin123<br/>Aluno: ana.aluno@simulaai.app / aluno123</p>}
    </form></section>
  </main>
}

function Sidebar({ user, active, onNavigate, onLogout, isOpen }: { user: Usuario; active: AdminScreen; onNavigate: (screen: AdminScreen) => void; onLogout: () => void; isOpen: boolean }) {
  const items: { screen: AdminScreen; label: string; icon: ReactNode }[] = [
    { screen: 'admin-dashboard', label: 'Visão geral', icon: <LayoutDashboard size={19}/> },
    { screen: 'subjects', label: 'Matérias e assuntos', icon: <LibraryBig size={19}/> },
    { screen: 'questions', label: 'Questões', icon: <ClipboardList size={19}/> },
    { screen: 'simulados', label: 'Simulados', icon: <GraduationCap size={19}/> },
  ]
  return <aside className={`sidebar ${isOpen ? 'open' : ''}`}><div><Brand/><p className="sidebar-role"><ShieldCheck size={15}/> Área administrativa</p></div><nav>{items.map((item) => <button key={item.screen} onClick={() => onNavigate(item.screen)} className={active === item.screen ? 'active' : ''}>{item.icon}{item.label}</button>)}</nav><div className="sidebar-footer"><div className="user-mini"><span className="avatar">AD</span><span><strong>{user.nome}</strong><small>Administrador</small></span></div><button className="logout" onClick={onLogout}><LogOut size={18}/> Sair</button></div></aside>
}
function Topbar({ onMenu, onLogout }: { onMenu: () => void; onLogout: () => void }) { return <header className="topbar"><button className="menu-button" onClick={onMenu} aria-label="Abrir menu"><Menu size={22}/></button><div className="breadcrumb">Administração <ChevronRight size={16}/> <strong>SimulaAI</strong></div><button className="mobile-logout" onClick={onLogout}><LogOut size={18}/></button></header> }

function AdminDashboard({ user, subjects, topics, questions, simulados, goTo }: { user: Usuario; subjects: Materia[]; topics: Assunto[]; questions: Questao[]; simulados: Simulado[]; goTo: (screen: AdminScreen) => void }) {
  return <>
    <section className="page-heading"><div><span className="eyebrow">PAINEL ADMINISTRATIVO</span><h1>Olá, {user.nome.split(' ')[0]}</h1><p>Gerencie os conteúdos armazenados no SimulaAI.</p></div><span className="date-label">Dados sincronizados com a API</span></section>
    <section className="metric-grid"><Metric icon={<BookOpen/>} number={subjects.length} label="Matérias cadastradas" tone="blue"/><Metric icon={<LibraryBig/>} number={topics.length} label="Assuntos organizados" tone="purple"/><Metric icon={<ClipboardList/>} number={questions.length} label="Questões cadastradas" tone="green"/><Metric icon={<GraduationCap/>} number={simulados.length} label="Simulados" tone="purple"/></section>
    <section className="action-panel"><div><h2>Gerencie o banco de questões</h2><p>As alterações são salvas no banco de dados do backend.</p></div><div className="action-buttons"><button className="button secondary" onClick={() => goTo('subjects')}><LibraryBig size={18}/> Gerenciar conteúdos</button><button className="button primary" onClick={() => goTo('simulados')}><Plus size={18}/> Criar simulados</button></div></section>
    <section className="dashboard-columns"><article className="panel"><div className="panel-header"><div><h2>Matérias cadastradas</h2><p>Base de organização dos simulados.</p></div><button className="text-button" onClick={() => goTo('subjects')}>Ver todas <ChevronRight size={16}/></button></div><div className="subject-list">{subjects.map((subject) => <div className="subject-row" key={subject.id}><span className="subject-icon"><BookOpen size={18}/></span><span><strong>{subject.nome}</strong><small>{topics.filter((topic) => topic.materia_id === subject.id).length} assuntos</small></span><ChevronRight size={18}/></div>)}</div></article><article className="panel"><div className="panel-header"><div><h2>Fluxo integrado</h2><p>Administração e estudos</p></div></div><ol className="steps"><li className="complete"><span><Check size={15}/></span><div><strong>Autenticação real</strong><small>JWT e permissões no backend.</small></div></li><li className="complete"><span><Check size={15}/></span><div><strong>Conteúdo persistente</strong><small>Matérias, assuntos e questões.</small></div></li><li className="complete"><span><Check size={15}/></span><div><strong>Simulados administráveis</strong><small>Seleção e ordenação das questões, respostas e correção.</small></div></li></ol></article></section>
  </>
}
function Metric({ icon, number, label, tone }: { icon: ReactNode; number: number; label: string; tone: string }) { return <article className={`metric-card ${tone}`}><span className="metric-icon">{icon}</span><div><strong>{number}</strong><span>{label}</span></div></article> }

function SubjectsPage({ subjects, topics, perform }: { subjects: Materia[]; topics: Assunto[]; perform: Perform }) {
  const [subjectModal, setSubjectModal] = useState(false)
  const [topicModal, setTopicModal] = useState(false)
  const [editingSubject, setEditingSubject] = useState<Materia | null>(null)
  const [editingTopic, setEditingTopic] = useState<Assunto | null>(null)
  const deleteSubject = (s: Materia) => { if (window.confirm(`Excluir “${s.nome}” e todos os seus assuntos e questões?`)) void perform(() => api.excluirMateria(s.id), 'Matéria excluída.') }
  const deleteTopic = (t: Assunto) => { if (window.confirm(`Excluir “${t.nome}” e suas questões?`)) void perform(() => api.excluirAssunto(t.id), 'Assunto excluído.') }
  return <>
    <section className="page-heading"><div><span className="eyebrow">ORGANIZAÇÃO DO CONTEÚDO</span><h1>Matérias e assuntos</h1><p>Organize as questões pelo conteúdo acadêmico.</p></div><div className="heading-actions"><button className="button secondary" disabled={!subjects.length} onClick={() => { setEditingTopic(null); setTopicModal(true) }}><Plus size={18}/> Novo assunto</button><button className="button primary" onClick={() => { setEditingSubject(null); setSubjectModal(true) }}><Plus size={18}/> Nova matéria</button></div></section>
    <section className="content-grid two"><article className="panel"><div className="panel-header"><div><h2>Matérias</h2><p>{subjects.length} cadastradas</p></div></div><div className="data-list">{subjects.map((s) => <div className="data-row" key={s.id}><div><strong>{s.nome}</strong><small>{s.descricao}</small></div><span className="count-badge">{topics.filter((t) => t.materia_id === s.id).length} assuntos</span><div className="row-actions"><button aria-label={`Editar ${s.nome}`} onClick={() => { setEditingSubject(s); setSubjectModal(true) }}><Edit3 size={16}/></button><button className="danger" aria-label={`Excluir ${s.nome}`} onClick={() => deleteSubject(s)}><Trash2 size={16}/></button></div></div>)}</div></article>
    <article className="panel"><div className="panel-header"><div><h2>Assuntos</h2><p>{topics.length} cadastrados</p></div></div><div className="data-list">{topics.map((t) => <div className="data-row compact" key={t.id}><div><strong>{t.nome}</strong><small>{subjects.find((s) => s.id === t.materia_id)?.nome ?? '—'}</small></div><div className="row-actions"><button aria-label={`Editar ${t.nome}`} onClick={() => { setEditingTopic(t); setTopicModal(true) }}><Edit3 size={16}/></button><button className="danger" aria-label={`Excluir ${t.nome}`} onClick={() => deleteTopic(t)}><Trash2 size={16}/></button></div></div>)}</div></article></section>
    {subjectModal && <SubjectModal subject={editingSubject} onClose={() => setSubjectModal(false)} onSave={async (data) => { const ok = await perform(() => editingSubject ? api.editarMateria(editingSubject.id, data) : api.criarMateria(data), editingSubject ? 'Matéria atualizada.' : 'Matéria cadastrada.'); if (ok) setSubjectModal(false) }}/>}
    {topicModal && <TopicModal topic={editingTopic} subjects={subjects} onClose={() => setTopicModal(false)} onSave={async (data) => { const ok = await perform(() => editingTopic ? api.editarAssunto(editingTopic.id, data) : api.criarAssunto(data), editingTopic ? 'Assunto atualizado.' : 'Assunto cadastrado.'); if (ok) setTopicModal(false) }}/>}
  </>
}

function QuestionsPage({ subjects, topics, questions, perform }: { subjects: Materia[]; topics: Assunto[]; questions: Questao[]; perform: Perform }) {
  const [modal, setModal] = useState(false)
  const [editing, setEditing] = useState<Questao | null>(null)
  const [search, setSearch] = useState('')
  const visible = useMemo(() => questions.filter((q) => q.enunciado.toLocaleLowerCase().includes(search.toLocaleLowerCase())), [questions, search])
  return <>
    <section className="page-heading"><div><span className="eyebrow">BANCO DE QUESTÕES</span><h1>Questões e alternativas</h1><p>Cadastre de 2 a 5 alternativas e indique a resposta correta.</p></div><button className="button primary" disabled={!topics.length} onClick={() => { setEditing(null); setModal(true) }}><Plus size={18}/> Nova questão</button></section>
    <section className="panel question-panel"><div className="table-toolbar"><div><h2>Questões cadastradas</h2><p>{questions.length} questões no banco</p></div><label className="search"><Search size={18}/><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Buscar por enunciado"/></label></div><div className="table-wrap"><table><thead><tr><th>Questão</th><th>Matéria</th><th>Assunto</th><th>Dificuldade</th><th aria-label="Ações"/></tr></thead><tbody>{visible.map((q) => { const topic = topics.find((t) => t.id === q.assunto_id); return <tr key={q.id}><td><strong>{q.enunciado}</strong><small>{q.alternativas.length} alternativas · correta: {String.fromCharCode(65 + q.alternativas.findIndex((a) => a.correta))}</small></td><td>{subjects.find((s) => s.id === topic?.materia_id)?.nome ?? '—'}</td><td>{topic?.nome ?? '—'}</td><td><span className="status active">{q.nivel_dificuldade ?? 'Não definida'}</span></td><td className="row-actions"><button aria-label="Editar questão" onClick={() => { setEditing(q); setModal(true) }}><Edit3 size={16}/></button><button className="danger" aria-label="Excluir questão" onClick={() => { if (window.confirm('Excluir esta questão?')) void perform(() => api.excluirQuestao(q.id), 'Questão excluída.') }}><Trash2 size={16}/></button></td></tr> })}{visible.length === 0 && <tr><td className="empty" colSpan={5}>Nenhuma questão encontrada.</td></tr>}</tbody></table></div></section>
    {modal && <QuestionModal question={editing} subjects={subjects} topics={topics} onClose={() => setModal(false)} onSave={async (data) => { const ok = await perform(() => editing ? api.editarQuestao(editing.id, data) : api.criarQuestao(data), editing ? 'Questão atualizada.' : 'Questão cadastrada.'); if (ok) setModal(false) }}/>}
  </>
}

function SimuladosPage({ subjects, topics, questions, simulados, perform, onError }: {
  subjects: Materia[]; topics: Assunto[]; questions: Questao[]; simulados: Simulado[];
  perform: Perform; onError: Notify
}) {
  const [modal, setModal] = useState(false)
  const [editing, setEditing] = useState<SimuladoDetalhe | null>(null)
  const [opening, setOpening] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const visible = useMemo(() => simulados.filter((s) => (s.titulo + ' ' + (s.descricao ?? '')).toLocaleLowerCase().includes(search.toLocaleLowerCase())), [simulados, search])
  const openEdit = async (simulado: Simulado) => {
    setOpening(simulado.id)
    try { setEditing(await api.simulado(simulado.id)); setModal(true) }
    catch (error) { onError(errorMessage(error)) }
    finally { setOpening(null) }
  }
  const remove = (simulado: Simulado) => {
    if (window.confirm(`Excluir “${simulado.titulo}”? Só é permitido quando não há tentativas de alunos.`)) {
      void perform(() => api.excluirSimulado(simulado.id), 'Simulado excluído.')
    }
  }
  return <>
    <section className="page-heading"><div><span className="eyebrow">ORGANIZAÇÃO DAS AVALIAÇÕES</span><h1>Simulados</h1><p>Monte avaliações com questões do banco e escolha a ordem de apresentação.</p></div><button className="button primary" disabled={!questions.length} onClick={() => { setEditing(null); setModal(true) }}><Plus size={18}/> Novo simulado</button></section>
    {!questions.length && <p className="api-banner">Cadastre ao menos uma questão antes de criar um simulado.</p>}
    <section className="panel question-panel"><div className="table-toolbar"><div><h2>Simulados cadastrados</h2><p>{simulados.length} simulado(s) no backend</p></div><label className="search"><Search size={18}/><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Buscar simulados" aria-label="Buscar simulados"/></label></div><div className="table-wrap"><table><thead><tr><th>Título</th><th>Descrição</th><th>Questões</th><th aria-label="Ações"/></tr></thead><tbody>{visible.map((simulado) => <tr key={simulado.id}><td><strong>{simulado.titulo}</strong></td><td>{simulado.descricao || '—'}</td><td>{simulado.total_questoes}</td><td className="row-actions"><button aria-label={`Editar simulado ${simulado.titulo}`} disabled={opening !== null} onClick={() => void openEdit(simulado)}><Edit3 size={16}/></button><button className="danger" aria-label={`Excluir simulado ${simulado.titulo}`} onClick={() => remove(simulado)}><Trash2 size={16}/></button></td></tr>)}{visible.length === 0 && <tr><td className="empty" colSpan={4}>Nenhum simulado encontrado.</td></tr>}</tbody></table></div></section>
    {modal && <SimuladoModal key={editing?.id ?? 'new'} simulado={editing} subjects={subjects} topics={topics} questions={questions} onClose={() => setModal(false)} onSave={async (data) => { const ok = await perform(() => editing ? api.editarSimulado(editing.id, data) : api.criarSimulado(data), editing ? 'Simulado atualizado.' : 'Simulado cadastrado e disponível para alunos.'); if (ok) setModal(false) }}/>} 
  </>
}

function SimuladoModal({ simulado, subjects, topics, questions, onClose, onSave }: {
  simulado: SimuladoDetalhe | null; subjects: Materia[]; topics: Assunto[]; questions: Questao[];
  onClose: () => void; onSave: (data: SimuladoInput) => Promise<void>
}) {
  const [title, setTitle] = useState(simulado?.titulo ?? '')
  const [description, setDescription] = useState(simulado?.descricao ?? '')
  const [selected, setSelected] = useState<number[]>(simulado?.questao_ids ?? [])
  const [subjectId, setSubjectId] = useState(0)
  const [topicId, setTopicId] = useState(0)
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const locked = Boolean(simulado?.total_tentativas)
  const available = questions.filter((q) => {
    const topic = topics.find((t) => t.id === q.assunto_id)
    return (!subjectId || topic?.materia_id === subjectId) && (!topicId || q.assunto_id === topicId) && q.enunciado.toLocaleLowerCase().includes(search.toLocaleLowerCase())
  })
  const choose = (id: number) => setSelected((ids) => ids.includes(id) ? ids.filter((value) => value !== id) : [...ids, id])
  const move = (index: number, direction: number) => {
    const next = [...selected]
    const other = index + direction
    if (other < 0 || other >= next.length) return
    ;[next[index], next[other]] = [next[other], next[index]]
    setSelected(next)
  }
  const submit = (event: FormEvent) => {
    event.preventDefault()
    if (title.trim().length < 3) { setError('O título precisa ter pelo menos 3 caracteres.'); return }
    if (!selected.length) { setError('Selecione ao menos uma questão.'); return }
    setBusy(true); setError('')
    void onSave({ titulo: title.trim(), descricao: description.trim() || null, questao_ids: selected }).finally(() => setBusy(false))
  }
  return <Modal title={simulado ? 'Editar simulado' : 'Novo simulado'} onClose={onClose}>
    <form className="modal-form simulado-form" onSubmit={submit}>
      <label>Título<input autoFocus required minLength={3} maxLength={150} value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Ex.: Revisão de matemática"/></label>
      <label>Descrição<textarea rows={2} value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Orientações para o aluno (opcional)"/></label>
      {locked && <p className="api-banner">Este simulado já possui {simulado?.total_tentativas} tentativa(s). Você pode editar o título e a descrição, mas não mudar as questões nem excluí-lo.</p>}
      <div className="simulado-builder"><div className="simulado-builder-title"><strong>Banco de questões</strong><span>Selecione para adicionar à avaliação</span></div>
        <div className="simulado-filters"><select aria-label="Filtrar por matéria" value={subjectId} onChange={(e) => { setSubjectId(Number(e.target.value)); setTopicId(0) }}><option value={0}>Todas as matérias</option>{subjects.map((s) => <option key={s.id} value={s.id}>{s.nome}</option>)}</select><select aria-label="Filtrar por assunto" value={topicId} onChange={(e) => setTopicId(Number(e.target.value))}><option value={0}>Todos os assuntos</option>{topics.filter((t) => !subjectId || t.materia_id === subjectId).map((t) => <option key={t.id} value={t.id}>{t.nome}</option>)}</select><input aria-label="Buscar questão" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Buscar enunciado"/></div>
        <div className="simulado-picker">{available.map((q) => <label key={q.id} className="simulado-picker-item"><input type="checkbox" disabled={locked || busy || (selected.length >= 200 && !selected.includes(q.id))} checked={selected.includes(q.id)} onChange={() => choose(q.id)}/><span>{q.enunciado}<small>{topics.find((t) => t.id === q.assunto_id)?.nome ?? 'Sem assunto'} · {q.nivel_dificuldade ?? 'Geral'}</small></span></label>)}{!available.length && <p className="empty-picker">Nenhuma questão com estes filtros.</p>}</div>
      </div>
      <div className="simulado-builder"><div className="simulado-builder-title"><strong>Ordem das questões</strong><span>{selected.length} selecionada(s) · máximo de 200</span></div><ol className="simulado-selected">{selected.map((id, index) => { const q = questions.find((item) => item.id === id); return <li key={id}><span className="simulado-question-label">{index + 1}. {q?.enunciado ?? `Questão #${id}`}</span><div className="row-actions"><button type="button" disabled={locked || index === 0} aria-label={`Subir questão ${index + 1}`} onClick={() => move(index, -1)}><ArrowUp size={16}/></button><button type="button" disabled={locked || index === selected.length - 1} aria-label={`Descer questão ${index + 1}`} onClick={() => move(index, 1)}><ArrowDown size={16}/></button><button type="button" disabled={locked} aria-label={`Remover questão ${index + 1}`} onClick={() => choose(id)}><X size={16}/></button></div></li> })}{!selected.length && <li className="empty-picker">Selecione questões do banco acima.</li>}</ol></div>
      {error && <p className="form-error" role="alert">{error}</p>}
      <div className="modal-actions"><button className="button ghost" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit" disabled={busy || !selected.length}>{busy ? 'Salvando...' : simulado ? 'Salvar simulado' : 'Criar simulado'}</button></div>
    </form>
  </Modal>
}

function Modal({ title, children, onClose }: { title: string; children: ReactNode; onClose: () => void }) { return <div className="modal-layer" role="dialog" aria-modal="true" aria-label={title}><div className="modal"><header><h2>{title}</h2><button onClick={onClose} aria-label="Fechar"><X size={20}/></button></header>{children}</div></div> }

function SubjectModal({ subject, onClose, onSave }: { subject: Materia | null; onClose: () => void; onSave: (data: Pick<Materia, 'nome' | 'descricao'>) => Promise<void> }) {
  const [name, setName] = useState(subject?.nome ?? '')
  const [description, setDescription] = useState(subject?.descricao ?? '')
  const [busy, setBusy] = useState(false)
  return <Modal title={subject ? 'Editar matéria' : 'Nova matéria'} onClose={onClose}><form className="modal-form" onSubmit={(e) => { e.preventDefault(); setBusy(true); void onSave({ nome: name.trim(), descricao: description.trim() }).finally(() => setBusy(false)) }}><label>Nome da matéria<input autoFocus value={name} onChange={(e) => setName(e.target.value)} required maxLength={100}/></label><label>Descrição<input value={description} onChange={(e) => setDescription(e.target.value)}/></label><div className="modal-actions"><button className="button ghost" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit" disabled={busy}>{busy ? 'Salvando...' : 'Salvar matéria'}</button></div></form></Modal>
}

function TopicModal({ topic, subjects, onClose, onSave }: { topic: Assunto | null; subjects: Materia[]; onClose: () => void; onSave: (data: Omit<Assunto, 'id'>) => Promise<void> }) {
  const [name, setName] = useState(topic?.nome ?? '')
  const [subjectId, setSubjectId] = useState(topic?.materia_id ?? subjects[0]?.id ?? 0)
  const [busy, setBusy] = useState(false)
  return <Modal title={topic ? 'Editar assunto' : 'Novo assunto'} onClose={onClose}><form className="modal-form" onSubmit={(e) => { e.preventDefault(); setBusy(true); void onSave({ nome: name.trim(), materia_id: subjectId, descricao: topic?.descricao ?? null }).finally(() => setBusy(false)) }}><label>Matéria<select required value={subjectId} onChange={(e) => setSubjectId(Number(e.target.value))}>{subjects.map((s) => <option key={s.id} value={s.id}>{s.nome}</option>)}</select></label><label>Nome do assunto<input autoFocus value={name} onChange={(e) => setName(e.target.value)} required maxLength={100}/></label><div className="modal-actions"><button className="button ghost" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit" disabled={busy}>{busy ? 'Salvando...' : 'Salvar assunto'}</button></div></form></Modal>
}

function QuestionModal({ question, subjects, topics, onClose, onSave }: { question: Questao | null; subjects: Materia[]; topics: Assunto[]; onClose: () => void; onSave: (data: QuestaoInput) => Promise<void> }) {
  const currentTopic = topics.find((t) => t.id === question?.assunto_id)
  const [statement, setStatement] = useState(question?.enunciado ?? '')
  const [subjectId, setSubjectId] = useState(currentTopic?.materia_id ?? subjects[0]?.id ?? 0)
  const [topicId, setTopicId] = useState(question?.assunto_id ?? topics.find((t) => t.materia_id === subjects[0]?.id)?.id ?? 0)
  const [alternatives, setAlternatives] = useState(question?.alternativas.map((a) => a.texto) ?? ['', '', '', ''])
  const [correctIndex, setCorrectIndex] = useState(question ? question.alternativas.findIndex((a) => a.correta) : 0)
  const [difficulty, setDifficulty] = useState(question?.nivel_dificuldade ?? '')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const availableTopics = topics.filter((t) => t.materia_id === subjectId)
  const changeSubject = (id: number) => { setSubjectId(id); setTopicId(topics.find((t) => t.materia_id === id)?.id ?? 0) }
  const updateAlternative = (index: number, value: string) => setAlternatives((prev) => prev.map((a, i) => i === index ? value : a))
  const submit = (e: FormEvent) => {
    e.preventDefault()
    if (!topicId || !statement.trim() || alternatives.some((a) => !a.trim()) || correctIndex < 0 || correctIndex >= alternatives.length) { setError('Preencha o enunciado, selecione o assunto e informe todas as alternativas.'); return }
    setBusy(true)
    setError('')
    void onSave({ assunto_id: topicId, enunciado: statement.trim(), nivel_dificuldade: difficulty || null, alternativas: alternatives.map((texto, i) => ({ texto: texto.trim(), correta: i === correctIndex })) }).finally(() => setBusy(false))
  }
  return <Modal title={question ? 'Editar questão' : 'Nova questão'} onClose={onClose}><form className="modal-form question-form" onSubmit={submit}><label>Enunciado<textarea autoFocus value={statement} onChange={(e) => setStatement(e.target.value)} rows={3} required/></label><div className="form-grid"><label>Matéria<select value={subjectId} onChange={(e) => changeSubject(Number(e.target.value))}>{subjects.map((s) => <option value={s.id} key={s.id}>{s.nome}</option>)}</select></label><label>Assunto<select value={topicId} required onChange={(e) => setTopicId(Number(e.target.value))}>{availableTopics.length ? availableTopics.map((t) => <option key={t.id} value={t.id}>{t.nome}</option>) : <option value={0}>Cadastre um assunto</option>}</select></label></div><fieldset><legend>Alternativas <span>Marque uma correta (de 2 a 5).</span></legend>{alternatives.map((alternative, index) => <label className="alternative-input" key={index}><input type="radio" name="correct" checked={correctIndex === index} onChange={() => setCorrectIndex(index)} aria-label={`Alternativa ${index + 1} correta`}/><span>{String.fromCharCode(65 + index)}</span><input required value={alternative} onChange={(e) => updateAlternative(index, e.target.value)} placeholder={`Alternativa ${index + 1}`}/></label>)}<div className="alternative-buttons"><button type="button" className="button ghost" disabled={alternatives.length >= 5} onClick={() => setAlternatives([...alternatives, ''])}>+ Alternativa</button><button type="button" className="button ghost" disabled={alternatives.length <= 2} onClick={() => { setAlternatives(alternatives.slice(0, -1)); setCorrectIndex(Math.min(correctIndex, alternatives.length - 2)) }}>− Alternativa</button></div></fieldset><label>Dificuldade<select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}><option value="">Não definida</option><option>Fácil</option><option>Médio</option><option>Difícil</option></select></label>{error && <p className="form-error">{error}</p>}<div className="modal-actions"><button className="button ghost" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit" disabled={busy}>{busy ? 'Salvando...' : question ? 'Salvar alterações' : 'Cadastrar questão'}</button></div></form></Modal>
}

function StudentArea({ user, onLogout }: { user: Usuario; onLogout: () => void }) {
  const [simulados, setSimulados] = useState<Simulado[]>([])
  const [history, setHistory] = useState<Tentativa[]>([])
  const [active, setActive] = useState<Tentativa | null>(null)
  const [gameQuestions, setGameQuestions] = useState<QuestaoJogo[]>([])
  const [result, setResult] = useState<Resultado | null>(null)
  const [iaStatus, setIaStatus] = useState<IAStatus | null>(null)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [busy, setBusy] = useState(false)
  const refresh = useCallback(async () => {
    const [list, attempts] = await Promise.all([api.simulados(), api.tentativas()])
    setSimulados(list)
    setHistory(attempts.slice().reverse())
  }, [])

  useEffect(() => { void refresh().catch((err: unknown) => setError(errorMessage(err))); void api.iaStatus().then(setIaStatus).catch(() => setIaStatus(null)) }, [refresh])

  const act = async (work: () => Promise<void>) => {
    setError('')
    setNotice('')
    setBusy(true)
    try { await work() }
    catch (err) { if (err instanceof ApiError && err.status === 401) onLogout(); else setError(errorMessage(err)) }
    finally { setBusy(false) }
  }
  const openAttempt = async (attempt: Tentativa) => {
    await act(async () => { const list = await api.questoesDaTentativa(attempt.id); setGameQuestions(list); setActive(attempt); setResult(null) })
  }
  const start = async (simulado: Simulado) => {
    await act(async () => {
      const attempt = await api.iniciar(simulado.id)
      const list = await api.questoesDaTentativa(attempt.id)
      setGameQuestions(list); setActive(attempt); setResult(null)
      await refresh()
    })
  }
  const viewResult = async (attempt: Tentativa) => {
    await act(async () => {
      const [corrected, list] = await Promise.all([api.resultado(attempt.id), api.questoesDaTentativa(attempt.id)])
      setGameQuestions(list); setActive(corrected.tentativa); setResult(corrected)
    })
  }
  const generateExplanations = async () => {
    if (!active) return
    await act(async () => {
      const corrected = await api.gerarExplicacoes(active.id)
      setResult(corrected)
      setNotice('Explicações pedagógicas registradas.')
    })
  }
  const answer = async (question: QuestaoJogo, alternativeId: number) => {
    if (!active) return
    await act(async () => {
      await api.responder(active.id, question.id, alternativeId)
      setGameQuestions((prev) => prev.map((q) => q.id === question.id ? { ...q, respondida_alternativa_id: alternativeId } : q))
      setNotice('Resposta salva.')
    })
  }
  const finish = async () => {
    if (!active || !window.confirm('Finalizar a tentativa? Você não poderá alterar suas respostas depois.')) return
    await act(async () => {
      const corrected = await api.finalizar(active.id)
      setResult(corrected); setActive(corrected.tentativa)
      await refresh()
    })
  }
  const goBack = () => { setActive(null); setResult(null); setGameQuestions([]); void refresh().catch((err: unknown) => setError(errorMessage(err))) }
  const activeName = simulados.find((s) => s.id === active?.simulado_id)?.titulo ?? 'Simulado'
  const answered = gameQuestions.filter((q) => q.respondida_alternativa_id !== null).length

  return <main className="student-preview student-area">
    <header><Brand/><div className="student-user"><span>Olá, {user.nome.split(' ')[0]}</span><button className="button ghost" onClick={onLogout}><LogOut size={17}/> Sair</button></div></header>
    <section className="student-content">
      <div className="student-heading"><span className="eyebrow">ÁREA DO ALUNO</span><h1>{active ? activeName : 'Seus simulados'}</h1><p>{active ? 'Suas respostas são registradas no servidor.' : 'Escolha um simulado, continue uma tentativa ou consulte seu desempenho.'}</p></div>
      {error && <div className="api-banner error" role="alert">{error}</div>}
      {notice && <div className="api-banner" role="status">{notice}</div>}
      {active ? <div className="student-workspace">
        {result ? <article className="panel result-panel"><h2>Simulado finalizado!</h2><p className="result-score">{Number(result.tentativa.percentual_aproveitamento).toFixed(1)}%</p><p>{result.tentativa.acertos} acertos · {result.tentativa.erros} erros · {gameQuestions.length - result.tentativa.acertos - result.tentativa.erros} sem resposta</p><h3>Correção das suas respostas</h3>{gameQuestions.map((q, index) => { const answer = result.respostas.find((r) => r.questao_id === q.id); return <div key={q.id} className="result-row"><strong>{index + 1}. {q.enunciado}</strong><span className={answer?.correta ? 'correct' : 'incorrect'}>{!answer ? 'Não respondida' : answer.correta ? 'Correta' : 'Incorreta'}</span>{answer?.explicacao_ia && <p>{answer.explicacao_ia}</p>}</div> })}{result.respostas.some((r) => !r.correta && !r.explicacao_ia) && <div className="ai-placeholder"><Sparkles size={19}/><div><strong>Explicações pedagógicas com IA</strong><p>{iaStatus?.descricao ?? 'A integração com IA está sendo preparada.'}</p></div>{iaStatus?.disponivel && <button className="button secondary" disabled={busy} onClick={() => void generateExplanations()}>Gerar explicações</button>}</div>}<button className="button primary" onClick={goBack}>Voltar aos simulados</button></article>
        : <><div className="student-toolbar"><button className="button ghost" onClick={goBack}><ArrowLeft size={17}/> Voltar</button><strong>{answered}/{gameQuestions.length} respondidas</strong></div>{gameQuestions.map((q, index) => <article key={q.id} className="panel quiz-card"><h2>Questão {index + 1} <span className="count-badge">{q.nivel_dificuldade ?? 'Geral'}</span></h2><p>{q.enunciado}</p><div className="quiz-options">{q.alternativas.map((a, i) => <label key={a.id} className={q.respondida_alternativa_id === a.id ? 'chosen' : ''}><input type="radio" name={`question-${q.id}`} disabled={busy} checked={q.respondida_alternativa_id === a.id} onChange={() => void answer(q, a.id)}/><span>{String.fromCharCode(65 + i)}.</span>{a.texto}</label>)}</div></article>)}<div className="student-toolbar"><span>As questões não respondidas reduzem o aproveitamento.</span><button className="button primary" disabled={busy} onClick={() => void finish()}>Finalizar simulado</button></div></>}
      </div> : <div className="student-workspace"><div className="student-section-heading"><h2>Simulados disponíveis</h2><p>{simulados.length} disponível(is)</p></div><div className="simulado-grid">{simulados.map((s) => <article className="panel" key={s.id}><ClipboardList size={30}/><h3>{s.titulo}</h3><p>{s.descricao ?? 'Avaliação objetiva'}</p><span>{s.total_questoes} questões</span><button disabled={busy || s.total_questoes === 0} className="button primary" onClick={() => void start(s)}>Iniciar simulado <ChevronRight size={17}/></button></article>)}{!simulados.length && <p>Nenhum simulado disponível. Peça ao administrador para cadastrá-los.</p>}</div><div className="student-section-heading"><h2>Meu histórico</h2><p>{history.length} tentativa(s)</p></div><div className="panel"><div className="history-list">{history.map((attempt) => <div className="history-row" key={attempt.id}><span><strong>{simulados.find((s) => s.id === attempt.simulado_id)?.titulo ?? `Simulado #${attempt.simulado_id}`}</strong><small>{new Date(attempt.data_inicio).toLocaleString('pt-BR')}</small></span><span>{attempt.status === 'FINALIZADO' ? `${Number(attempt.percentual_aproveitamento).toFixed(1)}% · ${attempt.acertos} acertos` : 'Em andamento'}</span>{attempt.status === 'EM_ANDAMENTO' ? <button className="button secondary" disabled={busy} onClick={() => void openAttempt(attempt)}>Continuar</button> : <button className="button secondary" disabled={busy} onClick={() => void viewResult(attempt)}>Ver resultado</button>}</div>)}{!history.length && <p>Você ainda não iniciou nenhum simulado.</p>}</div></div></div>}
    </section>
  </main>
}

export default App
