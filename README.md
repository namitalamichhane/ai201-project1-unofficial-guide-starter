# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
     Student reviews of professors at Appalachian State University. This knowledge is valuable because official course descriptions do not reflect teaching style, exam difficulty, or workload. Students cannot easily search across multiple professors at once without manually reading dozens of Rate My Professors pages.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| 1 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/2119118 |
| 2 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/2687695 |
| 3 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/2999455 |
| 4 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/3048819 |
| 5 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/2166822 |
| 6 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/2463681 |
| 7 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/3121188 |
| 8 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/221002 |
| 9 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/3035989 |
| 10 | Rate My Professors | Reviews | https://www.ratemyprofessors.com/professor/2008356 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**  Professor reviews are short opinions, usually 2-4 sentences. Small chunks preserve individual opinions without mixing reviews from different professors. Overlap ensures key information at chunk boundaries is not lost.

**Final chunk count:** 106

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**  For production I would consider OpenAI's text-embedding-3-large for better accuracy on domain-specific text, but it costs money per API call. all-MiniLM-L6-v2 runs locally with no cost or rate limits making it ideal for this project. For a multilingual system I would consider a multilingual model like paraphrase-multilingual-MiniLM-L12-v2.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** Answer the question using ONLY the information in the provided documents. If the documents don't contain enough information to answer, say 'I don't have enough information on that.' Always cite which document your answer comes from.

**How source attribution is surfaced in the response:** The retrieved chunk source filenames are passed to the LLM as context labels and also displayed separately in the Gradio interface under "Retrieved from"

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| 1 | What do students say about Professor Hodges exams? | Exams are hard and technical | Exams are "really hard" with "trick questions", studying required | Relevant | Accurate |
| 2 | Which App State professor is known for being helpful outside class? | A professor known for office hours | Could not identify professor by name | Partially relevant | Inaccurate |
| 3 | What do students say about homework load? | Reviews mention heavy workload | Found "lots of homework" for CIS1060 class | Relevant | Partially accurate |
| 4 | Which professor is recommended for CS students? | A highly rated CS professor | Could not identify CS-specific professors | Off-target | Inaccurate |
| 5 | What do students say about lecture style? | Reviews mention engaging or boring lectures | Found varying opinions about lecture styles | Relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Which App State professor is known for being helpful outside class?

**What the system returned:** "I don't have enough information on that. The documents provided do not mention the name of the App State professor."

**Root cause:** The documents were saved as generic filenames like prof_2.txt without including the professor's name inside the text. When the query asked for a professor by characteristic, the retrieved chunks contained helpful descriptions but no names, so the LLM could not identify which professor was being described.

**What you would change to fix it:** Add the professor's name as a header at the top of each .txt file before the reviews, so every chunk contains identifying context about which professor is being discussed.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped:** Writing the chunking strategy in planning.md before coding helped me decide on 300 character chunks with 50 character overlap before writing any code. This meant I had a clear target when implementing chunk_text() and did not have to guess at the right size during implementation.

**One way implementation diverged:** My planning.md assumed professor names would be easily retrievable from the reviews, but in practice the reviews rarely mentioned professor names. I had to rely on filenames for source attribution instead, which was not part of my original spec.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md and document structure description
- *What it produced:* A chunk_text() function using fixed character splitting with configurable chunk size and overlap
- *What I changed or overrode:* I kept the chunk size at 300 characters instead of the AI's suggested 500, because my documents are short reviews not long guides


**Instance 2**

- *What I gave the AI:* My full planning.md and pipeline diagram
- *What it produced:* The complete query.py with retrieval and grounded generation using Groq
- *What I changed or overrode:* I strengthened the grounding instruction to explicitly say "ONLY the information in the provided documents" because the original prompt was too weak and the model was drawing from general knowledge
