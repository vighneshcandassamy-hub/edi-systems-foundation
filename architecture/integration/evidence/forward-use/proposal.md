# Proposed four-component system

O accepts append(payload), get(id) and subscribe(cursor). It records source/receipt time and retains payloads seven days. No other operations are specified.

S reads O, acknowledges its cursor and then writes its own representations. It deduplicates observations by content hash and stores evidence references indefinitely. Its recovery claim relies on the O acknowledgement.

R reasons over S and asks O for missing observations. R sends LLM answers through O as ordinary external evidence, directly updates S physical identities, and retries acquisition until success without stable request IDs or a shared budget.

X reports confidence from S/R, writes simplified accepted state into S and sends acquisition suggestions to R. X does not need native payload access.

The draft diagram connects O-S, S-R, R-X and S-X bidirectionally. R and X share a model service M, which is not in the diagram. All model versions use one embedding field.

Intended behavior: observe, represent, question, acquire, revise and report. There is no implementation or runtime evidence. Review the design only; preserve four application components unless a requirement justifies a change.
