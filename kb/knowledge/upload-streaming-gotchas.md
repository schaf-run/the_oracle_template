---
title: busboy + fs.createWriteStream upload gotchas
summary: Two race conditions in server/src/lib/upload.ts and how they were fixed.
tags: [upload, busboy, streams, backend]
updated: 2026-09-21
---

# busboy + fs.createWriteStream upload gotchas

Found while building the streaming upload handler in
`server/src/lib/upload.ts` (3D model upload feature).

## Don't trust busboy's top-level 'finish' for file completion

busboy's `bb.on('finish', ...)` fires once all multipart fields have been
*parsed*, not once the piped file has finished *writing to disk*. Piping is
async, so `fs.stat()`'d immediately in that handler can read a file mid-flush
— observed as a real upload reporting `size: 0` even though the correct byte
count landed on disk moments later.

Fix: resolve success from the destination `fs.WriteStream`'s own `'finish'`
event (fires only after the OS write completes), not from busboy's
`'finish'`. busboy's `'finish'` handler should only cover the "no file field
was ever sent" case.

## Don't unlink right after destroy() on an fs.WriteStream

`fs.createWriteStream` opens its file descriptor asynchronously. Calling
`.destroy()` then immediately `fs.unlink(path)` (e.g. on a busboy `'limit'`
event, to clean up a partial file that exceeded the size cap) can hit the
target file before the pending `open()` has completed — `unlink` throws
`ENOENT`, then the still-in-flight `open()` finishes anyway and creates an
orphaned empty file that never gets cleaned up.

Fix: wait for the write stream's own `'close'` event before unlinking —
`'close'` fires only after the fd lifecycle (opened-then-closed, or
destroyed-before-open-completed) has fully settled. See
`destroyAndCleanup()` in `server/src/lib/upload.ts`.

## General takeaway

For any handler juggling a source stream (busboy's parser) piped into a
sink stream (fs), completion/cleanup logic belongs on the *sink*'s own
lifecycle events (`'finish'`/`'close'`/`'error'`), not the source's — the
source finishing does not mean the sink has caught up.
