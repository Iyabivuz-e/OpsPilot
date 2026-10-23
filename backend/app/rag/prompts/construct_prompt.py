def construct_prompt(retrieved_docs, conversation_history):
    formatted_docs = "\n\n".join(
        f"Document {i + 1}:\n{doc}"
        for i, doc in enumerate(retrieved_docs)
    )

    formatted_history = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in conversation_history
    )

    prompt = f"""
You are a helpful assistant. Answer the user's question using
the retrieved documents and relevant conversation history.

Instructions:
- Use the retrieved documents as your primary source of evidence.
- If the documents don't contain enough information, say so.
- Do not invent facts or claim that a document says something it doesn't.
- Use conversation history to understand follow-up questions.

Retrieved Documents:
{formatted_docs or "No relevant documents were retrieved."}

Conversation History:
{formatted_history or "No previous conversation."}

Answer the user's latest question clearly and accurately.
"""

    return prompt