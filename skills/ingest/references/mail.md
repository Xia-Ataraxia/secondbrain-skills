# Mail

Read only the designated message or thread; no arrival, label or scheduled collector authorizes compilation.
`source` is the message/thread identity in a non-private form; account names and workstation paths are not public locators. `author` is the sender as `"[[Name]]"`; `date_published` is the sent date shown in the message; `date_ingested` is today.
`## Original Content` holds the observed message or supplied UTF-8 export verbatim, in order, with sender/recipient roles, dates, quoted history and authorized attachment references.

Do not merge distinct messages by subject or infer missing dates or participants.
Record in `## Ingest Notes` omitted replies, clipped content and attachments not found or inaccessible; a partial thread stays labelled partial.
Analysis cites the exact message and quote location; a summary is not a new source.

Sending, forwarding, labeling, deleting and modifying mail are separate effects, never ingest side effects.
The helper preserves a supplied export; it does not authenticate or query a mailbox.
