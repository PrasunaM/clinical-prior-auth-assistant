## Sprint 2 — RAG Chain with LLM Answer Generation

### What was built
A full Retrieval-Augmented Generation (RAG) pipeline that answers clinical 
prior authorization questions grounded in real payer policy documents.

### Architecture

User Query → Query Rewriting → Payer-Filtered Retriever → Chroma Vectorstore
→ Retrieved Chunks → LangChain RetrievalQA → Ollama llama3 → Grounded Answer

### Corpus — 6 documents across 3 payers
| Document | Payer | Content |
|---|---|---|
| medi_cal_molecular_pathology.pdf | Medi-Cal | TAR criteria by CPT code, Oct 2025 |
| medi_cal_genetic_counseling.pdf | Medi-Cal | Genetic counseling billing & screening |
| medi_cal_mckt_provider_training.pdf | Medi-Cal | Kids & Teens provider framework |
| blue_shield_ca_genetic_testing_dev_delay.pdf | Blue Shield CA | CMA policy for ASD/Dev Delay, Apr 2026 |
| aetna_genetic_testing_cpb0140.pdf | Aetna | Genetic testing medical necessity criteria |
| cms_prior_auth_overview.txt | CMS | Prior auth regulatory overview |

### Key engineering decisions
- **Payer-filtered retrieval** — Aetna CPB 0140 accounts for 64% of corpus 
  chunks (1605/2511). Metadata filtering prevents Aetna from dominating 
  retrieval on Medi-Cal queries.
- **Query rewriting** — Clinical document terminology differs from natural 
  language queries. Rewriting queries to match document language 
  (e.g. "CPT 81228 81229 TAR autism spectrum disorder") significantly 
  improves retrieval precision.
- **Local inference** — Ollama + llama3 for development. Swap to OpenAI 
  or Anthropic API for production sub-second latency (one line change 
  in LangChain).

### Sample query
**Q:** Does Medi-Cal require a TAR for chromosomal microarray testing 
in a child with autism?

**A:** A TAR is required for CPT codes 81228 and 81229 when performing 
chromosomal microarray analysis for autism spectrum disorder with no 
identifiable cause, multiple congenital anomalies without an established 
diagnosis, congenital heart disease, or findings suggestive of primary 
immunodeficiency. *(Source: medi_cal_molecular_pathology.pdf)*

### Known limitations & future work
- Query rewriting is currently manual — next step is automatic query 
  rewriting using LLM before retrieval
- TAR abbreviation occasionally misexpanded by LLM — fix via prompt 
  template update
- Ollama llama3 inference is slow locally (~2-3 min) — production 
  deployment uses API-based LLM