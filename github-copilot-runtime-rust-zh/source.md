# Source and editorial notes

Source: https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/
Author: Stephen Toub
Published: 2026-09-16
Accessed: 2026-09-18

This video provides a brief factual overview and independent engineering commentary, not a full translation. Storefront, room-sharing, and file-indexing examples are original explanatory examples, not incidents claimed in the article.

Selected facts: over 800,000 production Rust lines; 128 landed migration PRs; prior SDK spawned a Node/V8 CLI; component-wise replacement; native in-process option alongside out-of-process hosting; in-process opt-in at publication; terminal UI layering ongoing; ten-client peak resident-private memory deltas 1,383/247/126 MB; attributed token cost approximately USD 120,000; team contributions remained important.

Benchmark limitations: deterministic localhost completion server removes inference/network latency. Delivered systems differ in more than language alone. The source performance table and adjacent prose/figure disagree about latency/throughput values; the video deliberately omits those disputed figures and uses the consistent memory data only.

Production: Chinese narration; 10 slides; default 0.25 s inter-slide holds; burned subtitles. Publication/upload is a separate optional stage.
