# JP / TW / SG VPNGate checked candidate pools

GitHub Actions runs at minute 17 and 47 of each UTC hour and supports manual dispatch. Scheduling can be delayed. Uses repository Secrets `DOMAIN` and `CHECK_TOKEN`; neither is published. Edge UUIDs, URLs and production inbound credentials must never be committed.

Empty countries are published as count=0, not invented and not a reason to block another working country. `target_source_counts` records the official feed's TCP candidate counts. Check timestamps before use. Checker success is advisory: active production replacements additionally require fail-closed end-to-end tests via the owned edge Worker, two IP databases, Google, GitHub and Cloudflare.

Residential status is unverified; general UDP/IPv6 is unsupported. Active server sidecar health is checked independently by a private systemd timer. Only already provisioned desired country routes can refresh; optional empty countries do not create broken client nodes. The main server and its previous nodes do not depend on the sidecar, and new nodes do not silently fall back to direct.
