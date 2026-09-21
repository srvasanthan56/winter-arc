# Track 05 — Networking (sockets, TCP, DNS, TLS)

> **Muscle group:** cardio. Unglamorous, and the thing that gives out first when you're under load.
> **Prereqs:** Track 01 Phase 1–2, Track 04 Phase 1 (you need file descriptors and processes).
> **Non-negotiable:** you cannot debug a distributed system (Track 09) without this.

## Why this track

"It works locally but not in staging" is almost always a network problem. So is "it's slow
for users in Singapore," "the connection resets after 60 seconds," "certificate expired,"
and half of all 3AM pages. You said you want basic networks including SSL and DNS — this
track goes a bit past basic, because the basic version doesn't actually let you fix things.

## Equipment

| Resource | Use it for |
|---|---|
| **Stanford CS144: Computer Networking** (cs144.github.io) — free lectures + labs | The backbone. Its labs have you **build a working TCP** in C++. |
| **Beej's Guide to Network Programming** | Socket programming, free, still the best |
| **Computer Networking: A Top-Down Approach** — Kurose & Ross | The textbook, if you want one. Read top-down: app → transport → network → link |
| **High Performance Browser Networking** — Ilya Grigorik (free online) | The practical performance layer. Excellent. |
| Julia Evans — *Bite Size Networking*, *How DNS Works* | The intuition |
| **Wireshark** + `tcpdump` | Your microscope. Non-optional. |
| **The Illustrated TLS Connection** (tls13.xargs.org) | Byte-by-byte TLS 1.3 handshake |

---

## Phase 1 — Foundation (the model and the tools)

### Set 1.1 — Layers and the shape of the thing
- [ ] OSI 7 layers vs the practical TCP/IP 4/5-layer model. Know which is which and use the second one
- [ ] **Encapsulation** — draw an HTTP request wrapped in TCP wrapped in IP wrapped in Ethernet, with real header field names and sizes. Save as `notes/encapsulation.md`
- [ ] MTU, MSS, fragmentation, and **path MTU discovery** (and the black-hole failure mode when ICMP is blocked — this is a real, nasty bug)
- [ ] CS144 Lecture 1–3
- [ ] **Rep:** capture a single HTTP request in Wireshark and expand every layer. Screenshot it and annotate

### Set 1.2 — Wireshark and tcpdump (learn the tool before the theory)
- [ ] `tcpdump -i any -nn port 443`, BPF filter syntax, `-w` to a file, `-A`/`-X` for payload
- [ ] Wireshark: display filters (`tcp.port==443`, `http.request`, `tcp.flags.syn==1`), Follow TCP Stream, Statistics → Conversations, Expert Info, IO Graph
- [ ] **Rep:** capture and identify, by eye, in one pcap: a DNS query/response, a TCP handshake, a TLS handshake, an HTTP request/response, and a connection teardown
- [ ] **Rep:** capture a **failed** connection. Distinguish these four by their packet signatures: connection refused (RST), host unreachable (ICMP), firewall drop (nothing — timeout), and TLS handshake failure. Write all four signatures into `notes/failure-signatures.md`. **This one page will save you hours, repeatedly**

### Set 1.3 — Link and network layer
- [ ] MAC addresses, Ethernet frames, switches vs hubs, ARP. `ip neigh`
- [ ] **Rep:** watch an ARP request/reply in Wireshark. Then poison your own ARP cache in a lab and see what breaks
- [ ] IPv4 addressing, **CIDR and subnet math** (do 20 subnetting problems until it's mechanical), broadcast/network addresses
- [ ] Private ranges (10/8, 172.16/12, 192.168/16), and **your "public networks" question**: public vs private IPs, why your laptop's IP isn't what a website sees, and what a "public network" actually means at the routing level
- [ ] **NAT** — how it rewrites addresses and ports, the connection tracking table, why inbound connections don't work behind NAT, port forwarding, and NAT traversal (STUN/TURN/hole punching)
- [ ] **Rep:** compare `ip addr` output with `curl ifconfig.me`. Explain the difference completely, including where the translation happens
- [ ] Routing: routing tables (`ip route`), default gateway, longest-prefix match, hops. `traceroute`/`mtr` and how they abuse TTL
- [ ] **Rep:** `mtr` to a server on another continent. Interpret the output — where is the latency, where is the packet loss, and why do some hops show 100% loss without breaking the path?
- [ ] BGP at a conceptual level: autonomous systems, peering, and why a BGP misconfiguration takes out large chunks of the internet
- [ ] IPv6: why it exists, address format, why adoption is slow, and dual-stack behavior (Happy Eyeballs)
- [ ] ICMP: echo, unreachable, time exceeded. Why blocking all ICMP breaks things

---

## Phase 2 — Volume (transport: TCP and UDP)

### Set 2.1 — TCP, properly (your listed item)
- [ ] CS144 Lectures 4–8
- [ ] The TCP header, field by field: ports, seq, ack, flags (SYN/ACK/FIN/RST/PSH/URG), window, checksum, options
- [ ] **Three-way handshake** — and why three and not two. SYN cookies and SYN flood defense
- [ ] **Four-way teardown**, half-close, and **`TIME_WAIT`**: why it lasts 2×MSL, why you see thousands of them, `SO_REUSEADDR` vs `SO_REUSEPORT`, and why "just tune `tcp_tw_reuse`" is usually the wrong first answer
- [ ] **The full TCP state machine.** Draw it from memory. Then map `ss -tan` output states onto your drawing
- [ ] Reliability: sequence numbers, cumulative ACKs, SACK, retransmission, RTO and Karn's algorithm, fast retransmit on 3 duplicate ACKs
- [ ] **Flow control**: the receive window, zero-window probes, silly window syndrome
- [ ] **Congestion control**: slow start, congestion avoidance (AIMD), fast recovery. Tahoe/Reno/CUBIC/**BBR**. Understand that flow control protects the *receiver* and congestion control protects the *network* — these are different problems
- [ ] Nagle's algorithm + delayed ACK, and the 40ms latency interaction bug. `TCP_NODELAY`
- [ ] Head-of-line blocking (this motivates HTTP/2 → HTTP/3)
- [ ] Keepalives: TCP keepalive vs application-level heartbeats. Why load balancers kill idle connections at 60s and what that does to your connection pool (link back to Track 03 Set 2.4)
- [ ] **Rep:** `ss -tan` on a busy box. Explain every state you see and what a large count of each would mean
- [ ] **Rep:** use `tc netem` to inject 200ms latency and 5% packet loss on a loopback interface. Watch throughput collapse in Wireshark and identify the retransmissions
- [ ] **Rep:** graph a TCP slow-start ramp from a real capture (Wireshark's IO graph / tcptrace view)

### Set 2.2 — UDP and when reliability isn't the point
- [ ] UDP header (all 8 bytes of it). No handshake, no ordering, no retransmit
- [ ] Where UDP wins: DNS, DHCP, NTP, VoIP/video, game state, QUIC
- [ ] **QUIC / HTTP3** — UDP + TLS 1.3 + stream multiplexing, 0-RTT resumption, connection migration. Why moving from Wi-Fi to cellular doesn't drop your QUIC connection

### Set 2.3 — Socket programming (build it, don't read it)
- [ ] Work through **Beej's Guide** and write the code
- [ ] The socket API in order: `socket`, `bind`, `listen`, `accept`, `connect`, `send`/`recv`, `shutdown`, `close`
- [ ] `sockaddr`, `getaddrinfo`, byte order (`htons`/`ntohl`), blocking vs non-blocking
- [ ] **Rep:** TCP echo server + client in C. Then in Python. Then handle multiple clients with `fork`, then with threads, then with `epoll`/`select` (this is the same exercise as Track 04 Set 2.2 — do it once, count it for both)
- [ ] **Message framing** — the thing everyone gets wrong. TCP is a byte stream, not a message stream. Implement length-prefixed framing and prove it works when you deliberately split a message across two `send` calls
- [ ] **Rep:** write a tiny HTTP/1.1 server from a raw socket. Parse the request line and headers, handle `Content-Length`, return a correct response. No frameworks
- [ ] **Rep (CS144 labs):** implement a reliable byte stream, a reassembler, a TCP receiver, a TCP sender, and a working TCP connection. **This is the single most respected exercise in networking education. If you do nothing else in Phase 2, do this.**

---

## Phase 3 — Strength (DNS, TLS, HTTP)

### Set 3.1 — DNS (your listed item)
- [ ] The hierarchy: root → TLD → authoritative. Recursive resolver vs authoritative server
- [ ] **Rep:** resolve a name by hand with `dig +trace`. Follow every referral from the root. Paste and annotate in `notes/dns-trace.md`
- [ ] Record types: A, AAAA, CNAME, MX, TXT, NS, SOA, SRV, CAA, PTR. What each is for
- [ ] The CNAME-at-apex problem and how ALIAS/ANAME records work around it
- [ ] **TTL and caching** — resolver cache, OS cache, browser cache, and why "I changed DNS but it's still resolving to the old IP" happens. The correct pre-migration TTL-lowering procedure
- [ ] `/etc/hosts`, `/etc/resolv.conf`, `nsswitch.conf`, and the resolution order
- [ ] `dig`, `dig +short`, `dig @8.8.8.8`, `nslookup`, `host`. Prefer `dig`
- [ ] Negative caching, DNS propagation (a misnomer — explain why in one sentence)
- [ ] DNS-based load balancing, GeoDNS, round-robin A records, and their weaknesses
- [ ] DNSSEC at a concept level. DoH/DoT and the privacy/debuggability tradeoff
- [ ] **Rep:** register a cheap domain (or use a free subdomain). Point it at your VM. Set up A, CNAME, MX, and TXT records. Break it deliberately, then debug it with `dig` only
- [ ] **Rep:** `notes/dns-debug.md` — the ordered checklist for "the domain isn't resolving"

### Set 3.2 — TLS/SSL (your listed item)
- [ ] The crypto primitives you need (no more): symmetric vs asymmetric, hashing, HMAC, digital signatures, key exchange (Diffie-Hellman). **What each one guarantees** — confidentiality, integrity, authenticity
- [ ] Why TLS uses asymmetric crypto only to agree on a symmetric key (performance)
- [ ] **TLS 1.2 handshake** vs **TLS 1.3 handshake** (1-RTT, and 0-RTT resumption with its replay caveat)
- [ ] **Rep:** read **tls13.xargs.org** end to end. Then capture a real TLS 1.3 handshake in Wireshark and match the messages: ClientHello, ServerHello, EncryptedExtensions, Certificate, CertificateVerify, Finished
- [ ] Certificates: X.509 structure, subject, SAN (and why CN alone is dead), issuer, validity, key usage
- [ ] **The chain of trust**: leaf → intermediate → root. The OS/browser trust store. **The #1 real-world TLS bug: a missing intermediate certificate** — works in your browser (which caches intermediates), fails in `curl` and in your backend HTTP client. Learn to spot this
- [ ] **Rep:** `openssl s_client -connect host:443 -showcerts` and read the whole chain. Then `openssl x509 -text -noout` on each cert
- [ ] Certificate validation: expiry, hostname match, chain, revocation (CRL, OCSP, OCSP stapling)
- [ ] SNI — why it exists, and how it lets one IP serve many HTTPS sites. ESNI/ECH
- [ ] **Let's Encrypt / ACME** — the HTTP-01 and DNS-01 challenges. `certbot`
- [ ] **Rep:** get a real cert on your VM, serve HTTPS with nginx or Caddy, score an A on ssllabs.com, and set up auto-renewal. Then simulate an expired cert and see exactly how it fails in a browser, in `curl`, and in a Python `requests` call
- [ ] mTLS (mutual TLS) — client certificates, and where it's used (service mesh, zero trust)
- [ ] **Rep:** build your own CA with `openssl`, issue a server and client cert, and set up mTLS between two of your services
- [ ] Where TLS terminates: at the load balancer, at the pod, or end-to-end. The tradeoffs. What `X-Forwarded-Proto` is for

### Set 3.3 — HTTP and the application layer
- [ ] HTTP/1.1: methods, status codes (know the real meaning of 301 vs 302 vs 307/308, 401 vs 403, 502 vs 503 vs 504), headers, `Content-Length` vs chunked transfer encoding
- [ ] Persistent connections, pipelining (and why it failed), head-of-line blocking
- [ ] **HTTP/2**: binary framing, multiplexing, HPACK header compression, server push (and why it was removed). The TCP-level HOL blocking that remains
- [ ] **HTTP/3**: QUIC, and which HOL blocking it actually fixes
- [ ] Caching: `Cache-Control`, `ETag`, `If-None-Match`, `Last-Modified`, `Vary`. CDN caching and cache invalidation strategies
- [ ] CORS — preflight requests, the actual security model, and why "just add `*`" is a bad reflex
- [ ] Cookies: `Secure`, `HttpOnly`, `SameSite`, domain/path scoping. Sessions vs JWT, and where each one's tradeoffs bite
- [ ] WebSockets: the HTTP upgrade handshake, framing, and when to use it vs SSE vs long polling
- [ ] **Rep:** `curl -v` a site. Then `curl --http1.1`, `--http2`, `--http3`. Compare. Learn `curl` flags properly: `-v`, `-I`, `-L`, `-H`, `-d`, `-X`, `--resolve`, `-w '%{time_total}'`, `--trace-time`
- [ ] **Rep:** use `curl -w` with a timing format to break one request into DNS / TCP connect / TLS handshake / TTFB / transfer. **This is how you answer "why is the API slow?"** Save the format string in `notes/curl-timing.md`
- [ ] Load balancing: L4 vs L7, algorithms (round robin, least connections, consistent hashing), health checks, sticky sessions, connection draining
- [ ] Reverse proxies: nginx/Caddy/Envoy config basics. `proxy_pass`, timeouts, buffering, upstream keepalive
- [ ] **Rep:** put nginx in front of two instances of your FastAPI app (Track 03/06). Load balance, add health checks, then kill one instance under load and observe the behavior

---

## Phase 4 — Peak

### Set 4.1 — Bluetooth (your listed item — the curiosity one)
- [ ] The stack: Classic (BR/EDR) vs **BLE**. They are genuinely different protocols sharing a name
- [ ] Physical layer: 2.4GHz ISM band, 40 channels, **adaptive frequency hopping** (and why Bluetooth and Wi-Fi coexist)
- [ ] BLE roles: Central/Peripheral, Broadcaster/Observer. Advertising and scanning. Connection intervals and why they dominate battery life
- [ ] **GATT** — Services, Characteristics, Descriptors, UUIDs. Read/Write/Notify/Indicate. **ATT** underneath it
- [ ] Pairing and bonding: Legacy vs LE Secure Connections, Just Works / Passkey / Numeric Comparison / OOB. MITM protection
- [ ] Profiles: A2DP (audio), HFP, HID. Why audio latency over Bluetooth is what it is — codecs (SBC/AAC/aptX/LC3) and buffering
- [ ] **Rep:** on Linux, use `bluetoothctl` and `btmon` to scan, pair, and watch the actual protocol traffic. Then use `bleak` (Python) to connect to a BLE device (a fitness band, a BLE dev board, or your phone in peripheral mode) and read a GATT characteristic
- [ ] **Rep:** `notes/bluetooth.md` — explain to a non-engineer why Bluetooth audio sometimes stutters in a crowded room, using AFH, interference, and retransmission. Then explain it to an engineer with the actual mechanisms

### Set 4.2 — Network performance and reliability
- [ ] Bandwidth vs latency vs throughput. The **bandwidth-delay product** and why a high-bandwidth high-latency link needs a big window
- [ ] Why latency, not bandwidth, is usually your problem. The speed of light budget between continents
- [ ] CDNs: edge caching, anycast, origin shielding, cache keys
- [ ] Timeouts, **retries with exponential backoff and jitter**, circuit breakers, bulkheads. Why naive retries cause **retry storms** and turn a blip into an outage
- [ ] Idempotency keys — why any retryable write needs one
- [ ] **Rep:** implement a client with timeout + bounded retries + exponential backoff with full jitter + a circuit breaker. Test it against a server you can make fail. Then remove the jitter and demonstrate the thundering herd
- [ ] Read the AWS Builders' Library articles on timeouts/retries/backoff and on load shedding

### Set 4.3 — Network debugging drills
- [ ] **Drill:** "Can't connect." Work the ladder in order: DNS resolves? → TCP connects? → TLS completes? → HTTP responds? Know the exact command for each rung
- [ ] **Drill:** "It works with `curl` but not from the app." (Proxy env vars, different CA bundle, IPv6 vs IPv4, different SNI, missing intermediate)
- [ ] **Drill:** "Intermittent 502s." Upstream timeouts, keepalive mismatch between proxy and upstream, connection reuse after upstream close
- [ ] **Drill:** "Connection resets after exactly 60 seconds." Find the idle timeout in the path
- [ ] **Drill:** "Slow only for large responses." MTU/MSS black hole, or TCP window limits
- [ ] **Drill:** "DNS resolves to the old IP." TTL, cache layers, negative caching
- [ ] **Drill:** "TLS works in Chrome, fails in Python." Missing intermediate or old CA bundle
- [ ] **Capstone:** `notes/network-3am-runbook.md` — ordered triage, exact commands, expected output for each

---

## Exit criteria for Track 05

- [ ] You built a TCP implementation (CS144) or at minimum an epoll server with correct framing
- [ ] You can read a pcap and narrate what happened
- [ ] You can break down a slow HTTP request into DNS/connect/TLS/TTFB and say which one to fix
- [ ] You can debug a TLS chain problem without googling
- [ ] You can draw the TCP state machine from memory
