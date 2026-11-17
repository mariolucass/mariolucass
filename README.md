<div align="center">

<img src="./assets/brand/hero.svg" alt="Mário Lucas, Full Stack Software Engineer. Terminal: architecture, code, cloud, delivery; shipping to production, and it keeps running. Open to engineering opportunities." width="100%">

<br>

<a href="https://mariolucas.tech"><img src="./assets/widgets/link-portfolio.svg" alt="Portfolio: mariolucas.tech" width="32%"></a>
<a href="https://www.linkedin.com/in/mariolucass/"><img src="./assets/widgets/link-linkedin.svg" alt="LinkedIn: in/mariolucass" width="32%"></a>
<a href="mailto:mariolasdev@gmail.com"><img src="./assets/widgets/link-email.svg" alt="Email: mariolasdev@gmail.com" width="32%"></a>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/sections/what-dark.svg">
  <img src="./assets/sections/what-light.svg" alt="01 — What I do" width="100%">
</picture>

<img src="./assets/cards/bento.svg" alt="Real problems, owned end to end. Four years in software: almost three reviewing other people's code at Kenzie, then over a year running a production platform alone at CECAPE. 1,650+ technical issues resolved, 450+ code reviews, 9.17 academic average, English C1." width="100%">

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/sections/work-dark.svg">
  <img src="./assets/sections/work-light.svg" alt="02 — Selected work" width="100%">
</picture>

### CECAPE Tech · Academic Repository

**Sole technical owner · Architecture → Production on AWS**

The institutional repository of Faculdade CECAPE, designed and shipped from zero.<br>**260 publications** from **418 authors**, across **17 courses**, organized in **6 collections**.

**[Visit the repository ↗](https://repositorio.faculdadececape.edu.br/)**

<a href="https://repositorio.faculdadececape.edu.br/"><img src="./assets/cards/repo-stats.svg" alt="Academic Repository: 260 publications from 418 authors, across 17 courses, in 6 collections." width="100%"></a>

<br>

<img src="./assets/diagrams/architecture.svg" alt="Architecture: readers reach App Runner inside a VPC, which talks to RDS PostgreSQL for full-text search and to S3 for files, with IAM scoping permissions." width="100%">

<br>

<img src="./assets/cards/decisions.svg" alt="Decisions: DDD plus events, native PostgreSQL full-text search, least-privilege AWS." width="100%">

<br>

<details>
<summary><b>Why no Elasticsearch?</b></summary>

<br>

The catalog is a bounded, relational dataset. Postgres `tsvector` + GIN indexes cover ranking, stemming and filters in the same transaction as the rest of the data, so there is no second system to sync, secure, monitor or pay for. If the problem outgrows it, the domain boundary makes the swap local.

</details>

<br>

### Kenzie Academy Brasil

**Technical Mentor & Code Reviewer**

Unblocked developers at scale: **1,650+ technical issues resolved**<br>and **450+ code reviews** delivered, raising code quality across cohorts.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/sections/building-dark.svg">
  <img src="./assets/sections/building-light.svg" alt="03 — Currently building" width="100%">
</picture>

<img src="./assets/cards/now.svg" alt="Now: building Iron Ledger, running the Academic Repository in production, studying Information Systems at IFCE." width="100%">

<br>

### Iron Ledger · Inventory, audit and saga orchestration

*In development · TypeScript · Express · Prisma · PostgreSQL · RabbitMQ · Temporal · Next.js · Python*

A distributed system for stock operations: every mutation is traceable,<br>multi-step transactions compensate when they fail, and the audit trail can't be rewritten.

**[Live demo ↗](https://iron-ledger-six.vercel.app/)**

<a href="https://iron-ledger-six.vercel.app/"><img src="./assets/diagrams/ledger-flow.svg" alt="Iron Ledger flow: a stock movement is written with its outbox event in PostgreSQL, relayed through RabbitMQ and stored in an append-only audit log. A transaction starts a Temporal saga that reserves and confirms stock, or releases the reservation on failure." width="100%"></a>

<br>

<img src="./assets/cards/ledger.svg" alt="Iron Ledger: transactional outbox, sagas, append-only audit, DDD." width="100%">

<br>

Next.js frontend in Feature-Sliced Design, with a BFF that keeps the session JWT in an HTTP-only cookie.<br>An isolated Python analytics service runs batch pipelines behind its own HTTP API.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/sections/toolkit-dark.svg">
  <img src="./assets/sections/toolkit-light.svg" alt="04 — Toolkit" width="100%">
</picture>

<img src="./assets/widgets/toolkit.svg" alt="Toolkit: React, Next.js, TypeScript, Tailwind, shadcn/ui, Node.js, Express, Python, Django, PostgreSQL, Redis, Prisma, AWS, Docker, Git, RabbitMQ, Temporal." width="100%">

<br>

DDD &nbsp;·&nbsp; Event-driven &nbsp;·&nbsp; Sagas &nbsp;·&nbsp; REST &nbsp;·&nbsp; JWT &nbsp;·&nbsp; RBAC &nbsp;·&nbsp; Feature-Sliced Design

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/sections/background-dark.svg">
  <img src="./assets/sections/background-light.svg" alt="05 — Background" width="100%">
</picture>

**B.Sc. Information Systems · IFCE** (expected 2027)<br>Academic average **9.17/10** &nbsp;·&nbsp; English **C1**, EF SET 66/100

<br><br>

<img src="./assets/cards/cta.svg" alt="Let’s build something useful." width="100%">

<br>

Open to engineering opportunities and conversations about my work.

<a href="mailto:mariolasdev@gmail.com"><img src="./assets/widgets/link-email.svg" alt="Email: mariolasdev@gmail.com" width="32%"></a>
<a href="https://www.linkedin.com/in/mariolucass/"><img src="./assets/widgets/link-linkedin.svg" alt="LinkedIn: in/mariolucass" width="32%"></a>
<a href="https://github.com/mariolucass"><img src="./assets/widgets/link-github.svg" alt="GitHub: mariolucass" width="32%"></a>

<br>

<img src="./assets/brand/footer.svg" alt="Mário Lucas" width="100%">

</div>
