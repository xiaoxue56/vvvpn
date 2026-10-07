# JP / KR VPNGate checked candidate pools

GitHub Actions runs at minute 17 and 47 of each UTC hour, and supports manual dispatch. GitHub scheduling can be delayed. Uses repository Secrets `DOMAIN` (owned checker HTTPS origin) and `CHECK_TOKEN` (Bearer authentication); neither is published. Pages contains checked JP/KR SSTP candidate metadata and public VPNGate credentials only. Edge UUIDs, URLs and production inbound credentials must never be committed.

If either country has zero successful checks the job fails and leaves the previously deployed Pages site unchanged. Check timestamps before use. OpenVPN TCP-derived SSTP candidates are accepted only after the owned SSTP checker returns success. Residential status is unverified; general UDP/IPv6 is not supported. These public pools do not change any active production sidecar automatically.

Production is managed independently by private scripts on the server. No third-party subscriptions or checkers are used.
