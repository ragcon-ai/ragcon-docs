# FAQ

Answers to recurring questions about the Moodle RAGflow suite. Missing something? Open an issue on the
relevant plugin's repository (linked at the top of each [plugin page](plugins/provider.md)).

## Tutor &amp; Helpdesk answers

??? question "The assistant greets the user but adds *“The answer you are looking for is not found in the dataset!”* — even to a plain “hello”. Why?"

    That sentence comes from the **RAGflow assistant's own system prompt**, not from the plugin.
    RAGflow's *default* assistant prompt contains a fixed instruction along the lines of: *“When all
    dataset content is irrelevant to the question, your answer must include the sentence 'The answer you
    are looking for is not found in the dataset!'.”* A greeting matches nothing in the knowledge base, so
    the model both greets **and** appends that mandated sentence.

    This only happens when the block is pointed at an assistant that was **created in RAGflow's own web
    UI** (which seeds that default prompt). Knowledge bases/assistants **created from the block** get a
    clean prompt that does not force the sentence. The block's own *System instruction* setting cannot
    override it either: RAGflow's chat endpoint ignores a per-request system message — the assistant's
    stored prompt always wins.

    **Fix it one of two ways:**

    - **Recommended — use a block-created assistant.** In the block's *Knowledge base / assistant*
      setting choose **➕ Create new knowledge base …** and add the course documents there. The new
      assistant is given the clean prompt automatically.
    - **Or edit the existing assistant in RAGflow.** Open the assistant in RAGflow → *Prompt* and remove
      the “…must include the sentence …not found in the dataset!” clause (and clear *Empty response* if
      it is set). RAGflow only applies such prompt changes in its own UI; the plugin cannot rewrite an
      existing assistant's prompt through the API, which is why a block-created assistant is the simpler
      route.

    See [Tutor block → Knowledge base / assistant](plugins/tutor.md) for where the assistant is chosen.
