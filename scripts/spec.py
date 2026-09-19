# Specimen bodies. Each is a LaTeX fragment; {W} is the measure in inches.
SPECIMENS = {}

SPECIMENS['paper'] = r"""
\begin{varwidth}{4.7in}\fontsize{10.5}{14.2}\selectfont
\noindent\textbf{3.2\quad Convergence of the truncated operator}\par\medskip
\noindent Let $\mathcal{H}$ be a separable Hilbert space and let $T_n$ denote the
rank-$n$ truncation of $T$. We first show that $\|T_n - T\|\to 0$ whenever the
spectral measure $\mu$ is absolutely continuous; the singular case is deferred to
Section~4. The argument is elementary but the bookkeeping is delicate, because the
error term $\varepsilon_n = O(n^{-1/2}\log n)$ is not uniform in $\lambda$.
Throughout, $c$ and $C$ denote absolute constants whose value may change from line
to line. Note that $\langle T_n x, y\rangle \to \langle Tx, y\rangle$ for all
$x, y \in \mathcal{H}$, so weak convergence is immediate; the content of the
theorem is that the convergence is in fact uniform on bounded sets.
\end{varwidth}"""

SPECIMENS['display'] = r"""
\begin{varwidth}{4.7in}\fontsize{10.5}{14.2}\selectfont
\noindent For every $f \in L^2(\mathbb{R}^d)$ and every $\alpha > 0$,
\[
  \widehat{f}(\xi) \;=\; \int_{\mathbb{R}^d} f(x)\, e^{-2\pi i \langle x,\xi\rangle}\,dx,
  \qquad
  \bigl\|\widehat{f}\,\bigr\|_{2} = \|f\|_{2}.
\]
\[
  \sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n^{s}}
  \;=\; \bigl(1 - 2^{1-s}\bigr)\zeta(s),
  \qquad
  \Gamma(z) = \int_0^\infty t^{z-1}e^{-t}\,dt .
\]
\[
  \frac{\partial u}{\partial t} = \nabla\!\cdot\!\bigl(D(u)\,\nabla u\bigr) + f,
  \qquad
  A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22}\end{pmatrix},
  \qquad
  \lim_{h\to 0^{+}} \frac{\varphi(x+h)-\varphi(x)}{h} .
\]
\end{varwidth}"""

SPECIMENS['theorem'] = r"""
\begin{varwidth}{4.7in}\fontsize{10.5}{14.2}\selectfont
\noindent\textbf{Theorem 3.4 (Spectral gap).}\;\textit{Let $P$ be reversible with
respect to $\pi$ and suppose $\lambda_2(P) \le 1-\delta$ for some $\delta \in (0,1)$.
Then for every $x$ in the state space,}
\[ \bigl\|P^{t}(x,\cdot) - \pi\bigr\|_{\mathrm{TV}} \le \tfrac{1}{2}\,\delta^{-1/2}\,(1-\delta)^{t}. \]
\noindent\textsc{Proof.} Expand $P^{t}$ in the orthonormal basis of eigenfunctions
$\{\varphi_j\}$ and apply Cauchy--Schwarz. Since $\varphi_1 \equiv 1$, the $j=1$
term cancels, leaving $\sum_{j\ge 2}\lambda_j^{2t}\varphi_j(x)^2 \le
(1-\delta)^{2t}\pi(x)^{-1}$. Taking square roots gives the claim. \hfill$\square$
\end{varwidth}"""

SPECIMENS['slide'] = r"""
\begin{varwidth}{4.7in}
{\fontsize{21}{25}\selectfont\bfseries Why the gap closes}\par\medskip
{\fontsize{12.5}{17}\selectfont
\begin{itemize}\setlength{\itemsep}{2pt}\setlength{\parskip}{0pt}
  \item Truncation error decays as $n^{-1/2}\log n$
  \item Uniform on bounded sets --- not just weakly
  \item Fails when $\mu$ has a singular part
\end{itemize}\par\smallskip
\[ \bigl\|T_n - T\bigr\| \;\longrightarrow\; 0 \qquad (n \to \infty) \]}
\end{varwidth}"""

SPECIMENS['ui'] = r"""
\begin{varwidth}{4.7in}
{\sffamily\fontsize{12}{15}\selectfont\bfseries Run 417 --- diagnostics}\par\smallskip
{\fontsize{9}{12}\selectfont
\begin{tabular}{@{}l r r l@{}}
\textsc{parameter} & \textsc{value} & \textsc{s.e.} & \textsc{status}\\[2pt]
step size $h$        & 0.015625 & 0.000031 & converged\\
tolerance $\epsilon$ & 1.0e{-}09 & --- & fixed\\
iterations           & 18,402 & --- & 93.7\,\% of budget\\
residual $\|r\|_2$   & 4.81e{-}07 & 2.2e{-}09 & OK\\
wall clock           & 00:41:38 & --- & 2026-09-19\\
\end{tabular}}\par\medskip
{\fontsize{8}{10.5}\selectfont Footnote size: the Illinois lllustration (Il1 O0 rn m) tests
ambiguous pairs at 8\,pt, where screen rendering is least forgiving.}
\end{varwidth}"""

SPECIMENS['chars'] = r"""
\begin{varwidth}{4.7in}\fontsize{12}{16}\selectfont
ABCDEFGHIJKLMNOPQRSTUVWXYZ\par
abcdefghijklmnopqrstuvwxyz\par
0123456789 \quad \textit{0123456789} \quad \textbf{0123456789}\par\smallskip
\textit{Italic: the quick brown fox} \quad \textbf{Bold weight}\par
Il1 O0 rn/m \quad ``quotes'' --- en--dash \quad \&\,\%\,\$\,@\,\#\par\smallskip
\noindent$\alpha\beta\gamma\delta\epsilon\zeta\eta\theta\kappa\lambda\mu\nu\xi\pi\rho\sigma\tau\phi\chi\psi\omega$
\quad $\Gamma\Delta\Theta\Lambda\Xi\Pi\Sigma\Phi\Psi\Omega$\par
$\mathbb{N}\,\mathbb{Z}\,\mathbb{Q}\,\mathbb{R}\,\mathbb{C}$ \quad
$\mathcal{A}\,\mathcal{B}\,\mathcal{F}\,\mathcal{H}\,\mathcal{L}$ \quad
$\int \oint \sum \prod \sqrt{x} \partial \nabla \infty$\par
$\leq \geq \neq \approx \equiv \subset \in \notin \rightarrow \Rightarrow \mapsto \otimes \oplus$
\end{varwidth}"""
