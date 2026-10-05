# Track 12 — Web Engineering (JS runtime → browser → React → typed backend → shipped)

> **Muscle group:** the arms you already have. This track is about the tendons underneath them.
> **Prereqs:** Phases 1–3 need nothing but a laptop. Phase 4 needs Track 03 Phase 1–2, Track 05 Set 3.3, and Track 06 Phase 2.
> **Assumes you already ship frontend code.** Nothing here explains what a component or a `fetch` call is.

## Why this track

Most frontend engineers who say they know JavaScript know its API. The ones who can fix
anything know its machinery: why a closure keeps a 40MB array alive, why a microtask loop
freezes the page and a `setTimeout` loop doesn't, why a cookie works locally and vanishes
behind the proxy, why a `useEffect` reads a value from three renders ago.

**The rule for this track: you build the thing before you use the library.** You write your
own Promise, your own React, your own store, your own reverse proxy, and your own session
auth. They will be worse than the real ones. That's fine. After building one, you
understand the real one well enough to debug it.

**If you can already explain a plain checkbox cold, check it and move on.** Spend your time
on the Reps.

**Where things go:** code in `work/12-web/<set-name>/`, writeups in `notes/`.

## Equipment

| Resource | Use it for |
|---|---|
| **You Don't Know JS Yet** — Kyle Simpson (free on GitHub) | *Scope & Closures* and *Objects & Classes*. The best explanation of the runtime |
| **javascript.info** — the advanced sections only | Event loop, prototypes, promises, generators, Proxy |
| **Jake Archibald — "In The Loop"** (JSConf Asia, YouTube) | The event loop *with* rendering. Watch this before Set 1.4 |
| **Build Your Own React** — Rodrigo Pombo (pomb.us/build-your-own-react) | Phase 3 centrepiece |
| **react.dev** — especially *You Might Not Need an Effect*, *Preserving and Resetting State* | The current mental model of React |
| **Mark Erikson — A (Mostly) Complete Guide to React Rendering Behavior** | When and why components re-render |
| **Stanford CS253 Web Security** (web.stanford.edu/class/cs253, free lectures) | Cookies, same-origin policy, CSRF, XSS, CSP. Core of Set 2.4 and 4.4 |
| **MIT 6.858 / 6.5660 Computer Systems Security** — web security lectures and the browser-security lab | Attacking a deliberately vulnerable web app |
| **PortSwigger Web Security Academy** (free labs) | Hands-on XSS, CSRF, CORS, JWT, OAuth attacks |
| **The Copenhagen Book** (thecopenhagenbook.com) | Building auth yourself, correctly. Phase 4 |
| **OWASP Cheat Sheets** — Session Management, Password Storage, Authentication | Reference while you build |
| **Effective TypeScript** — Dan Vanderkam + **type-challenges** (GitHub) | Phase 3 types |
| **web.dev** — rendering performance, Core Web Vitals | Set 2.1, 2.6 |
| **Pydantic v2 docs**, **nginx docs**, **MDN** | References |

---

## Phase 1 — Foundation (the JavaScript runtime, rebuilt by hand)

### Set 1.1 — Scope, closures, and what they cost
- [ ] Lexical environments, the scope chain, hoisting, and the temporal dead zone. Know why `let` in a `for` loop gives each iteration its own binding and `var` doesn't
- [ ] A closure is a function plus a reference to its environment, not a copy of it. Predict what changes when the outer variable is reassigned after the closure is created
- [ ] **Rep:** implement from scratch, with tests: `once`, `memoize` (with a cache-key function and an LRU bound), `debounce` and `throttle` (both with leading/trailing options and a `.cancel()`)
- [ ] **Rep:** write a closure that accidentally keeps a large object alive (an event handler that captures a big array). Find it in a DevTools heap snapshot through the retainer path, then fix it. Write up the retainer chain in `notes/closure-leak.md`
- [ ] Module pattern vs ES module scope vs class private fields (`#x`): three ways to get private state, and what each costs

### Set 1.2 — `this`, prototypes, and objects
- [ ] The four `this` binding rules (default, implicit, explicit, `new`), their precedence, and why arrow functions ignore all four
- [ ] **Rep:** write `call`, `apply`, and `bind` yourself. Your `bind` must work with `new` (the bound function used as a constructor). This edge case is the actual test
- [ ] **Rep:** write `myNew(Ctor, ...args)`, `myInstanceOf(obj, Ctor)`, and `Object.create` without using the built-ins
- [ ] Prototype chain lookup, `__proto__` vs `.prototype`, property shadowing, and what `class` actually compiles down to (desugar one class with `extends` and `super` by hand)
- [ ] Property descriptors, getters/setters, `Object.freeze` vs `seal` vs `preventExtensions`, and why `freeze` is shallow
- [ ] **Rep:** write `deepFreeze` and `deepClone`. The clone must handle cycles, `Date`, `Map`, `Set`. Then compare your clone to `structuredClone` and list what each one refuses to copy

### Set 1.3 — Functional techniques: currying, composition, partial application
- [ ] Currying vs partial application. They're different things and people mix them up. Define each in one sentence
- [ ] **Rep:** implement `curry(fn)` that supports calling with any grouping of arguments: `f(1)(2)(3)`, `f(1, 2)(3)`, `f(1)(2, 3)`. Then add placeholder support (`f(_, 2)(1)`) like Ramda's `R.__`
- [ ] Know the `fn.length` trap: default parameters and rest parameters change it, so a naive curry breaks. Write a test that shows the break
- [ ] **Rep:** implement `compose` and `pipe`, then an async `pipeAsync` that awaits each step. Build a real data-transformation pipeline with them, not a toy example
- [ ] Point-free style: where it helps readability and where it makes stack traces useless. Have an opinion and write it down
- [ ] Immutability in practice: structural sharing, and why `[...arr]` in a reducer is O(n). **Rep:** write a tiny persistent list or map with structural sharing and benchmark it against copying

### Set 1.4 — The event loop (in the browser *and* in Node)
- [ ] Watch "In The Loop". Call stack, task queue, microtask queue, and where **rendering** fits (rAF → style → layout → paint) inside a loop iteration
- [ ] Which APIs queue which kind of work: `setTimeout`, `MessageChannel`, `queueMicrotask`, promise reactions, `MutationObserver`, `requestAnimationFrame`, `requestIdleCallback`
- [ ] **Rep:** write 10 output-ordering puzzles of your own that mix all of the above, predict each one, then run it. Keep the ones you got wrong in `notes/event-loop-puzzles.md`
- [ ] **Rep:** freeze the page with a microtask loop, then show that the same loop written with `setTimeout` lets the page render. Explain why in three sentences
- [ ] Node's loop is different: libuv phases (timers → pending → poll → check → close), `process.nextTick` vs microtasks, `setImmediate` vs `setTimeout(0)`
- [ ] **Rep:** write a Node script whose output order depends on whether it runs inside an I/O callback. Explain the difference using the phases
- [ ] **Rep:** split a 2-second synchronous computation into chunks so the UI stays responsive. Do it three ways (`setTimeout` chunking, `scheduler.yield()` / `MessageChannel`, a Web Worker) and measure input delay for each

### Set 1.5 — Promises and async, built from scratch
- [ ] **Rep:** implement a Promises/A+ compliant `MyPromise` and pass the official `promises-aplus-tests` suite. The thenable-assimilation rules (2.3) are where it gets hard. **This is the centrepiece of Phase 1**
- [ ] **Rep:** implement `all`, `allSettled`, `race`, `any` (including `AggregateError`) on top of your promise
- [ ] Unhandled rejections: when the browser and Node fire them, and why a late `.catch` still counts as unhandled
- [ ] **Rep:** implement `async`/`await` yourself using generators plus a runner function (the `co` pattern). Once this works, `await` isn't magic anymore
- [ ] **Rep:** write `promisePool(tasks, concurrency)`, `retry(fn, {retries, backoff, jitter})`, and `timeout(promise, ms)` with real cancellation via `AbortSignal`. You'll reuse all three in Phase 4
- [ ] Async iterators and `for await`. **Rep:** consume a paginated API as an async generator that fetches lazily and stops early on `break`

### Set 1.6 — Metaprogramming, memory, and the engine
- [ ] Iterators and generators as protocols: implement `Symbol.iterator` on your own collection
- [ ] `Proxy` and `Reflect`: all the traps you'd actually use, plus the invariants a proxy must respect
- [ ] **Rep:** build a reactive store with `Proxy`: deep property tracking, effects that re-run when a value they read changes, and batched notifications. This is what Vue's reactivity and MobX do. You'll compare it to React's model in Phase 3
- [ ] `WeakMap`, `WeakSet`, `WeakRef`, `FinalizationRegistry`: what each guarantees, and why you can't rely on `FinalizationRegistry` callbacks ever running
- [ ] V8 basics: hidden classes (maps), inline caches, why changing an object's shape in a hot path is slow, and what a deopt is
- [ ] **Rep:** write a micro-benchmark where monomorphic code beats polymorphic code by a large margin. Run it with `node --trace-deopt` and read the output. Be honest in your writeup about how misleading micro-benchmarks are

### Set 1.7 — Modules and build tools
- [ ] ESM vs CommonJS: static vs dynamic, live bindings vs copied values, how circular imports behave in each, top-level await, the dual-package problem
- [ ] **Rep:** create a circular import that produces `undefined` in CJS and a `ReferenceError` in ESM. Explain both
- [ ] **Rep:** build a tiny bundler (in the style of `minipack`): parse files with `acorn`, build the dependency graph, wrap each module in a function, emit one runnable file. Add a naive tree-shaking pass for unused named exports
- [ ] What Vite actually does in dev (native ESM + esbuild pre-bundling) vs in production (Rollup). Source maps: what's in the file and how DevTools uses it

---

## Phase 2 — Volume (the browser as a platform)

### Set 2.1 — The rendering pipeline
- [ ] Parse HTML → DOM, parse CSS → CSSOM, then style → layout → paint → composite. What render-blocking and parser-blocking mean, and how `async` / `defer` / `type=module` change script loading
- [ ] Reflow vs repaint vs composite-only. Which CSS properties trigger which stage (use csstriggers-style reasoning, then verify in DevTools)
- [ ] **Rep:** write code that causes layout thrashing (alternating DOM reads and writes in a loop). Show the forced reflows in the Performance panel, fix it by batching reads before writes, and record before/after numbers
- [ ] **Rep:** build a virtualised list from scratch that renders 100,000 rows at 60fps with variable row heights. No library. Measure scroll performance
- [ ] Layers and compositing: `will-change`, `transform` vs `top/left` for animation, and the cost of having too many layers
- [ ] **Rep:** animate the same element with `left` and with `transform`. Show the difference in the Performance panel and the Layers panel

### Set 2.2 — DOM, events, and observers
- [ ] Event phases (capture, target, bubble), `stopPropagation` vs `stopImmediatePropagation`, `composedPath`, and how events cross shadow DOM boundaries
- [ ] **Rep:** implement event delegation for a 10,000-row table with one listener, including correct `closest()` targeting and keyboard accessibility
- [ ] Passive listeners and why scroll jank happens without them. `AbortController` for removing listeners in bulk
- [ ] `IntersectionObserver`, `ResizeObserver`, `MutationObserver`: what each one costs and when its callbacks run within the event loop
- [ ] **Rep:** build infinite scroll with `IntersectionObserver` plus your Set 1.5 `promisePool`, with request cancellation when the user scrolls fast
- [ ] **Rep:** build a tiny client-side router on the History API: `pushState`, `popstate`, link interception, scroll restoration. Note what breaks on a hard refresh until the server or proxy handles it (you'll fix this in Set 4.5)

### Set 2.3 — The Network tab, properly
Track 05 Set 3.3 covered HTTP itself and Track 07 Set 2.1 covered DevTools as a debugger. This set is about reading the Network tab as evidence.
- [ ] The timing breakdown: Queueing, Stalled, DNS Lookup, Initial connection, SSL, Request sent, Waiting (TTFB), Content Download. What makes each one large
- [ ] **Rep:** time the same request with DevTools and with your `curl -w` format from Track 05 (`notes/curl-timing.md`). Explain any difference: connection reuse, browser queueing, HTTP/2 coalescing
- [ ] Add the hidden columns: Protocol, Connection ID, Priority, Initiator, Size vs Transferred. Use Connection ID to *see* HTTP/2 multiplexing versus HTTP/1.1's six-connections-per-host limit
- [ ] Cache sources: `(memory cache)` vs `(disk cache)` vs a `304` revalidation vs a service worker. What each says about your `Cache-Control` and `ETag` headers
- [ ] Preflight requests: find them, read every `Access-Control-*` header, and set `Access-Control-Max-Age` to remove repeated preflights (browsers cap the value, so check what yours does)
- [ ] Initiator chains and request priority: why your hero image loads after a tracking script, and how `fetchpriority`, `preload`, and `preconnect` change it
- [ ] Tools: throttling, request blocking, **Local Overrides** (edit a production response on your machine), Copy as cURL / Copy as fetch, HAR export
- [ ] **Rep:** export a HAR from a real, heavy site. Write `notes/har-teardown.md`: the critical path, the three biggest wastes, and what you'd change. Then prove one fix works using Local Overrides
- [ ] **Rep:** reproduce and screenshot these four "the request failed" cases and how each one looks in the Network tab and the console: CORS block, mixed-content block, an extension blocking the request, a `(canceled)` request from navigation or an abort

### Set 2.4 — Cookies, storage, and the same-origin policy
Track 05 named the cookie attributes. Here you find out experimentally what they do.
- [ ] Origin vs site vs domain. Why `a.example.com` and `b.example.com` are *same-site* but *cross-origin*, and why that difference decides cookie behaviour
- [ ] Every `Set-Cookie` attribute: `Domain`, `Path`, `Expires`/`Max-Age`, `Secure`, `HttpOnly`, `SameSite=Strict|Lax|None`, `Partitioned` (CHIPS), and the `__Host-` / `__Secure-` prefixes. Know exactly what `__Host-` forces
- [ ] Browsers default to `SameSite=Lax`. Know the exceptions: top-level `GET` navigations still send Lax cookies, and some browsers briefly allow POST for newly set cookies
- [ ] Third-party cookie restrictions: Safari ITP, Firefox Total Cookie Protection, and Chrome's changing policy. What partitioned storage does to iframes and embeds
- [ ] **Rep — the cookie matrix.** Use your hosts file to set up `app.test`, `api.test`, and `evil.test` on local servers. Set one cookie of each kind (`Lax`, `Strict`, `None; Secure`, host-only, `Domain=`-scoped). For each of these, record which cookies arrive: top-level link, top-level form POST, `fetch` without credentials, `fetch` with `credentials: 'include'`, image tag, iframe. Save the table in `notes/cookie-matrix.md`. **This table will settle every cookie argument you have from now on**
- [ ] `localStorage` vs `sessionStorage` vs IndexedDB vs Cache Storage vs cookies: size limits, sync vs async, which ones scripts can read, how long each lasts, and storage partitioning
- [ ] **Rep:** open DevTools → Application and inspect, edit, and delete each kind of storage. Then do the same from code, including clearing site data

### Set 2.5 — Web security, attacked by you
- [ ] Watch the Stanford CS253 lectures on the same-origin policy, CSRF, XSS, and CSP
- [ ] Same-origin policy: what it actually blocks (*reading* cross-origin responses), not sending. Explain why CORS relaxes a browser rule and does **not** protect your server
- [ ] **Rep:** build a deliberately vulnerable mini-app with a comment box, a "transfer money" form, and a JSON API. Then attack it yourself:
  - [ ] Stored XSS that steals a non-`HttpOnly` cookie
  - [ ] Reflected XSS through a query parameter
  - [ ] DOM XSS through `innerHTML` and through `location.hash`
  - [ ] CSRF: a page on `evil.test` that submits the transfer form
  - [ ] Clickjacking: frame the app and trick a click
  - [ ] A CORS misconfiguration that reflects any `Origin` and allows credentials, then read private data from `evil.test`
- [ ] Now fix each one properly, and keep the before/after: output encoding, `HttpOnly`, `SameSite` plus a CSRF token, `frame-ancestors`, an origin allowlist
- [ ] **Content Security Policy:** nonce-based `script-src` with `strict-dynamic`, `report-to` / report-only mode, and Trusted Types. **Rep:** add a strict CSP to the mini-app, watch the violation reports, and fix the app until it runs clean
- [ ] Subresource Integrity, `Referrer-Policy`, `Permissions-Policy`, and COOP/COEP (also needed for `SharedArrayBuffer`)
- [ ] Do the PortSwigger Academy XSS, CSRF, and CORS apprentice-level labs. Keep notes only on the ones that surprised you

### Set 2.6 — Browser APIs you'd otherwise reach for a library for
- [ ] **Streams:** `ReadableStream`, `TransformStream`, `response.body`, backpressure. **Rep:** stream a large NDJSON response from your own server and render rows while it's still downloading. Show memory staying flat
- [ ] **Web Workers:** `postMessage` and the cost of structured cloning, transferables, and `Comlink`-style RPC. **Rep:** move a heavy parse or search into a worker, and write the RPC wrapper yourself
- [ ] **Service Workers:** registration, the install/activate/fetch lifecycle, update traps (the old worker keeps control), and cache strategies. **Rep:** make a small app work offline with a network-first strategy for the API and cache-first for static files. Then ship a broken service worker and work out how to recover users who already have it
- [ ] `BroadcastChannel` and the `storage` event for syncing tabs. **Rep:** log out in one tab and have every other tab follow
- [ ] IndexedDB is covered in Track 09 Set 4.2. Link your notes, don't repeat the work
- [ ] Core Web Vitals: LCP, INP, CLS. Lab data (Lighthouse) vs field data (CrUX, `web-vitals`). **Rep:** improve INP on a real interaction and prove it with field-style measurement, not just Lighthouse

---

## Phase 3 — Strength (React and TypeScript, from the inside)

### Set 3.1 — Build your own React
- [ ] **Rep:** work through *Build Your Own React* and type every line yourself: `createElement`, `render`, fibers, the interruptible work loop, render vs commit phases, reconciliation, function components, `useState`
- [ ] **Rep:** extend it beyond the tutorial: add `useEffect` with cleanup, keyed reconciliation for lists, and `useRef`. Write tests for each
- [ ] Now explain these from your implementation: why hooks must be called in the same order (they're a list indexed by call position), why `setState` doesn't change the value until the next render, and what "a render" actually is
- [ ] Save `notes/my-react.md`: the five biggest differences between your version and real React (scheduler lanes, event system, batching, effects timing, dev-mode double invoke)

### Set 3.2 — Rendering behaviour and identity
- [ ] Read Mark Erikson's rendering guide. Restate the rule: a component re-renders when its parent re-renders, unless something stops it. Prop changes aren't the trigger
- [ ] State belongs to a *position in the tree*, not to the component. **Rep:** show state resetting when the element type at a position changes, and state being kept when it doesn't. Then use `key` to reset state on purpose
- [ ] **Rep:** break a list by using array indexes as keys. Show inputs keeping the wrong values after a reorder. Fix it with stable keys
- [ ] Referential equality, `React.memo`, `useMemo`, `useCallback`. **Rep:** take an app with real lag, profile it with the React Profiler (with "why did this render" enabled), and fix it with the *fewest* memoizations. Write down which ones did nothing
- [ ] What the React Compiler automates, and which of your manual memoizations it would make unnecessary
- [ ] Batching in React 18+, `flushSync`, and when updates are synchronous vs deferred

### Set 3.3 — Effects and closures (where Phase 1 pays off)
- [ ] Stale closures in effects and handlers. **Rep:** write the classic interval counter that's stuck at 1, explain it using Set 1.1, then fix it three ways (functional update, ref, putting the dependency in the array)
- [ ] Read *You Might Not Need an Effect*. **Rep:** take an existing component of yours that uses effects to sync derived state and rewrite it with zero effects
- [ ] Effect cleanup and race conditions in data fetching. **Rep:** build a search box where fast typing never shows stale results, using an `AbortController` in the cleanup
- [ ] `useLayoutEffect` vs `useEffect` timing, related back to the rendering pipeline in Set 2.1. **Rep:** build a tooltip that flickers with `useEffect` and doesn't with `useLayoutEffect`. Show the frame in the Performance panel
- [ ] Strict Mode's double invoke. What it's catching, and why "turn it off" is the wrong fix

### Set 3.4 — State architecture
- [ ] Sort state into its real kinds: local UI state, shared client state, **server cache**, URL state, form state. Most state bugs come from storing one kind as if it were another
- [ ] Context re-render behaviour. **Rep:** build a context-based store, show every consumer re-rendering on any change, then fix it with split contexts and with selectors
- [ ] **Rep:** build a mini-Zustand on `useSyncExternalStore`, with selectors and equality functions. Demonstrate tearing without `useSyncExternalStore` in a concurrent render, and show it gone with it
- [ ] **Rep:** build a mini TanStack Query: a cache keyed by query key, request deduplication, stale-while-revalidate, invalidation after mutations, and an optimistic update with rollback. Then use the real library and list what it handles that yours doesn't
- [ ] Reducers and state machines: model a multi-step flow (checkout or upload) as an explicit state machine so impossible states can't be represented. Compare with XState
- [ ] Put the right state in the URL (filters, pagination, selected tab), and handle back/forward correctly

### Set 3.5 — Concurrency, Suspense, and the server
- [ ] `useTransition` and `useDeferredValue`. **Rep:** keep typing responsive while filtering 50k items, and measure input delay before and after
- [ ] Suspense for data and code splitting, and error boundaries (including what they *don't* catch: event handlers and async code)
- [ ] **Rep:** build server-side rendering by hand: a Node server that calls `renderToPipeableStream`, sends HTML, and hydrates with `hydrateRoot`. No framework. Then cause a hydration mismatch on purpose (a date, `Math.random`, a browser-only API) and fix it
- [ ] React Server Components at the concept level: what moves to the server, the serialisation boundary, and `"use client"`. Compare your hand-built SSR with a Next.js App Router page and write down what the framework added
- [ ] Forms: controlled vs uncontrolled, form actions, and validation that runs the same rules on client and server (this connects to Set 4.1)

### Set 3.6 — TypeScript as a design tool
- [ ] Structural typing, excess property checks (and why they only fire on fresh object literals), `unknown` vs `any` vs `never`
- [ ] Narrowing: `typeof`, `in`, discriminant checks, user-defined type guards, assertion functions. Exhaustiveness checks with `never`
- [ ] **Rep:** model API request state as a discriminated union (`idle | loading | success | error`) and remove every `data?.` optional chain in a real component. Make impossible states unrepresentable
- [ ] Generics with constraints, conditional types, `infer`, mapped types with key remapping, template literal types, `satisfies`, `as const`
- [ ] Branded types for IDs (`UserId` vs `OrderId`). **Rep:** catch a real mixed-up-ID bug at compile time
- [ ] **Rep:** do the **type-challenges** easy set and 20 medium ones. Keep the three that changed how you think in `notes/type-level.md`
- [ ] **Rep:** write a fully typed `fetchJson<T>` wrapper with a typed error union, and a typed event emitter where `on('event', handler)` infers the payload type
- [ ] Strict config: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`. Turn them on in an existing project and fix what breaks
- [ ] Types are erased at runtime. Every trust boundary (network, `localStorage`, `JSON.parse`, URL params) needs runtime validation. **Rep:** validate API responses with `zod` and get the TS types from the schema instead of writing them twice

---

## Phase 4 — Peak (the backend half: contracts, SQL, auth, proxies, shipping)

> Build everything in this phase as **one app**: the API from Track 03 Set 2.3 plus a React frontend. It becomes the frontend and auth half of [Capstone 1](10-capstones.md).

### Set 4.1 — Pydantic and the API contract
- [ ] Pydantic v2's model: validation vs serialisation, lax vs strict mode, `model_validate` vs constructing a model, `model_dump(mode="json")`
- [ ] `Annotated` constraints, `Field`, `field_validator` and `model_validator` (before/after/wrap), computed fields, aliases (`camelCase` on the wire, `snake_case` in Python)
- [ ] Discriminated unions in Pydantic (`Field(discriminator=...)`). They map one-to-one onto the TS unions from Set 3.6
- [ ] `TypeAdapter` for validating things that aren't models, and `pydantic-settings` for config
- [ ] Separate models per direction: `UserCreate`, `UserUpdate` (partial), `UserPublic`. Never return the database row model. **Rep:** prove that a field like `password_hash` can't leak through any endpoint, with a test
- [ ] **Rep — end-to-end types:** FastAPI generates OpenAPI from your Pydantic models → `openapi-typescript` generates TS types → your React client uses them. Rename a field in Python and watch the frontend build fail in CI. **This is the TypeScript approach, applied across the whole stack**
- [ ] Error contract: one error shape for every endpoint (RFC 9457 problem details or your own), mapped to a typed error union on the client
- [ ] Pagination done properly: offset vs **keyset (cursor)** pagination. **Rep:** show offset pagination getting slow and skipping rows under concurrent inserts, then implement keyset pagination with an opaque cursor (link to Track 03 Set 3.1 for the index it needs)

### Set 4.2 — SQL over ORMs
- [ ] The case, stated fairly: ORMs hide the query, the plan, and the transaction boundary; SQL keeps them visible. Also know when an ORM is the right call (simple CRUD admin screens, team conventions)
- [ ] **Rep:** build the same list endpoint twice, once with the SQLAlchemy ORM and lazy relationships, once with hand-written SQL. Turn on query logging. Show the ORM's N+1 (1 + N queries), then show your one query with a join or `json_agg`. `EXPLAIN ANALYZE` both (Track 03 Set 3.2)
- [ ] Drivers: `asyncpg` (`$1` placeholders, binary protocol, prepared statement cache) vs `psycopg` 3 (`%s` placeholders, server-side binding, pipeline mode). Pick one and know its pooling story (Track 03 Set 2.4, including the PgBouncer transaction-mode conflict with prepared statements)
- [ ] **SQL injection:** **Rep:** build an injectable endpoint with string formatting, exploit it (dump another tenant's rows), then fix it with parameters. Also know the cases parameters *can't* cover (dynamic `ORDER BY` column or table names) and handle them with an allowlist
- [ ] **Rep:** write your own thin data-access layer, about 150 lines: a pool, `fetch_one` / `fetch_all` / `execute` that return Pydantic models, an `async with transaction():` context manager that supports savepoints, and per-query timing logs. Keep SQL in `.sql` files or as named constants, not scattered through endpoints
- [ ] Return JSON straight from Postgres for read-heavy endpoints (`json_build_object`, `json_agg`) and measure it against Python-side serialisation
- [ ] Transactions in the API: one transaction per unit of work, `SELECT ... FOR UPDATE` for read-modify-write, retries on serialisation failure (Track 03 Set 3.3). **Rep:** an endpoint that's provably safe under 200 concurrent requests
- [ ] Migrations without ORM models: Alembic with hand-written SQL operations, or plain numbered SQL files with `dbmate`. Keep the expand/contract discipline (Track 03 Set 2.3)
- [ ] TypeScript side: typed SQL with `Kysely`, or `sqlc`-style code generation from `.sql` files. **Rep:** write one endpoint in Fastify + `pg` + Kysely, and compare the safety guarantees with your Python layer

### Set 4.3 — Authentication, built from primitives
Build all of this yourself, without an auth library, then attack it. The Copenhagen Book and the OWASP cheat sheets are your specification.
- [ ] **Password storage:** argon2id parameters, why fast hashes (SHA-256) are wrong, constant-time comparison, and rehashing on login when parameters change
- [ ] Login hardening: rate limiting per account and per IP, the account-enumeration problem (identical responses and timing), lockout vs throttling tradeoffs
- [ ] **Rep — sessions:** server-side sessions stored in Postgres or Redis. The session ID is a random token in a `__Host-` cookie with `HttpOnly; Secure; SameSite=Lax`. Store only a *hash* of the token. Rotate the ID on login (session fixation), invalidate it on logout and password change, and support both idle and absolute expiry
- [ ] **Rep — JWT:** access token plus refresh token, refresh rotation with **reuse detection** (a reused refresh token revokes the whole token family), and a short access-token lifetime. Write down exactly what you give up on revocation compared with sessions
- [ ] **Attack your own auth** and record each result in `notes/auth-attacks.md`:
  - [ ] Session fixation against a version that doesn't rotate
  - [ ] CSRF against cookie auth without `SameSite` or a token
  - [ ] Replaying a stolen JWT after logout
  - [ ] `alg: none` and RS256→HS256 key confusion against a naive verifier
  - [ ] Token theft from `localStorage` via the XSS you built in Set 2.5, and why an `HttpOnly` cookie stops that particular theft but not the XSS itself
- [ ] Write `notes/sessions-vs-jwt.md` with a clear recommendation for a first-party web app, and the cases where you'd choose differently (mobile clients, service-to-service)
- [ ] **MFA:** **Rep:** implement TOTP (RFC 6238 on top of HOTP, RFC 4226) from scratch in about 40 lines, verify it with a real authenticator app, add recovery codes, and handle clock-drift windows
- [ ] Passkeys/WebAuthn: the challenge–response flow and why it resists phishing. **Rep:** add passkey login with a library, and trace the ceremony in DevTools
- [ ] **OAuth 2.0 + OIDC by hand:** **Rep:** implement "Sign in with GitHub" or Google using the authorization code flow with **PKCE**, the `state` parameter, a `nonce`, the code exchange, and ID-token validation against the provider's JWKS. No OAuth library. Then break each protection (drop `state`, skip signature validation) and show what attack each one opens up
- [ ] **Authorization:** RBAC vs ABAC, enforced in one place, plus defence in depth with Postgres RLS (Track 03 Set 2.3). **Rep:** write IDOR tests that try to access another tenant's resources through every endpoint
- [ ] Do the PortSwigger authentication, JWT, and OAuth labs

### Set 4.4 — Reverse proxies (as your app sees them)
Track 05 Set 3.3 load-balanced two instances. This set is about what a proxy changes for the application: headers, cookies, WebSockets, and the SPA.
- [ ] What a reverse proxy does for an app: TLS termination, routing, buffering, compression, static file serving, caching, rate limiting, header rewriting
- [ ] **Rep:** build a reverse proxy yourself in Node `http` or Python `asyncio`, about 150 lines: forward requests, stream bodies both ways, add `X-Forwarded-For` / `-Proto` / `-Host`, round-robin across two upstreams with health checks, and enforce an upstream timeout. Then compare its behaviour with nginx on the same tests
- [ ] nginx `location` matching order (exact, `^~`, regex, prefix) and `proxy_pass` trailing-slash rules. **Rep:** write 8 `location` and `proxy_pass` combinations, predict each rewritten upstream path, then test them
- [ ] **Trusting forwarded headers:** without it, your app thinks every request is plain HTTP from the proxy's IP, so `Secure` cookies, redirects, and rate limiting all break. Configure uvicorn `--proxy-headers --forwarded-allow-ips` correctly. **Rep:** show login breaking behind the proxy, then fix it
- [ ] **Rep:** spoof `X-Forwarded-For` from a client and show your rate limiter being bypassed when the app trusts all hops. Fix it by trusting only the proxy
- [ ] WebSockets through the proxy (`proxy_http_version 1.1`, the `Upgrade` and `Connection` headers) and the default 60-second `proxy_read_timeout` that silently drops idle sockets. Heartbeats
- [ ] Server-Sent Events and buffering: `proxy_buffering off` or `X-Accel-Buffering: no`. **Rep:** show SSE arriving in bursts through the proxy, then fix it
- [ ] **Rep — WebSocket auth:** authenticate the upgrade with the session cookie (and check `Origin`, since browsers don't apply CORS to WebSockets), versus a short-lived ticket in the URL. Know why a bearer token in the query string ends up in logs
- [ ] **Same origin through the proxy:** serve the SPA at `/` and the API at `/api` from one origin. CORS disappears and cookies become first-party. Write down when you'd still choose separate origins
- [ ] Static asset caching: content-hashed filenames with `Cache-Control: immutable`, and `index.html` with `no-cache`. **Rep:** reproduce the "users stuck on the old frontend after deploy" bug, then fix it with headers
- [ ] SPA fallback (`try_files $uri /index.html`), gzip vs brotli, `client_max_body_size` for uploads, and request size and timeout limits
- [ ] Caddy and Traefik as alternatives: automatic TLS, and Traefik's Docker-label discovery. Run the same setup on Caddy and compare config size

### Set 4.5 — Shipping the full stack in containers
Builds on Track 06 Set 2.3 (compose) and Set 2.5 (shipping FastAPI).
- [ ] **Frontend image:** multi-stage, with a Node build stage producing static files and an nginx or Caddy runtime stage. Under 30MB, running as non-root
- [ ] **The build-time env problem:** Vite bakes `import.meta.env` into the bundle, so one image can't be promoted from staging to prod. **Rep:** implement runtime config (a `/config.json` or an injected `window.__CONFIG__` written at container start) so a single image runs in every environment
- [ ] Migrations as a one-shot job that runs before the API starts (a compose service with `service_completed_successfully`, an init container on Kubernetes), not inside app startup
- [ ] **Rep:** one `compose.yaml` that brings up proxy (TLS) + frontend + API + Postgres + PgBouncer + Redis (sessions) + the migration job, on a fresh VM, with your real domain. Login, OAuth, WebSockets, and SSE all work through the proxy
- [ ] Cookie and TLS details in production: `Secure` cookies need HTTPS end to end at the browser, HSTS (and the risk of `preload`), and where `X-Forwarded-Proto` comes from
- [ ] Health checks with meaning: liveness (the process is up) vs readiness (the database is reachable and migrations are applied)
- [ ] **Rep:** deploy the same stack on your Kubernetes cluster (Track 06 Set 3.3) with one Ingress routing `/api` and `/`, sessions in Redis, and a rolling deploy that doesn't log anyone out
- [ ] CI: type-check, unit tests, generated-API-types drift check, build both images, run an end-to-end smoke test with Playwright against the composed stack

### Set 4.6 — Full-stack 3AM drills
Each drill: reproduce it on your own stack, diagnose it using only DevTools, logs, and the shell, fix it, and write it up in `work/12-web/drills/`.
- [ ] **Drill:** "Login works locally, fails in prod." (`Secure` cookie over HTTP, untrusted `X-Forwarded-Proto`, `Domain` mismatch, a redirect loop)
- [ ] **Drill:** "The cookie isn't being sent." Work through your cookie matrix: `SameSite`, `Domain`, `Path`, a missing `credentials: 'include'`, third-party blocking
- [ ] **Drill:** "CORS error" that's actually a 500 with no CORS headers, a preflight hitting auth middleware, or `*` combined with credentials
- [ ] **Drill:** "Every API call is twice as slow from the browser." (Preflights on every request, no `Max-Age`, a non-simple header added by default)
- [ ] **Drill:** "WebSocket drops every 60 seconds." (Proxy idle timeout, no heartbeat)
- [ ] **Drill:** "Users see the old version after a deploy." (Cached `index.html`, a stuck service worker)
- [ ] **Drill:** "Hydration mismatch only in production." (Timezones, locale, an A/B flag read differently on server and client)
- [ ] **Drill:** "The SPA's memory grows on every navigation." (A listener or interval not cleaned up, a closure retaining old pages) — find it with heap snapshot comparison
- [ ] **Drill:** "React page is stuck in a render loop." (A `setState` in render, an effect with an object dependency created every render)
- [ ] **Drill:** "The list endpoint is slow for some tenants." (N+1, a missing keyset index, offset pagination deep into the table)
- [ ] **Drill:** "A deleted user still has access." (JWT lifetime, a session not invalidated, a cached permission)
- [ ] **Capstone:** `notes/web-3am-runbook.md` — symptom-first triage for the browser-to-database path: which DevTools panel to open first, which header to check, which log line to look for

---

## Exit criteria for Track 12

- [ ] Your `MyPromise` passes the Promises/A+ suite and your own React renders a keyed list with hooks
- [ ] You can predict event-loop ordering in both the browser and Node, including rendering
- [ ] Your cookie matrix exists, and you can explain any cookie behaviour from it without guessing
- [ ] You've exploited and then fixed XSS, CSRF, and a CORS misconfiguration in an app you built
- [ ] Your auth (sessions, refresh rotation, TOTP, OAuth with PKCE) was written from primitives and survived your own attacks
- [ ] Types flow from Pydantic to React without being written twice, and CI catches contract drift
- [ ] Your data layer is SQL you wrote, with no N+1 queries, and it's safe under concurrency
- [ ] The full stack runs behind a proxy you understand, from one `compose.yaml`, on a real domain over TLS
