# How to study IssueInsight

1. Open the module README and choose a chapter.
2. Read **Before we begin**, **What we worked on**, then trace the code excerpts. All excerpts identify their committed file and exact GitHub source location.
3. Follow a real example: who sends the request, which view receives it, which form validates it, which model saves it, and which page receives the response.
4. Use **Related development commits** to see the historical diff. One file can change across many modules; don't assume the entire current file was written in one step.
5. Try the **Teacher / interview questions** without reading the answers. If needed, ask the MU chat to quiz you.
6. Verify tests against real terminal output. Reading a test function does not establish that the test currently passes.
7. Never blindly rerun historic migrations, database resets or Git commands from study material.

**Difference from a chat-export journal:** This edition reconstructs the committed project and links original NOTES.md steps. It cannot recover chat messages or uncommitted intermediate code that was not captured in Git.

**Recommended MU prompt:** "Use this branch's module chapters as a study guide, but verify claims in the actual master-branch code and commit diffs. Teach one chapter at a time. Distinguish implemented functionality from plans."
