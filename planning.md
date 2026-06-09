# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This guide covers student reviews of professors at Appalachian State University. This knowledge is valuable because reviews are scattered across Rate My Professors and hard to search across multiple professors at once. Students cannot easily ask cross-professor questions without manually reading dozens of pages.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/2119118 |
| 2 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/2687695 |
| 3 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/2999455 |
| 4 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/3048819 |
| 5 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/2166822 |
| 6 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/2463681 |
| 7 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/3121188 |
| 8 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/221002 |
| 9 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/3035989 |
| 10 | Rate My Professors | Professor reviews | https://www.ratemyprofessors.com/professor/2008356 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** Professor reviews are short opinions, usually 2-4 sentences each. Small chunks preserve individual opinions without mixing reviews from different professors together. Overlap of 50 characters ensures that key information at chunk boundaries is not lost.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 4

**Production tradeoff reflection:** For production, I would consider OpenAI embeddings for better accuracy on domain-specific text, but they cost money and require API calls. all-MiniLM-L6-v2 runs locally with no cost or rate limits, making it ideal for this project.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Professor Jason Xiong's exams? | Reviews mention exam difficulty and grading style |
| 2 | Which App State professor is known for being helpful outside class? | A professor known for office hours and availability |
| 3 | What do students say about homework load for App State professors? | Reviews mention heavy or light workload |
| 4 | Which professor is recommended for CS students at App State? | A highly rated CS professor |
| 5 | What do students say about lecture style of App State professors? | Reviews mention engaging or boring lectures |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reviews on Rate My Professors are very short (1-2 sentences), which may produce chunks that are too small to carry enough semantic meaning for accurate retrieval.

2. Some chunks may split mid-sentence across chunk boundaries, causing the retrieval to return incomplete thoughts that confuse the LLM during generation.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     Documents (txt files)
    → Ingestion/Cleaning (Python, open())
    → Chunking (300 chars, 50 overlap)
    → Embedding (sentence-transformers, all-MiniLM-L6-v2)
    → Vector Store (ChromaDB)
    → Retrieval (top-4 semantic search)
    → Generation (Groq, llama-3.3-70b-versatile)
    → Answer + Sources (Gradio UI)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I will give Claude my Documents section and Chunking Strategy section and ask it to implement a script that loads .txt files, cleans them, and produces chunks of 300 characters with 50 character overlap.

**Milestone 4 — Embedding and retrieval:** I will give Claude my Retrieval Approach section and architecture diagram and ask it to implement embedding with all-MiniLM-L6-v2 and storage in ChromaDB with source metadata.

**Milestone 5 — Generation and interface:** I will give Claude my full planning.md and ask it to implement the Groq generation function with grounding instructions and source attribution, plus a Gradio interface.
